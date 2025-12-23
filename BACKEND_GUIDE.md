# バックエンド技術ガイド (FastAPI, Python)

このプロジェクトで使用されているバックエンド技術の基礎概念と使い方を解説します。

## 1. FastAPI とは？
Python製の **高速なWeb APIフレームワーク** です。
非常に高速で、**自動的にAPIドキュメント (Swagger UI)** を生成してくれるのが最大の特徴です。

### 主な特徴
- **Type Hints (型ヒント)**: Pythonの標準的な型定義を使用して、入力データのチェック（バリデーション）を自動で行います。
- **Async/Await**: 非同期処理をネイティブにサポートしており、大量のリクエストを効率よく処理できます。

### 基本的な書き方
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

---

## 2. Pydantic (Schemas)
FastAPIとセットで使われる **データバリデーションライブラリ** です。
`app/schemas/` ディレクトリに定義されています。

- **役割**: フロントエンドから送られてくるデータの型チェック、APIレスポンスの整形。
- **使い方**: クラスとして定義します。
    ```python
    class ShopCreate(BaseModel):
        name: str
        description: str | None = None  # 必須ではない
    ```

---

## 3. SQLAlchemy (Models & DB)
Pythonで最も有名な **ORM (Object Relational Mapper)** です。
`app/models.py` に定義されています。

- **役割**: Pythonのクラスとデータベースのテーブルを対応付けます。Pythonコードで書いた操作をSQLに変換してくれます。
- **AsyncSession**: このプロジェクトでは、FastAPIの非同期特性を活かすため、非同期モード (`AsyncSession`) を使用しています。

---

## 4. プロジェクトの構造 (Three-Layer Architecture)
このプロジェクトは、コードを役割ごとに3つの層に分けて管理しています。

1.  **Routers (`app/routers/`)**
    - **受付窓口**です。
    - URL (`/shops` など) と関数を紐付けます。リクエストを受け取り、Serviceを呼び出します。
2.  **Services (`app/services/`)**
    - **ビジネスロジック（仕事の中心）**です。
    - データの加工、計算、AIの呼び出しなど、複雑な処理はここに書きます。
3.  **Models/Schemas (Data Layer)**
    - データの定義です。

### データの流れ
`Frontend` -> `Router` (受付) -> `Service` (処理) -> `Database` or `AI`

---

## 5. 依存性注入 (Dependency Injection)
`Depends(...)` という書き方が頻出します。
これは「必要なもの（例: DB接続）をFastAPIに用意してもらう」仕組みです。

```python
# db: AsyncSession = Depends(get_db) と書くと
# リクエストが来るたびに新しいDB接続を作成し、
# 処理が終わると自動で閉じてくれます。
@router.get("/")
async def get_shops(db: AsyncSession = Depends(get_db)):
    ...
```

## 6. AI連携 (Google GenAI)
`app/services/ai_service.py` で管理しています。
Googleの `google-genai` ライブラリを使用しており、非同期ではなく同期的な処理になる場合もあるため、重い処理は工夫が必要ですが、現状はFastAPIの通常の関数呼び出しの中で行っています。


uvicorn app.main:app --reload --port 8000 