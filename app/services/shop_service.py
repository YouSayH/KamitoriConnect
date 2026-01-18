from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from typing import List
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

async def get_unclaimed_shops(db: AsyncSession) -> List[Shop]:
    """
    [追加] オーナーが決まっていない店舗を取得する (登録画面用)
    """
    result = await db.execute(select(Shop).filter(Shop.owner_id == None))
    return result.scalars().all()

async def get_shops_by_owner(db: AsyncSession, owner_id: int) -> List[Shop]:
    """
    [追加] 指定されたオーナーが所有する店舗を取得する (管理画面用)
    """
    result = await db.execute(select(Shop).filter(Shop.owner_id == owner_id))
    return result.scalars().all()

async def create_shop(db: AsyncSession, shop: ShopCreate, owner_id: int = None):
    """
    新しい店舗を作成する
    """
    # Pydanticモデルから辞書に変換し、owner_idを加えてShopインスタンスを作成
    shop_data = shop.model_dump()
    db_shop = Shop(**shop_data, owner_id=owner_id)
    
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

async def claim_shop(db: AsyncSession, shop_id: int, owner_id: int):
    """
    [追加] 既存店舗にオーナーを紐付ける
    """
    shop = await get_shop(db, shop_id)
    # 店舗が存在し、かつまだオーナーがいない場合のみ紐付ける
    if shop and shop.owner_id is None:
        shop.owner_id = owner_id
        await db.commit()
        await db.refresh(shop)
        return shop
    return None