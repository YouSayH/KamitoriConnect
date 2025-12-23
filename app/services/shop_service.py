from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from app.models import Shop
from app.schemas.shop import ShopCreate, ShopUpdate

async def get_shop(db: AsyncSession, shop_id: int):
    """
    IDで店舗を1件取得する
    """
    result = await db.execute(select(Shop).filter(Shop.id == shop_id))
    return result.scalars().first()

async def get_shops(db: AsyncSession, skip: int = 0, limit: int = 100):
    """
    店舗一覧を取得する (ページネーション対応)
    """
    result = await db.execute(select(Shop).offset(skip).limit(limit))
    return result.scalars().all()

async def create_shop(db: AsyncSession, shop: ShopCreate):
    """
    新しい店舗を作成する
    """
    db_shop = Shop(**shop.model_dump())
    db.add(db_shop)
    await db.commit() # 変更を確定
    await db.refresh(db_shop) # 新しいID等の情報を再取得
    return db_shop

async def update_shop(db: AsyncSession, shop_id: int, shop_update: ShopUpdate):
    """
    店舗情報を更新する
    """
    db_shop = await get_shop(db, shop_id)
    if not db_shop:
        return None
    
    # 更新されたフィールドだけを反映
    update_data = shop_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_shop, key, value)
    
    await db.commit()
    await db.refresh(db_shop)
    return db_shop

async def delete_shop(db: AsyncSession, shop_id: int):
    """
    店舗を削除する
    """
    db_shop = await get_shop(db, shop_id)
    if not db_shop:
        return None
    
    await db.delete(db_shop)
    await db.commit()
    return db_shop
