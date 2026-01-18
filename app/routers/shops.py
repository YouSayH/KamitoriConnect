from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.schemas.shop import ShopCreate, ShopResponse, ShopUpdate
from app.services import shop_service
from app.auth import get_current_user
from app.models import User

# ルーターの定義
router = APIRouter(
    prefix="/shops",
    tags=["shops"],
)

@router.post("/", response_model=ShopResponse)
async def create_shop(shop: ShopCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    新しい店舗を登録する
    - Adminが作成した場合: オーナー未定（owner_id = None）として作成（後で誰かが参加できる）
    - Ownerが作成した場合: 作成者本人がオーナーになる
    """
    # デフォルトでは作成者本人をオーナーにする
    owner_id = current_user.id
    
    # 【変更点】管理者が作成した場合は、オーナーを「なし(None)」にする
    # これにより、登録画面の「既存の店舗に参加」リストに表示されるようになります
    if getattr(current_user, "role", "owner") == "admin":
        owner_id = None

    return await shop_service.create_shop(db, shop, owner_id=owner_id)
@router.get("/", response_model=List[ShopResponse])
async def read_shops(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    店舗一覧を取得する
    """
    shops = await shop_service.get_shops(db, skip=skip, limit=limit)
    return shops

@router.get("/unclaimed", response_model=List[ShopResponse])
async def read_unclaimed_shops(db: AsyncSession = Depends(get_db)):
    """
    [追加] オーナーが決まっていない店舗一覧を取得 (登録画面用)
    """
    return await shop_service.get_unclaimed_shops(db)

@router.get("/managed", response_model=List[ShopResponse])
async def read_managed_shops(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    [追加] ログインユーザーが管理権限を持つ店舗一覧を取得 (管理画面用)
    - Admin: 全店舗
    - Owner: 自分の店舗
    """
    if current_user.role == "admin":
        # 管理者は全て見れる
        return await shop_service.get_shops(db, limit=1000)
    else:
        # オーナーは自分の店だけ
        return await shop_service.get_shops_by_owner(db, owner_id=current_user.id)

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
    店舗情報を更新する (所有者または管理者のみ)
    """
    # 権限チェックのためにまず現在の情報を取得
    existing_shop = await shop_service.get_shop(db, shop_id=shop_id)
    if existing_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")

    # 管理者(admin) または その店舗のオーナー(owner) であるか確認
    is_admin = getattr(current_user, "role", "owner") == "admin"
    is_owner = existing_shop.owner_id == current_user.id

    if not (is_admin or is_owner):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You do not have permission to edit this shop."
        )

    return await shop_service.update_shop(db, shop_id=shop_id, shop_update=shop)

@router.delete("/{shop_id}", response_model=ShopResponse)
async def delete_shop(shop_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    店舗を削除する (所有者または管理者のみ)
    """
    # 権限チェックのためにまず取得
    existing_shop = await shop_service.get_shop(db, shop_id=shop_id)
    if existing_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")

    is_admin = getattr(current_user, "role", "owner") == "admin"
    is_owner = existing_shop.owner_id == current_user.id

    if not (is_admin or is_owner):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You do not have permission to delete this shop."
        )

    return await shop_service.delete_shop(db, shop_id=shop_id)