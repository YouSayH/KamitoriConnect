import os
import shutil
import uuid
from datetime import datetime
from fastapi import FastAPI, Header, HTTPException, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

# 静的ファイル（画像）とテンプレートの設定
os.makedirs("static/uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# メモリ上のデータベース（サーバーを再起動すると消えます）
tweets_db = []

# X APIのリクエストボディを模倣
class TweetPayload(BaseModel):
    text: str
    media_id: str = None  # 画像ID（簡易実装）

# --- 1. ダッシュボード（タイムライン表示） ---
@app.get("/feed", response_class=HTMLResponse)
async def read_feed(request: Request):
    """投稿された内容をX風に表示する画面"""
    # 新しい順に表示
    sorted_tweets = sorted(tweets_db, key=lambda x: x['created_at'], reverse=True)
    return templates.TemplateResponse("feed.html", {"request": request, "tweets": sorted_tweets})

# --- 2. 画像アップロード用エンドポイント (Media Upload APIの模倣) ---
@app.post("/1.1/media/upload")
async def upload_media(
    file: UploadFile = File(...),
    authorization: str = Header(None) # APIキーチェック用
):
    # 簡易的なAPIキー認証チェック
    if not authorization or "Bearer" not in authorization:
        raise HTTPException(status_code=401, detail="Unauthorized: API Key missing")

    # 画像を保存
    file_id = str(uuid.uuid4())
    extension = file.filename.split(".")[-1]
    file_path = f"static/uploads/{file_id}.{extension}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # X APIに近いレスポンスを返す
    return {
        "media_id_string": file_id,
        "media_key": file_id,
        "url": f"/{file_path}" # ローカルでの表示用URL
    }

# --- 3. ツイート投稿用エンドポイント (/2/tweets の模倣) ---
@app.post("/2/tweets")
async def create_tweet(
    payload: TweetPayload,
    authorization: str = Header(None) # APIキーチェック用
):
    # 参考情報に基づき、Bearer Token等の認証をチェックするフリをする
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # データベースに保存
    new_tweet = {
        "id": str(len(tweets_db) + 1),
        "text": payload.text,
        "created_at": datetime.now(),
        "image_url": None
    }

    # 画像IDがあればURLを紐付け
    if payload.media_id:
        # staticフォルダ内の画像を探す簡易ロジック
        for filename in os.listdir("static/uploads"):
            if payload.media_id in filename:
                new_tweet["image_url"] = f"/static/uploads/{filename}"
                break

    tweets_db.append(new_tweet)

    # 参考情報にあるレスポンス形式 を模倣
    return {
        "data": {
            "id": new_tweet["id"],
            "text": new_tweet["text"]
        }
    }

if __name__ == "__main__":
    import uvicorn
    # localhost:8000 で起動
    uvicorn.run(app, host="0.0.0.0", port=8001)
