# 指示書: GitHub Actions ワークフローの BOM 削除とデプロイ修正

## 📋 基本情報
- **機能名**: GitHub Actions ワークフロー修正
- **プロジェクト**: magic-box-ai
- **作成日**: 2026-02-01
- **対象リポジトリ**: garyohosu/magic-box-ai
- **対象AI**: Gemini CLI
- **優先度**: 🔴 CRITICAL

---

## 🎯 実行内容

### 概要
GitHub Actions でエラーが発生している。3つのワークフローファイルに UTF-8 BOM が含まれており、さらに deploy.yml の実装が不完全。これらを修正する。

### 背景
- スクリーンショットで確認: Deploy to Sakura と PHPUnit Tests が失敗
- 原因 1: `.github/workflows/*.yml` に BOM が含まれている
- 原因 2: `deploy.yml` がファイルをサーバーにアップロードしていない

---

## 📝 実装手順

### Step 1: リポジトリの確認とクローン

```bash
# magic-box-ai リポジトリをクローン（まだの場合）
cd ~/garyohosu
git clone https://github.com/garyohosu/magic-box-ai.git || true
cd magic-box-ai

# 最新の状態に更新
git checkout main
git pull origin main
```

### Step 2: BOM の検出と削除

```bash
cd ~/garyohosu/magic-box-ai

# すべてのワークフローファイルから BOM を削除
for file in .github/workflows/*.yml; do
  echo "Processing $file"
  # BOM (EF BB BF) を削除
  if [ -f "$file" ]; then
    # Linux/macOS 両対応
    sed -i.bak '1s/^\xEF\xBB\xBF//' "$file" 2>/dev/null || \
    LC_ALL=C sed -i '' '1s/^\xEF\xBB\xBF//' "$file" 2>/dev/null || \
    perl -pi -e 's/^\xEF\xBB\xBF//' "$file"
    rm -f "$file.bak"
  fi
done

# 確認: BOM がないことを確認
for file in .github/workflows/*.yml; do
  echo "=== $file ==="
  head -1 "$file"
  # BOM があれば警告
  if head -c 3 "$file" | od -An -tx1 | grep -q "ef bb bf"; then
    echo "⚠️ BOM still exists!"
  else
    echo "✅ No BOM"
  fi
done
```

### Step 3: deploy.yml を完全版に置き換え

```bash
cd ~/garyohosu/magic-box-ai

# deploy.yml を完全版に置き換え
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
        
        # Deploy files using rsync
        rsync -avz --delete \
          -e "ssh -i ~/.ssh/sakura_key -o StrictHostKeyChecking=no" \
          --exclude='.git' \
          --exclude='.github' \
          --exclude='tests' \
          --exclude='vendor' \
          --exclude='composer.lock' \
          --exclude='README.md' \
          --exclude='.gitignore' \
          src/ ${SAKURA_USER}@garyo.sakura.ne.jp:~/public_html/magicboxai/src/
        
        # Verify deployment
        ssh -i ~/.ssh/sakura_key -o StrictHostKeyChecking=no ${SAKURA_USER}@garyo.sakura.ne.jp "ls -la ~/public_html/magicboxai/src/"
EOF

# BOM がないことを確認
if head -c 3 .github/workflows/deploy.yml | od -An -tx1 | grep -q "ef bb bf"; then
  echo "⚠️ BOM detected in deploy.yml! Removing..."
  sed -i '1s/^\xEF\xBB\xBF//' .github/workflows/deploy.yml
fi

echo "✅ deploy.yml updated"
```

### Step 4: 変更を確認

```bash
cd ~/garyohosu/magic-box-ai

# 変更されたファイルを確認
git status

# 差分を確認
git diff .github/workflows/

# 各ファイルの先頭行を確認（BOM がないこと）
for file in .github/workflows/*.yml; do
  echo "=== $file ==="
  head -3 "$file"
  echo ""
done
```

### Step 5: Git コミット＆プッシュ

```bash
cd ~/garyohosu/magic-box-ai

# 変更をステージング
git add .github/workflows/

# コミット
git commit -m "fix: Remove UTF-8 BOM from GitHub Actions workflows and fix deployment

Critical fixes:
- Removed UTF-8 BOM from all workflow files (.github/workflows/*.yml)
- Fixed deploy.yml to actually deploy files using rsync
- Changed SAKURA_KEY to SAKURA_SSH_KEY (correct secret name)
- Added SSH connection test
- Added rsync deployment with proper excludes
- Added deployment verification

BOM in workflow files was causing:
❌ GitHub Actions parsing errors
❌ Workflow execution failures

Missing deployment logic was causing:
❌ Files not being uploaded to server
❌ Production environment not being updated

This should fix all GitHub Actions errors."

# プッシュ
git push origin main

echo "✅ Changes pushed to GitHub"
```

### Step 6: GitHub Actions の実行を確認

```bash
# GitHub Actions のステータスを確認（gh コマンドが使える場合）
cd ~/garyohosu/magic-box-ai
gh run list --limit 5 || echo "gh command not available. Please check manually: https://github.com/garyohosu/magic-box-ai/actions"
```

---

## ✅ 検証項目

### 1. ローカルでの確認
- [ ] 3つのワークフローファイルから BOM が削除されている
- [ ] deploy.yml が完全版に置き換えられている
- [ ] Git コミット＆プッシュが成功している

### 2. GitHub Actions の確認
- [ ] Test PHPUnit が成功（緑色）
- [ ] Test Pytest が成功（緑色）
- [ ] Deploy to Sakura が成功（緑色）

### 3. デプロイログの確認
Deploy to Sakura のログで以下を確認：
```
✅ SSH connection OK
✅ sending incremental file list
✅ src/index.php
✅ src/cron_cleanup.php
✅ src/pages/home.php
```

### 4. 本番環境の確認
- [ ] https://garyo.sakura.ne.jp/magicboxai/ にアクセス
- [ ] Example Prompts が 8 個表示される
- [ ] ボタンが正常に表示される
- [ ] JavaScript が正常に動作する
- [ ] 404 エラーが出ていない

---

## 🚫 注意事項

### BOM について
- BOM (Byte Order Mark) は UTF-8 ファイルの先頭に付加される `EF BB BF`
- YAML パーサーが BOM を認識できず、エラーになる
- 必ず削除すること

### deploy.yml について
- 元の実装は SSH 接続のテストだけで、ファイルをアップロードしていなかった
- 新しい実装は rsync でファイルをサーバーにアップロードする
- `SAKURA_KEY` → `SAKURA_SSH_KEY` に変更（GitHub Secrets の名前に合わせる）

### rsync について
- `--delete` オプション: サーバー上の余分なファイルを削除
- `--exclude`: 不要なファイル（.git, tests, vendor など）を除外
- `src/` → `~/public_html/magicboxai/src/`: src ディレクトリの内容をサーバーにコピー

---

## 📊 期待される結果

### Before（現在）
```
❌ Deploy to Sakura - Failed
❌ PHPUnit Tests - Failed
✅ pytest Integration Tests - Success
```

### After（修正後）
```
✅ Deploy to Sakura - Success
✅ PHPUnit Tests - Success
✅ pytest Integration Tests - Success
```

### 本番環境
- ✅ ファイルが自動的にサーバーにアップロードされる
- ✅ Example Prompts が正常に表示される
- ✅ JavaScript が正常に動作する
- ✅ 404 エラーが解消される

---

## 🔗 関連リソース

- **GitHub Actions**: https://github.com/garyohosu/magic-box-ai/actions
- **Production URL**: https://garyo.sakura.ne.jp/magicboxai/
- **修正マニュアル**: https://github.com/garyohosu/virtual-company/blob/main/results/genspark/2026-02-01_GITHUB_ACTIONS_WORKFLOW_FIXES.md

---

## 📝 次のアクション

1. この指示書を Gemini CLI で実行
   ```bash
   cd ~/garyohosu/virtual-company
   ./scripts/gemini_wrapper.sh instructions/fix_github_actions_workflows_bom_20260201.md
   ```

2. 実行結果を確認
   ```bash
   cat results/gemini/2026-02-01_*_fix_github_actions_workflows_bom_20260201.md
   ```

3. GitHub Actions の実行状況を確認
   https://github.com/garyohosu/magic-box-ai/actions

4. 本番環境で動作を確認
   https://garyo.sakura.ne.jp/magicboxai/

---

## 📌 Status

- **Current**: 指示書作成完了
- **Next**: Gemini CLI で実行
- **Created At**: 2026-02-01

---

**この指示書を Gemini CLI で実行すれば、GitHub Actions のエラーが修正され、本番環境に自動デプロイされます！**
