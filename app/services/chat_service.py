from sqlalchemy.ext.asyncio import AsyncSession
from google.genai import types
from app.services import shop_service, ai_service
from app.schemas.chat import ChatHistoryItem

async def generate_chat_response(db: AsyncSession, message: str, history: list[ChatHistoryItem] = []) -> str:
    """
    ユーザーのチャットメッセージに対するAIの応答を生成します。
    RAG (Retrieval-Augmented Generation) の簡易実装として、
    現在登録されている全店舗情報をコンテキスト（文脈）としてAIに与えます。
    """
    # 1. コンテキスト作成のために全店舗データを取得
    # 店舗数が増えた場合は、ベクトル検索などへの移行を検討する必要があります
    shops = await shop_service.get_shops(db, limit=1000)
    
    # 2. 店舗データをプロンプト用に整形
    shops_context = ""
    for shop in shops:
        shops_context += f"- ID: {shop.id}, Name: {shop.name}, Category: {shop.category}, Description: {shop.description}, Location: {shop.location}, Map URL: {shop.map_url}\n"
        
    # 3. システムプロンプトの構築
    # ここでAIの役割（ペルソナ）と知識（店舗リスト）を定義します
    system_instruction = f"""
    You are a friendly and helpful AI tourist guide for the 'Kamitori Shopping Street' (Kamitori Shoueikai) in Kumamoto, Japan.
    
    Here is a list of shops in the shopping street:
    {shops_context}
    
    Please answer the user's question based on this information.
    If the user asks about location or where a shop is, please provide the 'Map URL' if available.
    Respond in the same language as the user's question.
    """
    # Gemini APIの形式 (types.Content) に変換
    contents = []

    for item in history:
        # フロントエンドのroleとGeminiのroleを合わせる必要があればここで変換
        # (今回はフロントエンドから "user", "model" で送らせる想定)
        role = "user" if item.role == "user" else "model"
        contents.append(types.Content(
            role=role,
            parts=[types.Part.from_text(text=item.content)]
        ))
    
    # 最新のメッセージを追加
    contents.append(types.Content(
        role="user",
        parts=[types.Part.from_text(text=message)]
    ))
    
    # 4. Gemini APIを呼び出して回答生成
    try:
        response = ai_service.client.models.generate_content(
            model=ai_service.MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7, # 創造性の度合い (0.0~2.0)
            )
        )
        return response.text
    except Exception as e:
        print(f"Chat Service Error: {e}")
        return "Sorry, I am having trouble connecting to my brain right now. Please try again later."
