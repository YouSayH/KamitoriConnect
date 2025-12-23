import os
import shutil
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import UploadFile
from app.models import Post, Translation
from app.schemas.post import PostCreate
from app.services import ai_service
from sqlalchemy.orm import selectinload

UPLOAD_DIR = "static/images"

async def create_post_with_ai(db: AsyncSession, shop_id: int, original_text: str, image: UploadFile):
    """
    画像とテキストを受け取り、AIで解析・翻訳した上でDBに保存する
    """
    # 1. 画像ファイルの保存
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_extension = image.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_extension}" # ファイル名重複防止のためにUUIDを使用
    file_path = os.path.join(UPLOAD_DIR, file_name)
    
    content = await image.read() # AI送信用にデータをメモリに読み込む
    
    # ディスクへの書き込み
    # (画像データはポインタが進んでいる可能性があるため、書き込みはAI送信後か、リセットが必要だが
    #  変数 content に保持しているのでこれを使う)
    with open(file_path, "wb") as buffer:
        buffer.write(content)
        
    # 2. AIサービスの呼び出し (記事生成・翻訳)
    ai_result = ai_service.analyze_and_translate(content, original_text)
    
    # 3. データベースへの保存
    
    # 投稿(Post)データの作成
    db_post = Post(
        shop_id=shop_id,
        original_text=original_text,
        image_path=f"/static/images/{file_name}" # Webからアクセス可能なパス
    )
    db.add(db_post)
    await db.flush() # IDを発行させるためにflush
    
    # 翻訳(Translation)データの作成
    languages = {
        "ja": ai_result.get("enhanced_text"), # AIが生成した魅力的な日本語文も翻訳の一種として扱う
        "en": ai_result.get("en"),
        "zh-tw": ai_result.get("zh_tw"),
        "zh-cn": ai_result.get("zh_cn"),
        "ko": ai_result.get("ko")
    }
    
    for lang_code, content in languages.items():
        if content:
            trans = Translation(
                post_id=db_post.id,
                language=lang_code,
                translated_content=content
            )
            db.add(trans)
            
    await db.commit()
    await db.refresh(db_post)
    
    # レスポンス用に翻訳データも含めて再取得 (Eager loading)
    # Post取得時にtranslationsも一緒に引いてくる
    stmt = select(Post).options(selectinload(Post.translations)).where(Post.id == db_post.id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_posts(db: AsyncSession, skip: int = 0, limit: int = 100):
    """
    記事一覧を取得する
    """
    # N+1問題を防ぐため、Translationもまとめてロードする
    stmt = select(Post).options(selectinload(Post.translations)).order_by(Post.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()
