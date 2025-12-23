import os
from google import genai
from google.genai import types
import json
from dotenv import load_dotenv

load_dotenv()

# Google Gemini APIの設定
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

# 使用するAIモデル (ユーザー指定: 2.5 flash lite)
MODEL_NAME = "gemini-2.5-flash-lite"

def analyze_and_translate(image_bytes: bytes, text: str) -> dict:
    """
    画像とテキストを受け取り、Geminiを使って以下の処理を行います。
    1. SNS向けの魅力的な投稿文の生成（日本語）
    2. 多言語への翻訳（英語, 繁体字, 簡体字, 韓国語）
    
    戻り値はJSON形式の辞書です。
    """
    
    # AIへの指示書 (プロンプト)
    # JSONで必ず返すように厳格に指示します
    prompt = """
    You are a professional social media manager for a shopping street in Japan.
    Based on the image and the shop owner's comment (text), create an engaging post for SNS.
    Then, translate the content into English (en), Traditional Chinese (zh_tw), Simplified Chinese (zh_cn), and Korean (ko).

    Return ONLY a JSON object with the following structure:
    {
        "enhanced_text": "Japanese content...",
        "en": "English content...",
        "zh_tw": "Traditional Chinese content...",
        "zh_cn": "Simplified Chinese content...",
        "ko": "Korean content..."
    }
    """
    
    try:
        response = client.models.generate_content(
            model=MODEL_NAME, 
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=prompt),
                        types.Part.from_text(text=f"Owner's comment: {text}"),
                        types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                    ]
                )
            ],
            # レスポンス形式をJSONに強制する設定
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema={
                    "type": "OBJECT",
                    "properties": {
                        "enhanced_text": {"type": "STRING"},
                        "en": {"type": "STRING"},
                        "zh_tw": {"type": "STRING"},
                        "zh_cn": {"type": "STRING"},
                        "ko": {"type": "STRING"}
                    },
                    "required": ["enhanced_text", "en", "zh_tw", "zh_cn", "ko"]
                }
            )
        )
        
        # 文字列のJSONをPython辞書に変換
        return json.loads(response.text)
    except Exception as e:
        print(f"AI Service Error: {e}")
        # エラー時はそのまま例外を上げて呼び出し元に通知
        raise e
