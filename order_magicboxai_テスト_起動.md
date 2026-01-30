# Order - MagicBoxAI テスト・起動・検証

**Status**: ⏳ 実行待ち
**Current Actor**: codex
**Next Actor**: (完了時）

---

## 🎯 ミッション

MagicBoxAI MVP を完全に動作確認して、サービスを起動・検証します。

---

## 📋 実行タスク

### Task 1: 依存関係をインストール

```bash
pip install -r requirements.txt
```

出力：FastAPI, Uvicorn, pytest その他がインストールされます。

---

### Task 2: ユニットテスト実行

```bash
python -m pytest tests/test_magicboxai_api.py -v
```

期待結果：
- ✅ テスト成功（全て PASS）
- または 🟡 いくつかスキップ（ローカル環境依存）

テスト結果を `results/codex/MAGICBOXAI_TEST_RESULTS.md` に保存してください。

---

### Task 3: データベース初期化

```bash
python -m scripts.init_db
```

期待結果：
- ✅ SQLite DB が `magicboxai.db` として作成
- ✅ `files` テーブル、`track_limit_daily` テーブル、`promo_codes` テーブルが作成
- ✅ テスト用プロモコード（5個）が生成

初期化ログを `results/codex/DB_INIT_LOG.md` に保存してください。

---

### Task 4: アプリケーション起動テスト

```bash
timeout 10 python -m magicboxai.main
```

または Windows:

```powershell
$process = Start-Process python -ArgumentList "-m magicboxai.main" -PassThru
Start-Sleep -Seconds 10
Stop-Process -InputObject $process
```

期待結果：
- ✅ サーバー起動成功
- ✅ `INFO: Uvicorn running on http://localhost:8000`
- ✅ 10秒後、正常に停止

起動ログを `results/codex/APP_STARTUP_LOG.md` に保存してください。

---

### Task 5: API エンドポイント検証

```bash
# サーバーをバックグラウンドで起動
python -m magicboxai.main &

# 少し待つ
sleep 5

# 健康状態チェック
curl http://localhost:8000/api/health

# レート制限チェック
curl http://localhost:8000/api/check-limit

# サーバー停止
pkill -f "magicboxai.main"
```

Windows PowerShell:

```powershell
# サーバーバックグラウンド起動
Start-Process python -ArgumentList "-m magicboxai.main" -WindowStyle Hidden

Start-Sleep -Seconds 5

# ヘルスチェック
Invoke-WebRequest http://localhost:8000/api/health

# レート制限チェック
Invoke-WebRequest http://localhost:8000/api/check-limit

# 停止
Get-Process python | Where-Object {$_.CommandLine -like "*magicboxai*"} | Stop-Process
```

期待結果：
- ✅ `/api/health` → `{"status": "ok"}`
- ✅ `/api/check-limit` → `{"allowed": true, "count": 0, ...}`

検証ログを `results/codex/API_VERIFICATION.md` に保存してください。

---

### Task 6: 動作確認レポート作成

`results/codex/MAGICBOXAI_READY_CHECK.md` を作成してください：

```markdown
# MagicBoxAI MVP - 動作確認レポート

## 実行日時
[実行日時]

## チェック結果

### 1. 依存関係インストール
- [ ] 成功
- [ ] 失敗：[理由]

### 2. ユニットテスト
- [ ] 全て PASS
- [ ] 一部失敗：[テスト名]
- テスト数：[N個]
- 成功：[N個]

### 3. データベース初期化
- [ ] 成功（magicboxai.db 作成）
- [ ] 失敗：[理由]
- [ ] テーブル確認：files, track_limit_daily, promo_codes

### 4. アプリ起動
- [ ] 成功（ポート 8000 バインド）
- [ ] 失敗：[理由]
- [ ] エラーログ：[有/無]

### 5. API 検証
- [ ] /api/health - OK
- [ ] /api/check-limit - OK
- [ ] その他エンドポイント確認

## 結論

MagicBoxAI MVP は **[本番準備完了 / テスト必要 / 修正必要]** です。

## 次のステップ

- [ ] Docker コンテナ化
- [ ] 本番デプロイ
- [ ] ユーザーテスト
```

---

## ✅ 成功基準

すべてが以下で確認されること：

- ✅ `requirements.txt` インストール成功
- ✅ ユニットテスト実行（結果を記録）
- ✅ データベース初期化成功
- ✅ アプリ起動成功（10秒以上稼働）
- ✅ API エンドポイント応答確認
- ✅ すべてのログファイルが results/codex に保存されている

---

## 📝 出力ファイル

実行後、以下が GitHub に push されること：

```
results/codex/
├── MAGICBOXAI_TEST_RESULTS.md
├── DB_INIT_LOG.md
├── APP_STARTUP_LOG.md
├── API_VERIFICATION.md
├── MAGICBOXAI_READY_CHECK.md
├── error.log（エラーがあれば）
└── execution_*.log（実行ログ）
```

---

## 🎯 最後のステップ

全て完了したら、git commit & push:

```bash
git add .
git commit -m "[feat] MagicBoxAI MVP - 完全動作確認完了

- requirements.txt インストール
- ユニットテスト実行・記録
- データベース初期化
- アプリケーション起動検証
- API エンドポイント確認
- 本番準備状況レポート"
git push origin main
```

---

**Status**: 実行準備完了
**ユーザーアクション**: なし（Codex が全部やります）
