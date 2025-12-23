from pydantic import BaseModel

class ChatRequest(BaseModel):
    """
    チャットリクエストのスキーマ
    """
    message: str # ユーザーからのメッセージ

class ChatResponse(BaseModel):
    """
    チャットレスポンスのスキーマ
    """
    response: str # AIからの返答
