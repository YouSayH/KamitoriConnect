from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services import chat_service

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    """
    AIチャットボットAPI
    ユーザーの質問を受け取り、店舗情報を元に回答を生成します。
    """
    response_text = await chat_service.generate_chat_response(db, request.message, request.history)
    return ChatResponse(response=response_text)
