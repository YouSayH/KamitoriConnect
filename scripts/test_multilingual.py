import requests
import time

# テスト対象のAPIエンドポイント
API_URL = "http://localhost:8000/chat"

# テストする言語と質問のリスト
test_cases = [
    {"lang": "🇨🇳 Chinese (Traditional)", "question": "有推薦的拉麵店嗎？"},
    {"lang": "🇨🇳 Chinese (Simplified)", "question": "有推荐的拉面店吗？"},
    {"lang": "🇰🇷 Korean", "question": "추천해주실 만한 라멘 가게가 있나요?"},
    {"lang": "🇰🇭 Khmer (Cambodia)", "question": "តើមានហាងមីណែនាំទេ?"},
    {"lang": "🇹🇭 Thai", "question": "มีร้านราเม็งแนะนำไหม?"},
    {"lang": "🇲🇾 Malay", "question": "Adakah kedai ramen yang anda syorkan?"},
    {"lang": "🇵🇭 Filipino (Tagalog)", "question": "May mairerekomenda ka bang ramen shop?"},
    {"lang": "🇻🇳 Vietnamese", "question": "Có quán ramen nào bạn muốn giới thiệu không?"},
    {"lang": "🇸🇬 Singapore (English)", "question": "Got any good ramen shop recommend?"},
    {"lang": "🇮🇳 Hindi", "question": "क्या आप किसी रमेन की दुकान की सिफारिश कर सकते हैं?"},
    {"lang": "🇮🇩 Indonesian", "question": "Ada rekomendasi restoran ramen?"},
    {"lang": "🇩🇪 German", "question": "Können Sie einen Ramen-Laden empfehlen?"},
    {"lang": "🇫🇷 French", "question": "Pouvez-vous recommander un restaurant de ramen ?"},
    {"lang": "🇺🇸 English", "question": "Can you recommend a ramen shop?"},
    {"lang": "🇯🇵 Japanese (Base)", "question": "おすすめのラーメン屋は？"},
]

def run_test():
    print(f"🚀 Starting Multilingual Test against {API_URL}...\n")
    

    for case in test_cases:
        lang = case["lang"]
        q = case["question"]
        
        print(f"Testing {lang}...")
        print(f"  Q: {q}")
        
        try:
            # POSTリクエスト送信
            # チャットAPIの仕様に合わせて JSON body を調整してください
            response = requests.post(API_URL, json={"message": q}, timeout=30)
            
            if response.status_code == 200:
                answer = response.text
                # レスポンスがJSONで返ってくる場合は .json() を使う
                # 今回の chat_service は文字列(text)を返している想定ですが、
                # もしJSON ({ "response": "..." }) なら response.json()["response"] に変更
                
                # ログ表示 (長い場合は切り詰める)
                display_answer = answer.replace("\n", " ")[:100] + "..."
                print(f"  A: {display_answer}")
                print("  ✅ OK\n")
            else:
                print(f"  ❌ Error: Status {response.status_code}")
                print(f"  Response: {response.text}\n")
                
        except Exception as e:
            print(f"  ❌ Request Failed: {e}\n")
        
        # API制限（Rate Limit）を考慮して少し待機
        time.sleep(2)

    print("🎉 All tests completed!")

if __name__ == "__main__":
    run_test()