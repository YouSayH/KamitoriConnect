from pydantic import BaseModel, ConfigDict
from typing import Optional

class ShopBase(BaseModel):
    """
    店舗データの基底スキーマ (共通フィールド)
    """
    name: str # 店舗名
    description: Optional[str] = None # 説明文 (任意)
    location: Optional[str] = None # 場所 (任意)
    category: Optional[str] = None # カテゴリ (任意)
    map_url: Optional[str] = None
    reservation_url: Optional[str] = None

class ShopCreate(ShopBase):
    """
    店舗作成時のスキーマ
    """
    pass

class ShopUpdate(ShopBase):
    """
    店舗更新時のスキーマ
    ここではnameも任意にしています
    """
    name: Optional[str] = None

class ShopResponse(ShopBase):
    """
    APIレスポンス用のスキーマ
    IDを含みます
    """
    id: int

    # ORMモデルからPydanticモデルへの変換を有効化
    model_config = ConfigDict(from_attributes=True)
