import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

# データベース接続URLを取得 (デフォルトはSQLite)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./kamitouri.db")

# 非同期エンジンを作成
engine = create_async_engine(
    DATABASE_URL,
    echo=True, # 開発中はSQLログを出力 (本番ではFalse推奨)
)

# 非同期セッションファクトリ
# これを使ってデータベースとのセッションを作成します
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# モデル定義の基底クラス
class Base(DeclarativeBase):
    pass

# DBセッションを取得する依存関係 (Dependency)
# FastAPIのDependsで使用します
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
