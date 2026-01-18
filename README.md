# Kamitori Connect (上通商栄会 AI集客システム)

上通商栄会のインバウンド観光客向け多言語対応AIシステムです。
店主の負担を最小限にしつつ、外国人観光客への魅力発信と、AIチャットによる快適な接客体験を提供します。

## 主な機能

1.  **AI記事作成・多言語翻訳 & SNS自動投稿**
    * 店主は「写真」と「一言コメント」をアップロードするだけ。
    * AI (Gemini 2.5 Flash lite) が魅力的な紹介文を自動生成。
    * 英語・繁体字・簡体字・韓国語へ自動翻訳し、DB保存と同時にSNSへ拡散。
2.  **AI観光コンシェルジュ (SQL RAG搭載)**
    * **Natural Language to SQL**: ユーザーの質問（「ラーメン屋はある？」など）をAIがSQLクエリに変換し、データベースから直接・正確に情報を検索。
    * 検索結果を元に、Geminiが文脈に沿った自然な回答を多言語で生成します。
3.  **X風モックアプリ (SNS連携シミュレーター)**
    * 実際のX (旧Twitter) APIを使用せずに、画像付き投稿やフィード表示をテストできるローカルアプリ。
    * 開発中の動作確認やデモに最適です。
4.  **店舗管理ダッシュボード**
    * シンプルなUIで店舗情報の登録・編集が可能。

## 技術スタック

* **Backend**: Python, FastAPI, SQLAlchemy (Async), Google GenAI SDK
* **Frontend**: TypeScript, Next.js 15 (App Router), Tailwind CSS, Shadcn UI
* **Database**: SQLite (開発用) / MySQL (本番想定)
* **AI Model**: Gemini 2.5 Flash lite
* **Mock Service**: FastAPI (X Mock Server)

## 起動方法

### 前提条件
* Python 3.10+
* Node.js v18+ (推奨 v20+)
* Google Gemini API Key (環境変数 `GEMINI_API_KEY` に設定)

### 1. Backend 起動
メインのAPIサーバーです。
```powershell
# プロジェクトルートで実行
cd kamitouriShoueikai

# 仮想環境の有効化 (Windowsの場合)
.\venv\Scripts\activate
# (Mac/Linuxの場合: source venv/bin/activate)

# 依存ライブラリのインストール
pip install -r requirements.txt

# サーバー起動 (Port: 8000)
uvicorn app.main:app --reload
```
*   API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. X Mock Server 起動 (SNS連携用)

SNS投稿機能をテストするためのモックサーバーです。

```powershell
# 別ターミナルで実行 (仮想環境有効化後)
python x_mock_demo/server.py
```

* Mock Feed (タイムライン): [http://localhost:8001/feed](http://localhost:8001/feed)
* サーバーは Port 8001 で動作します。

### 3. Frontend 起動

ユーザーおよび管理者向けのWeb画面です。

```powershell
# 別ターミナルで実行
cd kamitouriShoueikai/frontend

# 依存ライブラリのインストール
npm install

# 開発サーバー起動 (Port: 3000)
npm run dev
```
*   Web App: [http://localhost:3000](http://localhost:3000)

## ディレクトリ構成
```
kamitouriShoueikai/
├── app/                 # FastAPI Backend Code
│   ├── main.py
│   ├── models.py        # Database Models
│   ├── routers/         # API Endpoints
│   ├── schemas/         # Pydantic Models
│   └── services/        # Business Logic & AI
│   │   ├── chat_service.py # SQL RAG Implementation
│   │   └── sns_service.py  # Connects to X Mock
├── frontend/            # Next.js Frontend Code
│   ├── app/             # App Router Pages
│   └── components/      # UI 
├── x_mock_demo/         # X (Twitter) Mock Application
│   ├── server.py        # Mock API Server
│   └── templates/       # Mock UI
├── static/              # Uploaded Images
├── requirements.txt     # Python Dependencies
└── kamitouri.db         # SQLite Database
```
