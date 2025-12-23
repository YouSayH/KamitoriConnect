import os

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.models import User
from app.auth import get_password_hash, verify_password, create_access_token, get_current_user
from pydantic import BaseModel

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

class UserCreate(BaseModel):
    """ユーザー登録用のスキーマ"""
    email: str # EmailStr is strict, relaxing for now to avoid 422 on simple inputs.
    password: str
    invite_code: str

class Token(BaseModel):
    """トークンレスポンス用のスキーマ"""
    access_token: str
    token_type: str

@router.post("/register", response_model=Token)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    新規ユーザー登録
    """
    # 招待コードを取得
    correct_invite_code = os.getenv("INVITE_CODE")
    # 環境変数が設定されていない場合や、コードが間違っている場合はエラー
    # (念のため correct_invite_code が None の場合もエラー扱いにして安全側に倒します)
    if not correct_invite_code or user.invite_code != correct_invite_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid invitation code"
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
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    # トークン発行してログイン状態にする
    access_token = create_access_token(data={"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """
    ログイン (トークン発行)
    """
    # ユーザー検索
    result = await db.execute(select(User).filter(User.email == form_data.username)) # OAuth2Formのusernameフィールドにemailが入る
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
    現在のユーザー情報を取得 (トークン検証テスト用)
    """
    return {"email": current_user.email, "id": current_user.id}
