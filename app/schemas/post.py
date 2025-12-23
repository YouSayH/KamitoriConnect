from pydantic import BaseModel, ConfigDict
from typing import List, Optional
import datetime

class TranslationResponse(BaseModel):
    """
    翻訳結果のレスポンススキーマ
    """
    language: str # 言語コード
    translated_content: str # 翻訳された内容

    model_config = ConfigDict(from_attributes=True)

class PostBase(BaseModel):
    """
    記事データの基底スキーマ
    """
    original_text: str # 投稿文

class PostCreate(PostBase):
    """
    記事作成時のスキーマ
    画像はマルチパートフォームデータで送られるためここには含みません
    """
    shop_id: int

class PostResponse(PostBase):
    """
    記事レスポンス用のスキーマ
    """
    id: int
    shop_id: int
    image_path: Optional[str] = None # 画像のURLパス
    created_at: datetime.datetime # 投稿日時
    translations: List[TranslationResponse] = [] # 翻訳リスト

    model_config = ConfigDict(from_attributes=True)
