import os
import requests

# モックサーバーのURL (ポート8001)
MOCK_X_API_URL = "http://localhost:8001"
API_KEY = "dummy_api_key_12345"

def post_to_x(text: str, image_path: str = None):
    """
    生成された記事と画像をX(モック)に投稿する
    """
    media_id = None
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    try:
        # 1. 画像アップロード
        if image_path and os.path.exists(image_path):
            print(f"[SNS] Uploading image: {image_path}")
            with open(image_path, 'rb') as f:
                files = {'file': f}
                # モックサーバーの画像アップロードエンドポイント
                media_res = requests.post(
                    f"{MOCK_X_API_URL}/1.1/media/upload",
                    headers=headers,
                    files=files
                )
                
            if media_res.status_code == 200:
                media_id = media_res.json().get("media_id_string")
                print(f"[SNS] Image uploaded. Media ID: {media_id}")
            else:
                print(f"[SNS] Image upload failed: {media_res.text}")

        # 2. ツイート投稿
        print(f"[SNS] Posting tweet: {text[:20]}...")
        payload = {"text": text}
        if media_id:
            payload["media_id"] = media_id

        response = requests.post(
            f"{MOCK_X_API_URL}/2/tweets",
            json=payload,
            headers=headers
        )

        if response.status_code == 200:
            print("[SNS] Post successful!")
            return True
        else:
            print(f"[SNS] Post failed: {response.status_code} {response.text}")
            return False

    except Exception as e:
        print(f"[SNS] Error connecting to X Mock Server: {e}")
        return False