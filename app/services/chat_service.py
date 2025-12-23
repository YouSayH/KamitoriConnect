from sqlalchemy.ext.asyncio import AsyncSession
from google.genai import types
from app.services import shop_service, ai_service

async def generate_chat_response(db: AsyncSession, message: str) -> str:
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
        shops_context += f"- ID: {shop.id}, Name: {shop.name}, Category: {shop.category}, Description: {shop.description}\n"
        
    # 3. システムプロンプトの構築
    # ここでAIの役割（ペルソナ）と知識（店舗リスト）を定義します
    system_instruction = f"""
    You are a friendly and helpful AI tourist guide for the 'Kamitori Shopping Street' (Kamitori Shoueikai) in Kumamoto, Japan.
    
    Here is a list of shops in the shopping street:
    {shops_context}
    
    Please answer the user's question based on this information.
    If the user asks about something not in the list, politely say you don't have information about that, but try to recommend something similar from the list if possible.
    Respond in the same language as the user's question (Japanese, English, Chinese, Korean, etc.).
    Keep your answers concise and engaging.
    """
    
    # 4. Gemini APIを呼び出して回答生成
    try:
        response = ai_service.client.models.generate_content(
            model=ai_service.MODEL_NAME,
            contents=[
                types.Content(
                   role="user",
                   parts=[
                       types.Part.from_text(text=message)
                   ]
                )
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7, # 創造性の度合い (0.0~2.0)
            )
        )
        return response.text
    except Exception as e:
        print(f"Chat Service Error: {e}")
        return "Sorry, I am having trouble connecting to my brain right now. Please try again later."
