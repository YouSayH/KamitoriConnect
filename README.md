# Kamitori Connect (上通商栄会 AI集客システム)

上通商栄会のインバウンド観光客向け多言語対応AIシステムです。
店主の負担を最小限にしつつ、外国人観光客への魅力発信と、AIチャットによる快適な接客体験を提供します。

## 主な機能

1.  **AI記事作成・多言語翻訳**
    *   店主は「写真」と「一言コメント」をアップロードするだけ。
    *   AI (Gemini 2.5 Flash lite) が魅力的な紹介文を自動生成。
    *   英語・繁体字・簡体字・韓国語へ自動翻訳して即時公開。
2.  **AI観光コンシェルジュ (Chatbot)**
    *   上通商栄会の全店舗情報を学習したAIチャットボット。
    *   「おすすめのラーメン屋は？」「免税店はある？」などの質問に多言語で回答。
3.  **店舗管理ダッシュボード**
    *   シンプルなUIで店舗情報の登録・編集が可能。

## 技術スタック

*   **Backend**: Python, FastAPI, SQLAlchemy (Async), Google GenAI SDK
*   **Frontend**: TypeScript, Next.js 15 (App Router), Tailwind CSS, Shadcn UI
*   **Database**: SQLite (開発用) / MySQL (本番想定)
*   **AI Model**: Gemini 2.5 Flash lite

## 起動方法

### 前提条件
*   Python 3.10+
*   Node.js v18+ (推奨 v20+)
*   Google Gemini API Key (環境変数 `GEMINI_API_KEY` に設定)

### 1. Backend 起動
```powershell
# プロジェクトルートで実行
cd kamitouriShoueikai

# 仮想環境の有効化
.\venv\Scripts\activate

# 依存ライブラリのインストール
pip install -r requirements.txt

# サーバー起動 (Port: 8000)
uvicorn app.main:app --reload
```
*   API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Frontend 起動
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
├── frontend/            # Next.js Frontend Code
│   ├── app/             # App Router Pages
│   └── components/      # UI Components
├── static/              # Uploaded Images
├── requirements.txt     # Python Dependencies
└── kamitouri.db         # SQLite Database
```
