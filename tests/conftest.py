import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.database import Base
from app.models import Shop, Post

# テスト用インメモリデータベース
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture
async def test_db():
    """
    テストごとにインメモリDBを作成し、テーブル構築・データ投入を行い、
    セッションを返すフィクスチャ
    """
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    # テーブル作成
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # セッション作成
    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    
    async with SessionLocal() as session:
        # --- テストデータの投入 ---
        # 店舗データ
        shop1 = Shop(name="Kumamoto Ramen Keika", category="Ramen", description="Famous tonkotsu ramen.", location="North Area")
        shop2 = Shop(name="Okada Coffee", category="Cafe", description="Relaxing retro cafe.", location="South Area")
        session.add_all([shop1, shop2])
        await session.commit()
        await session.refresh(shop1)
        
        # 投稿データ
        post1 = Post(shop_id=shop1.id, original_text="New seasonal ramen is out!")
        session.add(post1)
        await session.commit()
        
        yield session
        
        # テスト終了後のクリーンアップ（インメモリなので閉じるだけで消える）
        await session.close()
    
    await engine.dispose()