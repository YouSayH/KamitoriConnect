import requests
import os

# --- 設定（ここをAPI登録画面のように見せかける） ---
API_KEY = "dummy_api_key_12345"  # 何を入れても動くように作っています
BASE_URL = "http://localhost:8000" # 本来は https://api.twitter.com

# ヘッダー情報のセット（OAuth 2.0 Bearer Token認証のフリ）
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def post_to_x_mock(text, image_path=None):
    media_id = None

    # 1. 画像がある場合は先にアップロード
    if image_path and os.path.exists(image_path):
        print(f"📷 画像をアップロード中: {image_path} ...")
        files = {'file': open(image_path, 'rb')}
        # アップロード用エンドポイント (v1.1仕様を模倣)
        media_res = requests.post(f"{BASE_URL}/1.1/media/upload", headers={"Authorization": f"Bearer {API_KEY}"}, files=files)
        
        if media_res.status_code == 200:
            media_id = media_res.json().get("media_id_string")
            print(f"✅ 画像アップロード成功 (ID: {media_id})")
        else:
            print("❌ 画像アップロード失敗")

    # 2. ツイートを投稿 (v2仕様を模倣)
    print(f"📝 投稿中: {text} ...")
    payload = {"text": text}
    if media_id:
        payload["media_id"] = media_id

    response = requests.post(
        f"{BASE_URL}/2/tweets",
        json=payload,
        headers=headers
    )

    if response.status_code == 200:
        print("🚀 投稿成功！")
        print("レスポンス:", response.json())
    else:
        print(f"❌ 投稿失敗: {response.status_code}")
        print(response.text)

# --- 実行 ---
if __name__ == "__main__":
    # テキストのみの投稿
    post_to_x_mock("X APIのデモテストです。これはテキスト&画像の投稿。")
    
    # 画像付きの投稿（実際に画像ファイルを同じフォルダに置いて試してください）
    post_to_x_mock("画像付きの投稿テスト！", "2c6ca464-fd44-40eb-941a-9f88de4a1620.jpg") 
