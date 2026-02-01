# 🚨 CRITICAL FIX: Sakura デプロイパスの修正

## 📋 基本情報
- **機能名**: Sakura デプロイパス修正
- **プロジェクト**: magic-box-ai
- **作成日**: 2026-02-01
- **対象リポジトリ**: garyohosu/magic-box-ai
- **対象AI**: Gemini CLI
- **優先度**: 🔴 CRITICAL - IMMEDIATE

---

## 🎯 問題の発見

### ユーザー報告
本番環境（https://garyo.sakura.ne.jp/magicboxai/）で古いコンテンツ（オセロゲーム）が表示されている。

### 根本原因
**デプロイ先のパスが間違っていた！**

```
❌ 間違ったパス（現在）:
~/public_html/magicboxai/src/

✅ 正しいパス:
/home/garyo/www/magicboxai/
```

ファイルは間違ったディレクトリにデプロイされており、本番環境には反映されていなかった。

---

## 📝 実装手順

### Step 1: magic-box-ai リポジトリの準備

```bash
cd ~/garyohosu
git clone https://github.com/garyohosu/magic-box-ai.git || true
cd magic-box-ai
git checkout main
git pull origin main
```

### Step 2: deploy.yml の修正

```bash
cd ~/garyohosu/magic-box-ai

# deploy.yml を修正
cat > .github/workflows/deploy.yml << 'EOF'
name: Deploy to Sakura

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Setup PHP
      uses: shivammathur/setup-php@v2
      with:
        php-version: 7.4
        tools: composer:v2
    - name: Install dependencies
      run: composer install
    - name: Run tests
      run: ./vendor/bin/phpunit tests/Unit

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to Sakura
      env:
        SAKURA_USER: ${{ secrets.SAKURA_USER }}
        SAKURA_SSH_KEY: ${{ secrets.SAKURA_SSH_KEY }}
      run: |
        # Setup SSH
        mkdir -p ~/.ssh
        echo "$SAKURA_SSH_KEY" > ~/.ssh/sakura_key
        chmod 600 ~/.ssh/sakura_key
        
        # Test SSH connection
        ssh -i ~/.ssh/sakura_key -o StrictHostKeyChecking=no ${SAKURA_USER}@garyo.sakura.ne.jp "echo 'SSH connection OK'"
        
        # Deploy files using rsync - CORRECT PATH!
        rsync -avz --delete \
          -e "ssh -i ~/.ssh/sakura_key -o StrictHostKeyChecking=no" \
          --exclude='.git' \
          --exclude='.github' \
          --exclude='tests' \
          --exclude='vendor' \
          --exclude='composer.lock' \
          --exclude='README.md' \
          --exclude='.gitignore' \
          src/ ${SAKURA_USER}@garyo.sakura.ne.jp:/home/garyo/www/magicboxai/
        
        # Verify deployment - CORRECT PATH!
        ssh -i ~/.ssh/sakura_key -o StrictHostKeyChecking=no ${SAKURA_USER}@garyo.sakura.ne.jp "ls -la /home/garyo/www/magicboxai/"
EOF

echo "✅ deploy.yml updated with correct path"
```

### Step 3: Git コミット＆プッシュ

```bash
cd ~/garyohosu/magic-box-ai

# 変更を確認
git diff .github/workflows/deploy.yml

# ステージング
git add .github/workflows/deploy.yml

# コミット
git commit -m "fix: Correct Sakura deployment path to /home/garyo/www/magicboxai/

CRITICAL FIX: Deployment path was incorrect!

Wrong path:
~/public_html/magicboxai/src/

Correct path:
/home/garyo/www/magicboxai/

This is why the production site was showing old content (Othello game).
Files were being deployed to the wrong directory.

This fix will deploy files to the correct location."

# プッシュ
git push origin main

echo "✅ Changes pushed to GitHub - GitHub Actions will deploy to correct path"
```

### Step 4: 即座に手動デプロイを実行（GitHub Actions を待たない）

```bash
cd ~/garyohosu/magic-box-ai

echo "=== Immediate manual deployment to correct path ==="

# SSH 秘密鍵のパスを確認
SSH_KEY_PATH="$HOME/.ssh/id_rsa"
if [ ! -f "$SSH_KEY_PATH" ]; then
  SSH_KEY_PATH="$HOME/.ssh/id_ed25519"
fi

if [ -f "$SSH_KEY_PATH" ]; then
  echo "Using SSH key: $SSH_KEY_PATH"
  
  # 正しいパスにデプロイ
  rsync -avz --delete \
    -e "ssh -i $SSH_KEY_PATH -o StrictHostKeyChecking=no" \
    --exclude='.git' \
    --exclude='.github' \
    --exclude='tests' \
    --exclude='vendor' \
    --exclude='composer.lock' \
    --exclude='README.md' \
    --exclude='.gitignore' \
    src/ garyo@garyo.sakura.ne.jp:/home/garyo/www/magicboxai/
  
  echo "✅ Manual deployment completed to /home/garyo/www/magicboxai/"
  
  # デプロイ後の確認
  echo ""
  echo "=== Verification ==="
  ssh -i $SSH_KEY_PATH garyo@garyo.sakura.ne.jp "ls -la /home/garyo/www/magicboxai/"
  
  echo ""
  echo "=== File count ==="
  ssh -i $SSH_KEY_PATH garyo@garyo.sakura.ne.jp "find /home/garyo/www/magicboxai/ -type f | wc -l"
  
  echo ""
  echo "=== home.php check ==="
  ssh -i $SSH_KEY_PATH garyo@garyo.sakura.ne.jp "ls -lh /home/garyo/www/magicboxai/pages/home.php"
  ssh -i $SSH_KEY_PATH garyo@garyo.sakura.ne.jp "grep -c 'Example Prompts' /home/garyo/www/magicboxai/pages/home.php"
else
  echo "⚠️ SSH key not found at $HOME/.ssh/id_rsa or $HOME/.ssh/id_ed25519"
  echo "Please run manual deployment with your SSH key"
fi
```

---

## ✅ 検証項目

### 1. デプロイパスの確認
- [ ] deploy.yml が正しいパスに修正されている
- [ ] `/home/garyo/www/magicboxai/` に変更されている
- [ ] Git コミット＆プッシュが成功している

### 2. 手動デプロイの確認
- [ ] rsync が成功している
- [ ] ファイルが `/home/garyo/www/magicboxai/` に存在する
- [ ] home.php に "Example Prompts" が含まれている

### 3. 本番環境の確認
- [ ] https://garyo.sakura.ne.jp/magicboxai/ にアクセス
- [ ] **Example Prompts が 8 個表示される**
- [ ] **オセロゲームが表示されない**
- [ ] ボタンが正常に表示される
- [ ] JavaScript が正常に動作する

---

## 📊 期待される結果

### Before（現在）
```
❌ 本番環境: オセロゲーム表示
❌ デプロイ先: ~/public_html/magicboxai/src/ (間違い)
❌ 本番サイト: 古いコンテンツ
```

### After（修正後）
```
✅ 本番環境: Example Prompts 表示
✅ デプロイ先: /home/garyo/www/magicboxai/ (正しい)
✅ 本番サイト: 新しいコンテンツ
```

---

## 🚀 実行後の確認

### 1. ブラウザで確認
https://garyo.sakura.ne.jp/magicboxai/

**強制リロード**: `Ctrl + F5` (Windows) / `Cmd + Shift + R` (Mac)

### 2. 確認項目
- [ ] Example Prompts が 8 個表示される
- [ ] MagicBoxAI のロゴが表示される
- [ ] Tailwind CSS のスタイルが適用される
- [ ] Alpine.js が動作する
- [ ] オセロゲームは表示されない

---

## 📝 次のアクション

1. この指示書を Gemini CLI で実行
   ```bash
   cd ~/garyohosu/virtual-company
   ./scripts/gemini_wrapper.sh instructions/fix_sakura_deployment_path_20260201.md
   ```

2. 実行結果を確認
   ```bash
   cat results/gemini/2026-02-01_*_fix_sakura_deployment_path_20260201.md
   ```

3. 本番環境を確認
   https://garyo.sakura.ne.jp/magicboxai/

4. ブラウザで強制リロード（Ctrl+F5）

---

## 📌 Status

- **Current**: 指示書作成完了
- **Next**: Gemini CLI で即座に実行
- **Priority**: 🔴 CRITICAL - すぐに実行してください
- **Created At**: 2026-02-01

---

**この指示書を Gemini CLI で実行すれば、デプロイパスが修正され、本番環境に正しいコンテンツがデプロイされます！**

**手動デプロイも同時に実行されるため、GitHub Actions を待たずに即座に本番環境が更新されます！**
