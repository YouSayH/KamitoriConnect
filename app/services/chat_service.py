import logging
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from google.genai import types
from app.services import ai_service
from app.schemas.chat import ChatHistoryItem

# --- ロガーの設定 ---
# ログファイル "rag_debug.log" に詳細なログを書き出します
logger = logging.getLogger("kamitori_rag")
logger.setLevel(logging.INFO)

# フォーマット設定 (読みやすさ重視)
formatter = logging.Formatter(
    '\n%(asctime)s [%(levelname)s] ----------------------------------------\n%(message)s'
)

# ハンドラの設定 (コンソールとファイル)
if not logger.handlers:
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler("rag_debug.log", encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
# --------------------

async def generate_chat_response(db: AsyncSession, message: str, history: list[ChatHistoryItem] = []) -> str:
    """
    SQL RAG方式によるチャット応答生成
    1. 現在のDB状態から動的にスキーマ情報を作成
    2. ユーザーの質問をSQLに変換
    3. DBで実行
    4. 結果を元に回答を生成
    """
    
    # [Log 1] ユーザーの質問
    logger.info(f"🔍 [1. User Question]\n{message}")

    # 1. 動的スキーマ情報の生成
    # カテゴリ一覧や店名の例を埋め込んだリッチなスキーマを作成します
    schema_info = await _get_dynamic_schema_info(db)
    
    # 2. SQL生成 (Natural Language to SQL)
    sql_query = await _generate_sql(message, schema_info)
    
    if not sql_query:
        logger.warning("⚠️ [SQL Generation Failed]")
        return "申し訳ありません。質問の意図をうまく理解できませんでした。"

    # [Log 2] 生成されたSQL
    logger.info(f"🛠️ [2. Generated SQL]\n{sql_query}")

    # 3. DB実行
    try:
        # NOTE: 本番環境では読み取り専用ユーザーの使用や、SQLインジェクション対策(バリデーション等)を推奨
        result = await db.execute(text(sql_query))
        rows = result.mappings().all()
        
        # 検索結果が空の場合
        if not rows:
            query_result = "No matching shops or posts found."
        else:
            # 結果をJSON文字列化してコンテキストにする
            # datetime型などが含まれる場合のために default=str を指定
            query_result = json.dumps([dict(row) for row in rows], ensure_ascii=False, default=str)
            
        # [Log 3] SQLの実行結果
        logger.info(f"📊 [3. SQL Output]\n{query_result}")

    except Exception as e:
        logger.error(f"❌ [SQL Execution Error]\n{e}")
        # SQL生成ミスなどの場合は、汎用的な回答へフォールバックするかエラーを返す
        return "データベースの検索中にエラーが発生しました。もう一度お試しください。"

    # 4. 回答生成 (Retrieval Augmented Generation)
    final_answer = await _generate_answer(message, query_result, history)
    
    # [Log 5] LLMの最終回答 (_generate_answer内でプロンプトのログも出力しています)
    logger.info(f"🤖 [5. LLM Output]\n{final_answer}")
    
    return final_answer

async def _get_dynamic_schema_info(db: AsyncSession) -> str:
    """
    DBから実際のデータを少し取得して、よりリッチなスキーマ情報を作成する
    """
    try:
        # カテゴリ一覧を取得 (重複排除)
        cat_result = await db.execute(text("SELECT DISTINCT category FROM shops WHERE category IS NOT NULL"))
        categories = [row.category for row in cat_result if row.category]
        categories_str = ", ".join(categories)

        # 店舗名の例を3件取得
        name_result = await db.execute(text("SELECT name FROM shops LIMIT 3"))
        example_names = ", ".join([row.name for row in name_result if row.name])
    except Exception as e:
        print(f"Schema Info Generation Error: {e}")
        # エラー時は空文字にして最低限のスキーマで動かすなどのフォールバック
        categories_str = "Various"
        example_names = "Example Shop"

    # 動的なスキーマ定義文字列を作成
    schema_text = f"""
Table: shops
Columns:
- id (INTEGER, Primary Key)
- name (TEXT, Name of the shop. Examples: {example_names})
- description (TEXT, Description of the shop)
- location (TEXT, Location or address)
- category (TEXT, Category. Valid values: {categories_str})
- map_url (TEXT, Google Maps URL)
- reservation_url (TEXT, Reservation URL)

Table: posts
Columns:
- id (INTEGER, Primary Key)
- shop_id (INTEGER, Foreign Key to shops.id)
- original_text (TEXT, Content of the post)
- created_at (TIMESTAMP)
"""
    return schema_text

async def _generate_sql(question: str, schema_info: str) -> str:
    """
    自然言語の質問をSQLクエリに変換する内部関数
    """
    prompt = f"""
    You are a SQL expert. Convert the user's question into a SQL query for a SQLite database.
    
    Database Schema:
    {schema_info}
    
    Rules:
    1. Return ONLY the SQL query. No markdown formatting.
    2. Use 'LIKE' for fuzzy text matching.
    3. If the user asks about a category, match closely with 'Valid values'.
    4. Limit the result to 5 rows if not specified.
    
    User Question: {question}
    """
    
    try:
        response = ai_service.client.models.generate_content(
            model=ai_service.MODEL_NAME,
            contents=[types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
        )
        # 余分なマークダウン記号などを除去
        sql = response.text.replace("```sql", "").replace("```", "").strip()
        return sql
    except Exception as e:
        logger.error(f"SQL Generation Error: {e}")
        return ""

async def _generate_answer(question: str, context: str, history: list[ChatHistoryItem]) -> str:
    """
    検索結果(context)を元に回答を生成する内部関数
    """
    system_instruction = """
    You are a friendly AI tourist guide for 'Kamitori Shopping Street'.
    
    Resource:
    - Database Results (JSON format, mainly in Japanese).

    **CORE RULE: LANGUAGE MATCHING**
    - You MUST answer in the SAME LANGUAGE as the User's Question.
    - If the user asks in English, your answer MUST be in English.
    - If the user asks in Traditional Chinese, your answer MUST be in Traditional Chinese.
    - **NEVER** reply in Japanese unless the user asks in Japanese.

    **Step-by-Step Response Generation:**
    1. **Identify Language**: Determine the language of the User's Question.
    2. **Extract Data**: Get info from 'Database Results'.
    3. **Translate Content**: If the detected language is different from the database content (Japanese), TRANSLATE the shop descriptions, categories, and names naturally.
    4. **Format Output**: Present the shops clearly.
    
    **Output Format:**
    - Do NOT output your internal thinking process. Just output the final response to the user.
    - Keep URLs (Map URL, Reservation URL) as is.
    """
    
    contents = []
    
    # 履歴の構築
    for item in history:
        # フロントエンドのroleとGeminiのroleを合わせる
        role = "user" if item.role == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part.from_text(text=item.content)]))
        
    # 今回のプロンプト
    current_prompt = f"""
    User Question: {question}
    
    Database Results (Context):
    {context}
    """
    
    contents.append(types.Content(role="user", parts=[types.Part.from_text(text=current_prompt)]))
    
    # --- [Log 4] 完全なプロンプトコンテキストの生成と出力 ---
    # システム指示、履歴、今回の入力をすべて結合してログに残します
    full_log_text = "--- [System Instruction] ---\n" + system_instruction + "\n\n"
    
    if history:
        full_log_text += "--- [Chat History] ---\n"
        for item in history:
            full_log_text += f"[{item.role}]: {item.content}\n"
        full_log_text += "\n"
    
    full_log_text += "--- [Current Prompt] ---\n" + current_prompt
    
    logger.info(f"📝 [4. Final Prompt Context (FULL)]\n{full_log_text}")
    # ----------------------------------------------------
    
    try:
        response = ai_service.client.models.generate_content(
            model=ai_service.MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7, # 創造性の度合い
            )
        )
        return response.text
    except Exception as e:
        logger.error(f"Answer Generation Error: {e}")
        return "すみません、エラーが発生しました。"