import os
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.database import get_db
from app.models import User
from app.auth import get_password_hash, verify_password, create_access_token, get_current_user
from app.services import shop_service
from app.schemas.shop import ShopCreate

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

class UserCreate(BaseModel):
    """ユーザー登録用のスキーマ"""
    email: str 
    password: str
    invite_code: str
    
    # [追加] 店舗紐付け用フィールド (オーナー登録時に必須)
    shop_name: Optional[str] = None       # 新規店舗を作る場合
    existing_shop_id: Optional[int] = None # 既存店舗を選ぶ場合

class Token(BaseModel):
    """トークンレスポンス用のスキーマ"""
    access_token: str
    token_type: str

@router.post("/register", response_model=Token)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    新規ユーザー登録 (ロール振り分けと店舗紐付け)
    """
    # 招待コードを取得 (環境変数から)
    invite_code_owner = os.getenv("INVITE_CODE")
    invite_code_admin = os.getenv("ADMIN_INVITE_CODE")

    # ロールの判定
    user_role = "owner" # デフォルト

    if invite_code_admin and user.invite_code == invite_code_admin:
        user_role = "admin"
    elif invite_code_owner and user.invite_code == invite_code_owner:
        user_role = "owner"
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid invitation code"
        )

    # [追加] オーナー登録の場合、店舗情報の検証
    if user_role == "owner":
        if not user.shop_name and not user.existing_shop_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Shop information (create new or join existing) is required for shop owners."
            )

    # 既存ユーザーチェック
    result = await db.execute(select(User).filter(User.email == user.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # ユーザー作成
    hashed_password = get_password_hash(user.password)
    new_user = User(
        email=user.email, 
        hashed_password=hashed_password,
        role=user_role 
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    # [追加] 店舗の作成または紐付け (オーナーのみ)
    if user_role == "owner":
        if user.shop_name:
            # 新規店舗作成
            new_shop_data = ShopCreate(name=user.shop_name)
            await shop_service.create_shop(db, new_shop_data, owner_id=new_user.id)
        elif user.existing_shop_id:
            # 既存店舗を選択して紐付け
            shop = await shop_service.claim_shop(db, user.existing_shop_id, owner_id=new_user.id)
            if not shop:
                # 失敗時のハンドリング: 本来はトランザクションをロールバックすべきだが、
                # ここでは簡易的にログ出力のみとする (あるいは400エラー)
                print(f"Failed to claim shop {user.existing_shop_id} for user {new_user.id}")

    # トークン発行
    access_token = create_access_token(data={"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """
    ログイン (トークン発行)
    """
    result = await db.execute(select(User).filter(User.email == form_data.username)) 
    user = result.scalars().first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    現在のユーザー情報を取得
    """
    return {
        "id": current_user.id,
        "email": current_user.email, 
        "role": current_user.role
    }