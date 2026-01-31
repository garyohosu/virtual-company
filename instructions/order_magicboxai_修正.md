# Order - MagicBoxAI 3つの修正（並列実行）

**Status**: ⏳ 修正待ち
**Current Actor**: codex
**Next Actor**: (完了時)

---

## 🎯 ミッション

MagicBoxAI の 3 つの問題を修正してテスト・検証を完了します。

---

## 🔴 修正項目

### 修正 1: /api/health エンドポイント追加

**問題**: API verification で `/api/health` が 404

**解決**:

`magicboxai/main.py` に以下を追加：

```python
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}
```

場所: 他の GET エンドポイント（`/api/check-limit`）の近くに追加。

**検証**: `curl http://localhost:8000/api/health` → `{"status": "ok", ...}` が返ること

---

### 修正 2: DualWriter に isatty() メソッド追加

**問題**: Uvicorn が DualWriter に `isatty()` メソッドを要求

**解決**:

`magicboxai/logging_utils.py` の `DualWriter` クラスに追加：

```python
class DualWriter:
    def __init__(self, *files):
        self.files = files
    
    def write(self, msg):
        for f in self.files:
            f.write(msg)
            f.flush()
    
    def flush(self):
        for f in self.files:
            f.flush()
    
    def isatty(self):
        """Return True if any underlying file is a TTY"""
        return any(hasattr(f, 'isatty') and f.isatty() for f in self.files)
```

**検証**: `python -m magicboxai.main` が エラーなく起動すること

---

### 修正 3: requirements.txt に httpx をピン・テスト依存関係を確認

**問題**: TestClient/httpx のバージョン不一致

**解決**:

`requirements.txt` を確認・更新：

```
fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6
pydantic==2.5.0
python-dotenv==1.0.0
httpx==0.25.1
pytest==7.4.3
pytest-asyncio==0.21.1
```

それから：

```bash
pip install --upgrade -r requirements.txt
python -m pytest tests/test_magicboxai_api.py -v
```

**検証**: `pytest` で全テスト PASS すること

---

## 📋 実行順序

### Step 1: コード修正（並列可能）
- main.py に /api/health 追加
- logging_utils.py に isatty() 追加
- requirements.txt 更新

### Step 2: 依存関係再インストール
```bash
pip install --upgrade -r requirements.txt
```

### Step 3: テスト実行
```bash
python -m pytest tests/test_magicboxai_api.py -v
```

期待: ✅ 全て PASS

### Step 4: 起動テスト
```bash
timeout 10 python -m magicboxai.main
```

期待: ✅ エラーなく起動・停止

### Step 5: API 検証
```bash
# サーバーを起動
python -m magicboxai.main &
sleep 3

# 全エンドポイント検証
curl http://localhost:8000/api/health
curl http://localhost:8000/api/check-limit
curl -X POST http://localhost:8000/api/save -H "Content-Type: application/json" -d '{"html": "<h1>Test</h1>"}'

# 停止
pkill -f "magicboxai.main"
```

期待:
- ✅ /api/health → 200 OK
- ✅ /api/check-limit → 200 OK
- ✅ /api/save → 200 OK

### Step 6: レポート作成

`results/codex/MAGICBOXAI_FIXES_REPORT.md` を作成：

```markdown
# MagicBoxAI - 修正完了レポート

## 修正内容

### 1. /api/health エンドポイント追加
- [x] 実装
- [x] テスト検証
- 結果: [OK / NG]

### 2. DualWriter isatty() メソッド追加
- [x] 実装
- [x] uvicorn 起動テスト
- 結果: [OK / NG]

### 3. requirements.txt 更新・テスト実行
- [x] 依存関係更新
- [x] pytest 実行
- 結果: [全 PASS / 一部失敗]
- テスト数: [N]

## API エンドポイント検証

| エンドポイント | 期待 | 結果 |
|---|---|---|
| GET /api/health | 200 | ✅ |
| GET /api/check-limit | 200 | ✅ |
| POST /api/save | 200 | ✅ |
| DELETE /api/delete/{token} | 200/403 | ✅ |

## 結論

MagicBoxAI MVP は **本番デプロイ準備完了** です。

## 次のステップ

- [ ] Docker コンテナ化
- [ ] 本番デプロイ（Heroku / Railway / Sakura）
- [ ] ユーザーテスト
```

---

## ✅ 成功基準

すべてが満たされること：

- ✅ `/api/health` エンドポイント実装・動作確認
- ✅ DualWriter に isatty() 追加・起動成功
- ✅ pytest 全て PASS
- ✅ 全 API エンドポイント 200 OK
- ✅ レポート作成・GitHub push

---

## 📝 ログ出力

実行後、results/codex に以下が保存されること：

```
MAGICBOXAI_FIXES_REPORT.md
MAGICBOXAI_TEST_RESULTS_AFTER_FIX.md
API_VERIFICATION_AFTER_FIX.md
EXECUTION_LOG.md
RESULT.md
```

---

## 🎯 最後

全て完了したら、git commit & push：

```bash
git add .
git commit -m "[fix] MagicBoxAI - 3つの修正完了

- /api/health エンドポイント追加
- DualWriter isatty() メソッド追加
- requirements.txt httpx バージョン確認
- pytest 全て PASS
- API 全エンドポイント検証完了
- 本番デプロイ準備完了"

git push origin main
```

---

**Status**: 修正実行準備完了
**ユーザーアクション**: 以下を実行

```bash
git pull
codex --yolo order_magicboxai_修正.md を読んで実行してください
```

**すべて自動。** ✅
