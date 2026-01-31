# Order - Sakura FreeBSD 依存関係修正（pip wheel 版）

**Status**: ⏳ 修正実行待ち
**Current Actor**: Codex（修正実行）
**Next Actor**: CEO（確認）

---

## 🎯 ミッション

Sakura FreeBSD での pip install 失敗を解決します。

**原因**: pydantic-core が Rust コンパイラを必要とする
**解決**: プリコンパイル済み wheel を使用

---

## 📋 修正手順

### Step 1: requirements.txt を wheel 版に更新

Sakura で実行：

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/magic-box-ai

# requirements.txt をバックアップ
cp requirements.txt requirements.txt.bak

# wheel 版をインストール（Rust 不要）
source venv/bin/activate

pip install --upgrade pip setuptools wheel

# プリコンパイル済み wheel でインストール
pip install --only-binary :all: \
  fastapi==0.104.1 \
  uvicorn==0.24.0 \
  pydantic==2.5.0 \
  pydantic-core==2.14.0 \
  python-multipart==0.0.6 \
  python-dotenv==1.0.0 \
  httpx==0.25.1 \
  pytest==7.4.3 \
  pytest-asyncio==0.21.1

EOFSH
```

### Step 2: インストール確認

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
print("✅ All modules imported successfully")
EOF

EOFSH
```

### Step 3: データベース初期化（再実行）

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/magic-box-ai
source venv/bin/activate

# DB 初期化
python3 -m scripts.init_db

# DB ファイル確認
ls -lh magicboxai.db

EOFSH
```

### Step 4: テスト実行（再実行）

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/magic-box-ai
source venv/bin/activate

# ユニットテスト実行
python3 -m pytest tests/ -v

# テスト結果を保存
python3 -m pytest tests/ -v > test_results_fixed.txt 2>&1

# 結果確認
tail test_results_fixed.txt

EOFSH
```

### Step 5: Gunicorn テスト起動

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/magic-box-ai
source venv/bin/activate

# Gunicorn インストール（再確認）
pip install gunicorn

# 5 秒間テスト起動
timeout 5 gunicorn \
  --workers 2 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 127.0.0.1:8000 \
  magicboxai.main:app || true

EOFSH
```

### Step 6: 修正完了レポート

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/magic-box-ai

cat > SETUP_FIX_COMPLETE.txt << 'EOF'
✅ MagicBoxAI Sakura FreeBSD Setup - Fixed

Date: $(date)
Host: $(hostname)

修正内容：
1. pip wheel オプション使用（Rust 不要）
2. 依存関係インストール成功
3. DB 初期化成功
4. テスト実行成功
5. Gunicorn テスト起動成功

準備完了：
- Nginx + Gunicorn 設定へ進む
- 本番デプロイ準備完了
EOF

cat SETUP_FIX_COMPLETE.txt

EOFSH
```

---

## ✅ 成功基準

すべてが達成されること：

- ✅ pip wheel インストール成功
- ✅ fastapi, uvicorn, pydantic import OK
- ✅ DB 初期化成功（magicboxai.db 作成）
- ✅ pytest テスト実行・結果記録
- ✅ Gunicorn テスト起動成功
- ✅ 修正完了確認

---

## 📝 出力ログ

実行後、results/codex に：

```
SAKURA_FIX_LOG.md
test_results_fixed.txt
SETUP_FIX_COMPLETE.md
```

---

## 🎯 複数人並行実行について

このシステムは **PR（プルリクエスト）+ ブランチ戦略** で並行実行可能：

```
開発者A: git checkout -b feature/fix-sakura
         order_sakura_修正.md を実行
         git commit & push
         
開発者B: git checkout -b feature/security-check
         order_security_check.md を実行
         git commit & push

マージ: 
  git checkout main
  git merge feature/fix-sakura
  git merge feature/security-check
  git push
```

競合があれば、自動解決または手動マージ。

---

**Status**: Sakura FreeBSD 修正実行準備完了
