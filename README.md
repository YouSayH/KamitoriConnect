# Kamitori Connect (上通商栄会 AI集客システム)

上通商栄会のインバウンド観光客向け多言語対応AIシステムです。
店主の負担を最小限にしつつ、外国人観光客への魅力発信と、AIチャットによる快適な接客体験を提供します。

## 📖 目次

1. 主な機能
2. 技術スタック
3. 環境構築
4. 起動方法
5. 使い方 (デモ)
6. 今後の実装したい機能

---

## 🚀 主な機能

1. **AI記事作成・多言語翻訳 & SNS自動投稿**
* 店主は「写真」と「一言コメント」をアップロードするだけ。
* AI (Gemini 2.5 Flash lite) が魅力的な紹介文を自動生成。
* 英語・繁体字・簡体字・韓国語へ自動翻訳し、DB保存と同時にSNSへ拡散。


2. **AI観光コンシェルジュ (SQL RAG搭載)**
* **Natural Language to SQL**: ユーザーの質問（「ラーメン屋はある？」など）をAIがSQLクエリに変換し、データベースから直接・正確に情報を検索。
* 検索結果を元に、Geminiが文脈に沿った自然な回答を多言語で生成します。


3. **X風モックアプリ (SNS連携シミュレーター)**
* 実際のX (旧Twitter) APIを使用せずに、画像付き投稿やフィード表示をテストできるローカルアプリ。


4. **店舗管理ダッシュボード**
* シンプルなUIで店舗情報の登録・編集が可能。



---

## 👥 ロール（役割）と権限

システムには主に3つの役割が存在します。

| ロール | 対象ユーザー | 招待コード (.env) | できること (役割) |
| --- | --- | --- | --- |
| **管理者**<br>(Admin) | 商店街組合、運営事務局 | .envの`ADMIN_INVITE_CODE`に記入 | ・全店舗データの管理・編集<br>・全ユーザーの管理<br>・システム全体設定の変更 |
| **店舗オーナー**<br>(Shop Owner) | 各店舗の店主・スタッフ | .envの`INVITE_CODE`に記入 | ・自店舗情報の登録・編集<br>・AI記事作成（写真アップロード）<br>・SNS投稿の実行<br>・自店舗に関する翻訳内容の確認 |
| **観光客/ゲスト**<br>(Guest) | 上通を訪れるお客様 | (不要) | ・AI観光コンシェルジュ (チャット) の利用<br>・店舗検索、多言語記事の閲覧<br>・ログイン不要で利用可能 |

---

## 🛠 技術スタック

* **Backend**: Python, FastAPI, SQLAlchemy (Async), Google GenAI SDK
* **Frontend**: TypeScript, Next.js 15 (App Router), Tailwind CSS, Shadcn UI
* **Database**: SQLite (開発用) / MySQL (本番想定)
* **AI Model**: Gemini 2.5 Flash lite
* **Mock Service**: FastAPI (X Mock Server)

---

## ⚙️ 環境構築・要件

### 💻 システム要件 (PCスペック)

本システムをローカル環境で動作させるために必要なスペックは以下の通りです。

* **メモリ (RAM)**: アプリケーション動作に **約 800MB** 使用
* *(OSやブラウザを含めると、PC全体で 8GB以上のメモリ搭載を推奨、EC2やLightSailなどで使う場合は4GB以上のメモリがあるといいかも？)*


* **ストレージ (Disk)**: **約 600MB**
* *(Pythonライブラリ、Nodeモジュール、画像キャッシュ等を含む)*


* **OS**: Windows 10/11, macOS, Linux (Ubuntu等)

### 前提ソフトウェア

* Python 3.10+
* Node.js v18+ (推奨 v20+)
* Google Gemini API Key

### 1. リポジトリのクローン

```bash
git clone https://github.com/yousayh/kamitoriconnect.git
cd kamitoriconnect

```

### 2. 環境変数 (.env) の作成

プロジェクトルートに `.env` ファイルを作成し、以下の内容を記述してください。

```ini
# .env file

# Google AI Studioで取得したAPIキー(https://aistudio.google.com/api-keys)
GEMINI_API_KEY=your_gemini_api_key_here

# 認証用のシークレットキー（適当なランダム文字列でOK）
SECRET_KEY=change_this_to_a_random_secret_string

# ユーザー登録用招待コード（任意の文字列）
# 登録時にこのコードを入力することで、オーナー権限や管理者権限が付与されます
INVITE_CODE=kamitori_owner
ADMIN_INVITE_CODE=kamitori_admin

# データベースURL（デフォルトはSQLite）
DATABASE_URL=sqlite+aiosqlite:///./kamitouri.db

```

*参考: `app/routers/auth.py` で招待コード、`app/main.py` でDB設定が読み込まれます。*

### 3. バックエンドのセットアップ

```bash
# 仮想環境の作成と有効化 (Windows)
python -m venv venv
.\venv\Scripts\activate
# (Mac/Linuxの場合: source venv/bin/activate)

# 依存パッケージのインストール
pip install -r requirements.txt

```

### 4. フロントエンドのセットアップ

```bash
cd frontend
npm install
cd ..

```

---

## ▶️ 起動方法

システム全体を動作させるには、以下の3つのターミナルを開き、それぞれ実行してください。

### ① Backend (API Server)

```bash
# プロジェクトルートで実行 (venv有効化状態で)
uvicorn app.main:app --reload --port 8000

```

* **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
* 正常に起動すると `Welcome to Kamitori Connect API` が表示されます。

### ② X Mock Server (SNS連携用)

```bash
# プロジェクトルートで実行 (venv有効化状態で)
python x_mock_demo/server.py

```

* **Mock Feed**: [http://localhost:8001/feed](http://localhost:8001/feed)
* ポート **8001** で起動し、擬似的なX (Twitter) 環境を提供します。

### 3. Frontend 起動

ユーザーおよび管理者向けのWeb画面です。

```bash
# 別ターミナルで実行
cd frontend
# 依存ライブラリのインストール

npm run dev
# 開発サーバー起動 (Port: 3000)
npm run dev
```

* **Web App**: [http://localhost:3000](http://localhost:3000)

---

## 🎥 使い方 (デモ)

### 1. 管理者・店舗オーナー機能

#### ユーザー登録 & 店舗参加

招待コード (`kamitori_owner` または `kamitori_admin`) を使用してアカウントを作成し、店舗を登録または既存店舗に参加します。


#### AI記事作成 & 自動翻訳

写真をアップロードし、一言コメントを入れるだけで、AIが魅力的な文章を作成し、多言語に翻訳します。


### 2. SNS連携シミュレーション

#### X (旧Twitter) への自動投稿

作成された記事は、即座にモックサーバー（仮想SNS）に画像付きで投稿されます。


### 3. 観光客向け機能

#### 多言語AIコンシェルジュ

「ラーメンが食べたい」「お土産のおすすめは？」などの質問に対し、データベースの最新情報を元にAIが回答します。


---

## 📂 ディレクトリ構成

```
kamitouriShoueikai/
├── app/                 # FastAPI Backend Code
│   ├── main.py
│   ├── models.py        # Database Models
│   ├── routers/         # API Endpoints (Auth, Shops, Posts, Chat)
│   ├── schemas/         # Pydantic Models
│   └── services/        # Business Logic & AI (RAG, Gemini)
├── frontend/            # Next.js Frontend Code
│   ├── app/             # App Router Pages
│   └── components/      # UI Components
├── x_mock_demo/         # X (Twitter) Mock Application
│   ├── server.py        # Mock API Server (Port 8001)
│   └── templates/       # Mock UI (feed.html)
├── static/              # Uploaded Images
├── requirements.txt     # Python Dependencies
├── schema.sql           # SQL Schema definition
└── kamitouri.db         # SQLite Database

```

## 6. 今後の実装したい機能

1. **ユーザー管理**: ロール（管理者/オーナー）の明確化、動的招待コード（24時間有効）、ユーザー削除機能。
2. **店舗管理**: 登録時の詳細設定、Googleマップ連携。
3. **投稿機能**: 承認プロセス（確認・編集・再生成）、アカウント切り替え（公式/独自API）。
4. **UI/UX**: ログイン状態（ロール・店舗）の可視化。
5. **多言語対応**: 翻訳機能の明記。
6. **分析**: コンシェルジュやSNSデータの蓄積・分析。