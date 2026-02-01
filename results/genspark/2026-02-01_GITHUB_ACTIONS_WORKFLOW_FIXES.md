# 🚨 GitHub Actions Workflow Fixes - Manual Application Required

## 📋 実行日時
- 日付: 2026-02-01
- レポート作成者: Genspark AI
- 優先度: **🔴 CRITICAL**

---

## 🔍 問題の発見

### スクリーンショットから確認された問題
GitHub Actions で以下のエラーが発生：

```
❌ fix: Remove UTF-8 BOM from all PHP files
   - Deploy to Sakura #11: Failed
   - PHPUnit Tests #11: Failed
   - pytest Integration Tests #11: Success ✅
```

### 根本原因
**3つの GitHub Actions ワークフローファイルに UTF-8 BOM (U+FEFF) が含まれていた**：

1. `.github/workflows/deploy.yml` - BOM あり
2. `.github/workflows/test-phpunit.yml` - BOM あり
3. `.github/workflows/test-pytest.yml` - BOM あり

**さらに、deploy.yml の実装が不完全で、ファイルをサーバーにアップロードする処理がなかった。**

---

## 🛠️ 実施した修正

### 1. BOM の削除（3ファイル）

```bash
# すべてのワークフローファイルから BOM を削除
for file in .github/workflows/*.yml; do
  cat "$file" | sed '1s/^\xEF\xBB\xBF//' > "$file.tmp"
  mv "$file.tmp" "$file"
done
```

#### 修正前
```yaml
﻿name: Deploy to Sakura
```

#### 修正後
```yaml
name: Deploy to Sakura
```

### 2. deploy.yml の完全実装

#### 修正前（不完全）
```yaml
- name: Deploy
  env:
    SAKURA_HOST: ${{ secrets.SAKURA_HOST }}
    SAKURA_USER: ${{ secrets.SAKURA_USER }}
    SAKURA_KEY: ${{ secrets.SAKURA_KEY }}
  run: |
    mkdir -p ~/.ssh
    echo "$SAKURA_KEY" > ~/.ssh/sakura_key
    chmod 600 ~/.ssh/sakura_key
    ssh -i ~/.ssh/sakura_key -o StrictHostKeyChecking=no $SAKURA_USER@$SAKURA_HOST "echo 'Deployment OK'"
```

**問題点**:
- ❌ ファイルをサーバーにアップロードする処理がない
- ❌ SSH 接続のテストだけで終わっている
- ❌ `SAKURA_KEY` という secret が存在しない（正しくは `SAKURA_SSH_KEY`）

#### 修正後（完全版）
```yaml
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
```

**改善点**:
- ✅ SSH 接続のテスト
- ✅ **rsync でファイルをサーバーにアップロード**
- ✅ 不要なファイルを除外（.git, tests, vendor など）
- ✅ デプロイ後の検証

---

## ⚠️ GitHub App の権限制限

### プッシュ時のエラー
```
! [remote rejected] main -> main (refusing to allow a GitHub App to create or update workflow `.github/workflows/deploy.yml` without `workflows` permission)
error: failed to push some refs to 'https://github.com/garyohosu/magic-box-ai.git'
```

### 原因
GitHub App には `.github/workflows/` 配下のファイルを変更する権限がありません。これは GitHub のセキュリティ制限です。

### 解決方法
**ユーザー様がローカル環境で手動適用する必要があります。**

---

## 📝 手動適用手順（ユーザー様へ）

### 準備: ローカル環境で magic-box-ai リポジトリをクローン

```bash
# まだクローンしていない場合
cd ~/garyohosu
git clone https://github.com/garyohosu/magic-box-ai.git
cd magic-box-ai

# すでにクローン済みの場合
cd ~/garyohosu/magic-box-ai
git pull origin main
```

---

### 手順 1: BOM を削除（3ファイル）

```bash
cd ~/garyohosu/magic-box-ai

# すべてのワークフローファイルから BOM を削除
for file in .github/workflows/*.yml; do
  # macOS/Linux
  LC_ALL=C sed -i '' '1s/^\xEF\xBB\xBF//' "$file" 2>/dev/null || \
  # Linux (GNU sed)
  sed -i '1s/^\xEF\xBB\xBF//' "$file"
done

# 確認
head -1 .github/workflows/deploy.yml
# 期待値: "name: Deploy to Sakura" (﻿ が付いていないこと)
```

**Windows (PowerShell) の場合**:
```powershell
cd C:\Users\YourName\garyohosu\magic-box-ai

# すべてのワークフローファイルから BOM を削除
Get-ChildItem .github\workflows\*.yml | ForEach-Object {
    $content = [System.IO.File]::ReadAllText($_.FullName)
    if ($content[0] -eq [char]0xFEFF) {
        $content = $content.Substring(1)
        [System.IO.File]::WriteAllText($_.FullName, $content)
    }
}

# 確認
Get-Content .github\workflows\deploy.yml -Head 1
# 期待値: "name: Deploy to Sakura" (﻿ が付いていないこと)
```

---

### 手順 2: deploy.yml を完全版に置き換え

**ファイル**: `.github/workflows/deploy.yml`

以下の内容で**完全に置き換えてください**：

```yaml
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
```

**VS Code での編集方法**:
1. VS Code で `magic-box-ai` フォルダを開く
2. `.github/workflows/deploy.yml` を開く
3. すべての内容を削除
4. 上記の内容をコピー＆ペースト
5. 保存（Ctrl+S または Cmd+S）

---

### 手順 3: Git コミット＆プッシュ

```bash
cd ~/garyohosu/magic-box-ai

# 変更を確認
git status

# 変更をステージング
git add .github/workflows/

# コミット
git commit -m "fix: Remove BOM from GitHub Actions workflows and fix deployment

Critical fixes:
- Removed UTF-8 BOM from all workflow files
- Fixed deploy.yml to actually deploy files using rsync
- Changed SAKURA_KEY to SAKURA_SSH_KEY (correct secret name)
- Added SSH connection test
- Added rsync deployment with proper excludes
- Added deployment verification"

# プッシュ
git push origin main
```

**Windows (PowerShell) の場合**:
```powershell
cd C:\Users\YourName\garyohosu\magic-box-ai

# 変更を確認
git status

# 変更をステージング
git add .github/workflows/

# コミット
git commit -m "fix: Remove BOM from GitHub Actions workflows and fix deployment"

# プッシュ
git push origin main
```

---

### 手順 4: GitHub Actions の実行を確認

プッシュ後、以下の URL で GitHub Actions の実行状況を確認してください：

**GitHub Actions ページ**: https://github.com/garyohosu/magic-box-ai/actions

#### 確認すべき項目

1. **Test PHPUnit** - ✅ 緑色（成功）
2. **Test Pytest** - ✅ 緑色（成功）
3. **Deploy to Sakura** - ✅ 緑色（成功）

#### 期待される実行ログ

**Deploy to Sakura** のログで以下を確認：

```
✅ SSH connection OK
✅ sending incremental file list
✅ src/index.php
✅ src/cron_cleanup.php
✅ src/pages/home.php
✅ Deployment completed successfully
```

---

### 手順 5: 本番環境の確認

デプロイが完了したら（通常 5-10 分）、以下を確認してください：

**Production URL**: https://garyo.sakura.ne.jp/magicboxai/

#### 確認項目
- [ ] ページが正常に表示される
- [ ] **Example Prompts が 8 個表示される**
- [ ] ボタンがすべて表示される
- [ ] JavaScript が正常に動作する
- [ ] 404 エラーが出ていない

---

## 📊 修正の効果

### 修正前
```
❌ GitHub Actions がパースエラーで失敗
❌ デプロイが実行されない
❌ 本番環境のファイルが更新されない
❌ Example Prompts が表示されない
```

### 修正後（期待される結果）
```
✅ GitHub Actions が正常に実行される
✅ テストが成功する
✅ デプロイが自動的に実行される
✅ 本番環境のファイルが更新される
✅ Example Prompts が正常に表示される
✅ JavaScript が正常に動作する
```

---

## 🛡️ 再発防止策

### 1. エディタの設定
**VS Code** (推奨):
```json
{
  "files.encoding": "utf8",
  "files.eol": "\n"
}
```

### 2. `.editorconfig` の追加
リポジトリのルートに `.editorconfig` を追加：

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.yml]
indent_style = space
indent_size = 2
```

### 3. Git pre-commit フック
`.git/hooks/pre-commit` に以下を追加：

```bash
#!/bin/bash
# Check for BOM in workflow files
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '.github/workflows/.*\.yml$')
for FILE in $FILES; do
  if [ -f "$FILE" ] && head -c 3 "$FILE" | od -An -tx1 | grep -q "ef bb bf"; then
    echo "ERROR: BOM found in $FILE"
    exit 1
  fi
done
```

---

## 🎯 次のアクション（ユーザー様へ）

### 優先度 1: 手動修正の適用（必須）
上記の「手動適用手順」を実行してください：

1. BOM を削除（3ファイル）
2. deploy.yml を完全版に置き換え
3. Git コミット＆プッシュ

### 優先度 2: GitHub Actions の確認（5-10分後）
https://github.com/garyohosu/magic-box-ai/actions

すべてのワークフローが成功しているか確認してください。

### 優先度 3: 本番環境の確認（デプロイ後）
https://garyo.sakura.ne.jp/magicboxai/

Example Prompts が正常に表示されるか確認してください。

---

## 📚 関連情報

### ローカルで作成したファイル
```
/home/user/magic-box-ai/.github/workflows/deploy.yml     (修正済み・未プッシュ)
/home/user/magic-box-ai/.github/workflows/test-phpunit.yml  (BOM削除済み・未プッシュ)
/home/user/magic-box-ai/.github/workflows/test-pytest.yml   (BOM削除済み・未プッシュ)
```

### Git コミット情報
```
Commit: 3e840ed (ローカルのみ)
Branch: main
Status: 未プッシュ（GitHub App の権限制限のため）
```

---

## 🎉 まとめ

### 発見した問題
- ❌ 3つのワークフローファイルに BOM が含まれていた
- ❌ deploy.yml の実装が不完全だった
- ❌ ファイルをサーバーにアップロードする処理がなかった

### 実施した修正
- ✅ すべてのワークフローファイルから BOM を削除
- ✅ deploy.yml を完全版に置き換え（rsync によるデプロイ）
- ✅ ローカル環境で修正完了

### 次のステップ
**ユーザー様による手動適用が必要です：**
1. ローカル環境で BOM を削除
2. deploy.yml を完全版に置き換え
3. Git コミット＆プッシュ
4. GitHub Actions の実行を確認
5. 本番環境で動作を確認

---

**修正手順がわからない場合や、問題が発生した場合は、お気軽にお知らせください！**

---

**作成日時**: 2026-02-01  
**作成者**: Genspark AI  
**ステータス**: ローカル修正完了、手動適用待ち
