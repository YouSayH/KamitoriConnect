from sqlalchemy import String, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import Base
import datetime

class Shop(Base):
    """
    店舗情報を管理するモデル
    """
    __tablename__ = "shops"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False) # 店舗名
    description: Mapped[str] = mapped_column(Text, nullable=True) # 店舗説明
    location: Mapped[str] = mapped_column(String(255), nullable=True) # 場所
    category: Mapped[str] = mapped_column(String(100), nullable=True) # カテゴリ (例: ラーメン, 雑貨)
    map_url: Mapped[str] = mapped_column(String(500), nullable=True) # GoogleMapのURL

    # リレーション: 店舗に関連する投稿
    posts = relationship("Post", back_populates="shop", cascade="all, delete-orphan")

class Post(Base):
    """
    SNS投稿(記事)を管理するモデル
    """
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    shop_id: Mapped[int] = mapped_column(ForeignKey("shops.id"), nullable=False) # どの店舗の投稿か
    original_text: Mapped[str] = mapped_column(Text, nullable=False) # 元の投稿文(日本語)
    image_path: Mapped[str] = mapped_column(String(255), nullable=True) # 画像ファイルへのパス
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP, server_default=func.now()
    ) # 作成日時

    # リレーション
    shop = relationship("Shop", back_populates="posts")
    translations = relationship("Translation", back_populates="post", cascade="all, delete-orphan")

class Translation(Base):
    """
    記事の翻訳データを管理するモデル
    """
    __tablename__ = "translations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False) # 元の記事ID
    language: Mapped[str] = mapped_column(String(10), nullable=False) # 言語コード (例: 'en', 'zh-tw')
    translated_content: Mapped[str] = mapped_column(Text, nullable=False) # 翻訳された内容

    # リレーション
    post = relationship("Post", back_populates="translations")

class User(Base):
    """
    管理者ユーザーを管理するモデル
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
