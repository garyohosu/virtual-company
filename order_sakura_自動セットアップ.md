# Order - Sakura FreeBSD 自動セットアップ（Codex が SSH で実行）

**Status**: ⏳ セットアップ待ち
**Current Actor**: Codex CLI（SSH 経由）
**Next Actor**: CEO（note 記事執筆）

---

## 🎯 ミッション

Codex が **SSH で Sakura サーバーに接続**して、
MagicBoxAI のセットアップをすべて自動実行します。

**前提条件**: GitHub SSH キーはすでに登録済み（CEO が手作業完了）

---

## 📋 実行内容

Codex は以下を SSH 経由で Sakura サーバー上で実行：

### Step 1: Python 仮想環境作成

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/magic-box-ai

# Python 仮想環境作成
python3 -m venv venv

# 仮想環境有効化
source venv/bin/activate

# 確認
which python
# /home/garyo/magic-box-ai/venv/bin/python

EOFSH
```

### Step 2: 依存関係インストール

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/magic-box-ai
source venv/bin/activate

# pip アップグレード
pip install --upgrade pip

# 依存関係インストール
pip install -r requirements.txt

# インストール確認
pip list | grep fastapi

EOFSH
```

### Step 3: データベース初期化

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

### Step 4: テスト実行

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/magic-box-ai
source venv/bin/activate

# ユニットテスト実行
python3 -m pytest tests/ -v

# テスト結果を保存
python3 -m pytest tests/ -v > test_results.txt 2>&1

EOFSH
```

### Step 5: Gunicorn インストール

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/magic-box-ai
source venv/bin/activate

# Gunicorn インストール
pip install gunicorn

# インストール確認
pip list | grep gunicorn

EOFSH
```

### Step 6: Gunicorn テスト起動（5 秒）

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/magic-box-ai
source venv/bin/activate

# バックグラウンドで 5 秒間起動
timeout 5 gunicorn \
  --workers 2 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 127.0.0.1:8000 \
  magicboxai.main:app || true

EOFSH
```

### Step 7: 完了確認・レポート作成

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/magic-box-ai

# セットアップ完了確認
cat > SETUP_COMPLETE.txt << 'EOF'
✅ MagicBoxAI Sakura FreeBSD Setup Complete

Date: $(date)
Host: $(hostname)
OS: $(uname -a)
Python: $(python3 --version)

Venv: ~/magic-box-ai/venv
DB: ~/magic-box-ai/magicboxai.db

Ready for:
1. Gunicorn + Nginx 設定
2. SSL 証明書設定
3. 本番デプロイ
EOF

cat SETUP_COMPLETE.txt

EOFSH
```

---

## 📊 出力結果

Codex は以下をローカルに保存：

```
results/codex/
├── SAKURA_SETUP_COMPLETE.md
├── test_results.txt
├── setup_log.txt
└── EXECUTION_LOG.md
```

---

## ✅ 成功基準

すべてが達成されること：

- ✅ SSH 接続成功（パスワード不要）
- ✅ Python 仮想環境作成
- ✅ 依存関係インストール完了
- ✅ DB 初期化完了
- ✅ pytest テスト実行（結果を記録）
- ✅ Gunicorn インストール完了
- ✅ Gunicorn テスト起動成功
- ✅ セットアップ完了確認
- ✅ すべてのログが GitHub に記録

---

## 🎯 次のステップ

セットアップ完了後：

```bash
git pull
codex --yolo order_sakura_gunicorn_nginx.md を実行
```

Codex が Gunicorn + Nginx + SSL 設定を自動実行。

---

## 💡 このシステムの素晴らしさ

```
CEO（あなた）: GitHub SSH キー登録（1 回だけ手作業）
Codex: その後、すべての技術的な作業を自動実行

結果：
- Sakura サーバー側の操作: 0（Codex が全部）
- あなたの仕事: 最小限
- 再現可能: 同じ order ファイルで何度でも実行可能
- 監査可能: すべてのログが GitHub に記録
```

これが **真の自動化** です。 ✨

---

**Status**: Codex による完全自動セットアップ準備完了
