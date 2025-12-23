from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.schemas.shop import ShopCreate, ShopResponse, ShopUpdate
from app.services import shop_service
from app.auth import get_current_user
from app.models import User

# ルーターの定義
# prefix="/shops" なので、このファイルのAPIは全て /shops から始まります
router = APIRouter(
    prefix="/shops",
    tags=["shops"],
)

@router.post("/", response_model=ShopResponse)
async def create_shop(shop: ShopCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    新しい店舗を登録する (ログイン必須)
    """
    return await shop_service.create_shop(db, shop)

@router.get("/", response_model=List[ShopResponse])
async def read_shops(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    店舗一覧を取得する
    """
    shops = await shop_service.get_shops(db, skip=skip, limit=limit)
    return shops

@router.get("/{shop_id}", response_model=ShopResponse)
async def read_shop(shop_id: int, db: AsyncSession = Depends(get_db)):
    """
    ID指定で店舗詳細を取得する
    """
    db_shop = await shop_service.get_shop(db, shop_id=shop_id)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop

@router.put("/{shop_id}", response_model=ShopResponse)
async def update_shop(shop_id: int, shop: ShopUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    店舗情報を更新する (ログイン必須)
    """
    db_shop = await shop_service.update_shop(db, shop_id=shop_id, shop_update=shop)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop

@router.delete("/{shop_id}", response_model=ShopResponse)
async def delete_shop(shop_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    店舗を削除する (ログイン必須)
    """
    db_shop = await shop_service.delete_shop(db, shop_id=shop_id)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop
