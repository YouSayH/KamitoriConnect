from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.schemas.post import PostResponse
from app.services import post_service

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)

@router.post("/", response_model=PostResponse)
async def create_post(
    shop_id: int = Form(...), # フォームデータとしてshop_idを受け取る
    text: str = Form(...),    # フォームデータとしてテキストを受け取る
    image: UploadFile = File(...), # ファイルアップロードとして画像を受け取る
    db: AsyncSession = Depends(get_db)
):
    """
    AIを使った記事作成API
    写真とコメントを受け取り、AI生成・翻訳を行った上で投稿を作成します。
    """
    try:
        return await post_service.create_post_with_ai(db, shop_id, text, image)
    except Exception as e:
        # 何らかのエラーが発生した場合は500エラーを返す
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[PostResponse])
async def read_posts(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    投稿記事の一覧を取得する
    """
    return await post_service.get_posts(db, skip=skip, limit=limit)
