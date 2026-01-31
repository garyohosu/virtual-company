# Order - GitHub Actions CI/CD 構築

**Status**: ⏳ CI/CD 実装待ち
**Current Actor**: Claude / Gemini
**Goal**: コード変更時に自動テスト・デプロイを実行
**Output**: `.github/workflows/ci.yml` + ドキュメント

---

## 🎯 ミッション

push するだけで、自動的に：

1. ✅ ローカル環境でテスト実行
2. ✅ 成功したら Sakura にデプロイ
3. ✅ 本番環境で動作確認
4. ✅ 失敗時は通知

---

## 📋 実装内容

### 1. ワークフローファイル作成

`.github/workflows/ci.yml`:

```yaml
name: MagicBoxAI CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      # リポジトリをチェックアウト
      - uses: actions/checkout@v3
      
      # Python 3.12 をセットアップ
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      # 依存関係をインストール
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      # ローカルテスト実行
      - name: Run pytest (Local)
        run: |
          python -m pytest tests/test_magicboxai_api.py -v
      
      # テスト成功時だけデプロイ
      - name: Deploy to Sakura Server
        if: success()
        env:
          SAKURA_SSH_KEY: ${{ secrets.SAKURA_SSH_KEY }}
          SAKURA_USER: ${{ secrets.SAKURA_USER }}
          SAKURA_HOST: garyo.sakura.ne.jp
        run: |
          # SSH キーをセットアップ
          mkdir -p ~/.ssh
          echo "$SAKURA_SSH_KEY" > ~/.ssh/sakura_key
          chmod 600 ~/.ssh/sakura_key
          
          # PHP ファイルをデプロイ
          echo "🚀 Deploying to Sakura..."
          scp -i ~/.ssh/sakura_key -o StrictHostKeyChecking=no \
            -r magicboxai/php/* \
            $SAKURA_USER@$SAKURA_HOST:~/www/magicboxai/
          
          echo "✅ Deployment complete"
      
      # 本番環境で健康診断
      - name: Smoke Test (Production)
        if: success()
        run: |
          echo "🔍 Running production health check..."
          
          # API ヘルスチェック
          RESPONSE=$(curl -s https://garyo.sakura.ne.jp/magicboxai/index.php/api/health)
          
          if echo "$RESPONSE" | grep -q "ok"; then
            echo "✅ Production health check passed"
            echo "$RESPONSE"
          else
            echo "❌ Production health check failed"
            echo "$RESPONSE"
            exit 1
          fi
      
      # 失敗時の通知
      - name: Notify on Failure
        if: failure()
        run: |
          echo "❌ CI/CD Pipeline failed"
          echo "Check the logs above for details"
```

---

## 🔐 GitHub Secrets の設定

### Step 1: SSH キーを生成（Windows PowerShell）

```powershell
# Sakura サーバーにすでにアクセスできる場合、既存キーを使用
# ~/.ssh/id_rsa を GitHub に登録

# または新規生成
ssh-keygen -t rsa -b 4096 -f sakura_key -N ""

# 公開鍵を Sakura に登録
cat sakura_key.pub | ssh garyo@garyo.sakura.ne.jp "cat >> ~/.ssh/authorized_keys"
```

### Step 2: GitHub に秘密鍵を登録

```
GitHub → Settings → Secrets and variables → New repository secret

Name: SAKURA_SSH_KEY
Value: (sakura_key の内容を貼り付け)
```

### Step 3: ユーザー名も登録

```
Name: SAKURA_USER
Value: garyo
```

---

## 🚀 使い方

### コード変更時の自動実行

```bash
# 1. ローカルでコード変更
vi magicboxai/php/index.php

# 2. commit & push
git add .
git commit -m "fix: Update routing logic"
git push origin main

# 3. GitHub Actions が自動実行
   - pytest でテスト
   - 成功したら Sakura にデプロイ
   - 本番環境でヘルスチェック
```

---

## 📊 ワークフロー図

```
push
  ↓
GitHub Actions 起動
  ├─ pytest 実行
  │  ├─ 失敗 → 通知・終了
  │  └─ 成功 ↓
  ├─ Sakura にデプロイ
  │  └─ scp で PHP ファイル転送
  ├─ 本番環境テスト
  │  ├─ /api/health にアクセス
  │  ├─ 失敗 → ロールバック通知
  │  └─ 成功 ↓
  └─ ✅ 完了・通知
```

---

## ✅ 成功基準

- ✅ `.github/workflows/ci.yml` が作成される
- ✅ SAKURA_SSH_KEY を GitHub Secrets に登録
- ✅ push 時に自動テスト実行
- ✅ テスト成功時に Sakura に自動デプロイ
- ✅ 本番環境でのヘルスチェックが実行される

---

## 🎓 このワークフローのメリット

```
✅ 開発者負担ゼロ
   push するだけで自動化

✅ バグが本番に行かない
   ローカルテスト + 本番テストで二重チェック

✅ デプロイミス防止
   手動デプロイではなく自動化

✅ 変更履歴が自動記録
   GitHub Actions ログで何をしたか可視化
```

---

**Status**: CI/CD 実装待ち

これで、コード変更 → 自動テスト → 自動デプロイが完全に自動化されます！
