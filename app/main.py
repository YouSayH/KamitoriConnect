from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database import engine, Base
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

# アプリケーションのライフサイクル管理
# 起動時と終了時の処理を定義します
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 起動時の処理: データベースのテーブルを自動作成
    # (本番環境ではマイグレーションツールなどを使うことが推奨されますが、開発用としてシンプルに実装)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 終了時の処理: (今回は特になし)

app = FastAPI(
    title="Kamitori Connect API",
    description="上通商栄会 インバウンド向けAI集客システム API",
    version="0.1.0",
    lifespan=lifespan
)

# CORS (Cross-Origin Resource Sharing) の設定
# フロントエンド (localhost:3000) からのアクセスを許可します
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
from app.routers import shops, posts, chat

# 静的ファイルの配信設定
# 投稿された画像を /static/... でアクセスできるようにします
app.mount("/static", StaticFiles(directory="static"), name="static")

# ルーターの登録
# 各機能のAPIエンドポイントをアプリケーションに追加します
app.include_router(shops.router)
app.include_router(posts.router)
app.include_router(chat.router)

@app.get("/")
def read_root():
    """
    ルートエンドポイント: サーバーが動いているか確認用
    """
    return {"message": "Welcome to Kamitori Connect API"}

@app.get("/health")
def health_check():
    """
    ヘルスチェック: ロードバランサーや監視ツール用
    """
    return {"status": "ok"}
