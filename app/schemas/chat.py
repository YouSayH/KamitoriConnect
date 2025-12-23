from pydantic import BaseModel
from typing import List

class ChatHistoryItem(BaseModel):
    role: str # "user" or "model"
    content: str

class ChatRequest(BaseModel):
    """
    チャットリクエストのスキーマ
    """
    message: str # 最新のユーザーメッセージ
    history: List[ChatHistoryItem] = []

class ChatResponse(BaseModel):
    """
    AIのチャットレスポンスのスキーマ
    """
    response: str