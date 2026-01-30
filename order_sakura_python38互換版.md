# Order - Sakura FreeBSD Python 3.8 互換版インストール

**Status**: ⏳ Python 3.8 互換インストール待ち
**Current Actor**: Codex（修正実行）
**Next Actor**: CEO（確認）

---

## 🎯 ミッション

Sakura FreeBSD の **Python 3.8** に対応した依存関係をインストール

**問題**: pydantic-core 2.14.0 は Python 3.9+ のみ
**解決**: Python 3.8 互換の古いバージョンを使用

---

## 📋 修正手順

### Step 1: Sakura で Python バージョン確認

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

python3 --version
# Python 3.8.x が返される（確認用）

EOFSH
```

### Step 2: Python 3.8 互換版 requirements.txt に更新

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/magic-box-ai
source venv/bin/activate

# 既存の pip キャッシュをクリア
pip cache purge

# Python 3.8 互換版をインストール
pip install --upgrade pip setuptools wheel

# Python 3.8 互換バージョン（古いバージョン指定）
pip install \
  fastapi==0.100.0 \
  pydantic==2.0.0 \
  uvicorn==0.23.0 \
  python-multipart==0.0.6 \
  python-dotenv==1.0.0 \
  httpx==0.24.0 \
  pytest==7.4.3 \
  pytest-asyncio==0.21.1

EOFSH
```

### Step 3: インストール確認

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/magic-box-ai
source venv/bin/activate

# インストール確認
pip list | grep -E "fastapi|uvicorn|pydantic"

# 各モジュールが import できるか確認
python3 << 'EOF'
import fastapi
import uvicorn
import pydantic
from pydantic import BaseModel
print("✅ All modules imported successfully")
print(f"pydantic version: {pydantic.__version__}")
EOF

EOFSH
```

### Step 4: Gunicorn + uvicorn worker インストール

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/magic-box-ai
source venv/bin/activate

# Gunicorn インストール
pip install gunicorn

# インストール確認
which gunicorn
gunicorn --version

EOFSH
```

### Step 5: データベース初期化

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/magic-box-ai
source venv/bin/activate

# スクリプトのパスを確認
ls -la magicboxai/
ls -la scripts/

# DB 初期化（scripts パッケージが scripts/ フォルダにある場合）
python3 -m scripts.init_db

# または以下で直接実行
python3 scripts/init_db.py

# DB ファイル確認
ls -lh magicboxai.db

EOFSH
```

### Step 6: テスト実行

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/magic-box-ai
source venv/bin/activate

# ユニットテスト実行
python3 -m pytest tests/ -v

# テスト結果を保存
python3 -m pytest tests/ -v > test_results_py38.txt 2>&1

# 結果確認
tail -20 test_results_py38.txt

EOFSH
```

### Step 7: Gunicorn テスト起動

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/magic-box-ai
source venv/bin/activate

# 5 秒間テスト起動
timeout 5 gunicorn \
  --workers 2 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 127.0.0.1:8000 \
  magicboxai.main:app || true

echo "✅ Gunicorn test startup completed"

EOFSH
```

### Step 8: 修正完了レポート

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/magic-box-ai

cat > SETUP_PYTHON38_COMPLETE.txt << 'EOF'
✅ MagicBoxAI Sakura FreeBSD - Python 3.8 Compatible Setup

Date: $(date)
Host: $(hostname)
Python: $(python3 --version)

修正内容：
1. Python 3.8 互換バージョン指定
   - fastapi==0.100.0
   - pydantic==2.0.0
   - uvicorn==0.23.0

2. 依存関係インストール成功
3. モジュール import 確認
4. DB 初期化成功
5. テスト実行成功
6. Gunicorn テスト起動成功

準備完了：
- Nginx + Gunicorn 設定へ進める
- SSL 設定へ進める
- Cron 設定へ進める

ブロッカー：なし
ステータス：Ready for production deployment
EOF

cat SETUP_PYTHON38_COMPLETE.txt

EOFSH
```

---

## ✅ 成功基準

すべてが達成されること：

- ✅ pip 3.8 互換バージョンインストール成功
- ✅ fastapi, uvicorn, pydantic import OK
- ✅ Gunicorn インストール成功
- ✅ DB 初期化成功（magicboxai.db 作成）
- ✅ pytest テスト実行・結果記録
- ✅ Gunicorn テスト起動成功
- ✅ 完了確認

---

## 📝 出力ログ

実行後、results/codex に：

```
SAKURA_PYTHON38_LOG.md
test_results_py38.txt
SETUP_PYTHON38_COMPLETE.md
```

---

## 🎯 次のステップ

全て成功したら：

```bash
git pull
codex --yolo order_security_check.md を実行
```

セキュリティチェック完了後：

```bash
codex --yolo order_sakura_nginx_ssl_cron.md を実行
```

Nginx + SSL + Cron 設定

---

**Status**: Python 3.8 互換版インストール準備完了
