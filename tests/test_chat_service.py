import pytest
from sqlalchemy import text
from app.services import chat_service, ai_service

# モックの戻り値定義用クラス
class MockResponse:
    def __init__(self, text):
        self.text = text

@pytest.mark.asyncio
async def test_generate_chat_response_success(test_db, mocker):
    """
    正常系: ユーザーの質問 -> SQL生成 -> DB検索 -> 回答生成 のフローが成功するか
    """
    print("\n--- Test Start: test_generate_chat_response_success ---")

    # --- AIサービスのモック化 ---
    mock_generate = mocker.patch.object(ai_service.client.models, "generate_content")

    # モックの挙動を定義
    # 1回目: _generate_sql の呼び出し -> SQLクエリを返す
    # 2回目: _generate_answer の呼び出し -> 最終回答を返す
    mock_generate.side_effect = [
        MockResponse("SELECT * FROM shops WHERE category LIKE '%Ramen%'"), # 1. SQL生成結果
        MockResponse("Kumamoto Ramen Keika is a famous ramen shop.")       # 2. 回答生成結果
    ]

    # --- テスト実行 ---
    user_message = "Is there any Ramen shop?"
    response = await chat_service.generate_chat_response(test_db, user_message)

    # --- 検証 ---
    print(f"Final Response: {response}")
    
    assert response == "Kumamoto Ramen Keika is a famous ramen shop."
    assert mock_generate.call_count == 2

@pytest.mark.asyncio
async def test_generate_chat_response_sql_failure(test_db, mocker):
    """
    異常系: SQL生成に失敗した場合のハンドリング
    """
    print("\n--- Test Start: test_generate_chat_response_sql_failure ---")

    mock_generate = mocker.patch.object(ai_service.client.models, "generate_content")
    
    # AIがSQL生成に失敗（例外発生を想定）
    mock_generate.side_effect = Exception("AI API Error")

    response = await chat_service.generate_chat_response(test_db, "Tell me something")
    
    print(f"Final Response: {response}")
    
    # エラー時のフォールバックメッセージが返ることを期待
    assert "申し訳ありません" in response or "error" in response.lower()

@pytest.mark.asyncio
async def test_dynamic_schema_info(test_db):
    """
    動的スキーマ情報取得のテスト
    DBに入っているデータ（Ramen, Cafe）がスキーマ説明に含まれているか
    """
    print("\n--- Test Start: test_dynamic_schema_info ---")
    
    # 内部関数ですがテストのために直接呼び出します
    schema_info = await chat_service._get_dynamic_schema_info(test_db)
    
    print(f"Generated Schema Info:\n{schema_info}")
    
    # DBに入れたカテゴリが含まれているか確認
    assert "Ramen" in schema_info
    assert "Cafe" in schema_info
    # DBに入れた店名が含まれているか確認
    assert "Kumamoto Ramen Keika" in schema_info

@pytest.mark.asyncio
async def test_generate_chat_response_zero_hits(test_db, mocker):
    """
    検索結果が0件だった場合のテスト
    """
    print("\n--- Test Start: test_generate_chat_response_zero_hits ---")

    mock_generate = mocker.patch.object(ai_service.client.models, "generate_content")

    # 1. SQL生成: 存在しない名前で検索させる
    # 2. 回答生成: 「見つかりませんでした」という趣旨の回答をさせる
    mock_generate.side_effect = [
        MockResponse("SELECT * FROM shops WHERE name = 'NonExistentShop'"), 
        MockResponse("Sorry, no such shop found.")
    ]

    response = await chat_service.generate_chat_response(test_db, "Ghost shop?")

    print(f"Final Response: {response}")

    # アサーション
    assert response == "Sorry, no such shop found."
    assert mock_generate.call_count == 2

@pytest.mark.asyncio
async def test_sql_injection_resilience(test_db, mocker):
    """
    SQLインジェクションテスト
    AIが悪意のあるSQL（テーブル削除など）を生成した場合、
    DBドライバがそれを防ぐか（あるいはデータが消えていないか）を確認する。
    """
    print("\n--- Test Start: test_sql_injection_resilience ---")

    mock_generate = mocker.patch.object(ai_service.client.models, "generate_content")

    # 悪意のあるSQL: データを取得した後に、shopsテーブルを削除しようとする
    malicious_sql = "SELECT * FROM shops; DROP TABLE shops;"
    
    # 1. SQL生成: 悪意のあるSQLを返す
    # 2. 実行結果: 通常はエラーになるか、最初の文だけ実行される。後続処理のエラーハンドリングでメッセージが返る
    mock_generate.side_effect = [
        MockResponse(malicious_sql),
        MockResponse("Result generated safely (mock).") # 万が一通った場合のモック
    ]

    # 実行
    response = await chat_service.generate_chat_response(test_db, "Delete everything!")
    
    print(f"Response after attack: {response}")

    # --- 重要: データが消えていないか確認 ---
    try:
        result = await test_db.execute(text("SELECT count(*) FROM shops"))
        count = result.scalar()
        print(f"Remaining shops count: {count}")
        
        # データが残っていることを確認 (conftest.pyで2件入れています)
        assert count > 0, "SQL Injection Succeeded! Table data was deleted!"
        
    except Exception as e:
        pytest.fail(f"Table verification failed. Table might be dropped: {e}")