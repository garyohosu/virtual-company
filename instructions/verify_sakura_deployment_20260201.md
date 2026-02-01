# 指示書: Sakura サーバーのファイル確認とデバッグ

## 📋 基本情報
- **機能名**: Sakura サーバーファイル確認
- **プロジェクト**: magic-box-ai
- **作成日**: 2026-02-01
- **対象リポジトリ**: garyohosu/magic-box-ai
- **対象AI**: Gemini CLI
- **優先度**: 🔴 CRITICAL

---

## 🎯 実行内容

### 概要
本番環境で画像が変わっていない。Sakura サーバーに SSH 接続して、index.php が正しくアップロードされているか確認する。

### 背景
- GitHub Actions の Deploy to Sakura が成功しているはず
- しかし、本番環境で古いコンテンツが表示されている
- Example Prompts が表示されていない
- オセロゲームの画像が表示されている（古いコンテンツ）

---

## 📝 実装手順

### Step 1: SSH 接続とファイル確認

```bash
# Sakura サーバーに SSH 接続
ssh garyo@garyo.sakura.ne.jp << 'EOF'

echo "=== 1. ファイルの存在確認 ==="
ls -lh ~/public_html/magicboxai/src/index.php
echo ""

echo "=== 2. ファイルサイズと行数 ==="
wc -l ~/public_html/magicboxai/src/index.php
wc -c ~/public_html/magicboxai/src/index.php
echo ""

echo "=== 3. Example Prompts が含まれているか ==="
grep -c 'Example Prompts' ~/public_html/magicboxai/src/index.php || echo "0"
grep -c 'example' ~/public_html/magicboxai/src/index.php || echo "0"
echo ""

echo "=== 4. 最後の5行を確認（</html> で終わっているか） ==="
tail -5 ~/public_html/magicboxai/src/index.php
echo ""

echo "=== 5. ファイルの先頭5行を確認（BOM がないか） ==="
head -5 ~/public_html/magicboxai/src/index.php
echo ""

echo "=== 6. BOM の確認 ==="
od -c ~/public_html/magicboxai/src/index.php | head -1
echo ""

echo "=== 7. home.php の確認 ==="
if [ -f ~/public_html/magicboxai/src/pages/home.php ]; then
  echo "home.php exists"
  wc -l ~/public_html/magicboxai/src/pages/home.php
  grep -c 'Example Prompts' ~/public_html/magicboxai/src/pages/home.php || echo "0"
  grep -c 'Tailwind' ~/public_html/magicboxai/src/pages/home.php || echo "0"
  grep -c 'Alpine' ~/public_html/magicboxai/src/pages/home.php || echo "0"
else
  echo "home.php NOT FOUND!"
fi
echo ""

echo "=== 8. ディレクトリ構造の確認 ==="
ls -la ~/public_html/magicboxai/
echo ""
ls -la ~/public_html/magicboxai/src/
echo ""

echo "=== 9. .htaccess の確認 ==="
if [ -f ~/public_html/magicboxai/.htaccess ]; then
  cat ~/public_html/magicboxai/.htaccess
else
  echo ".htaccess NOT FOUND!"
fi
echo ""

echo "=== 10. 最終更新日時 ==="
stat ~/public_html/magicboxai/src/index.php | grep Modify
stat ~/public_html/magicboxai/src/pages/home.php | grep Modify 2>/dev/null || echo "home.php not found"
echo ""

EOF
```

### Step 2: GitHub Actions のデプロイログ確認

```bash
# magic-box-ai リポジトリに移動
cd ~/garyohosu/magic-box-ai

# 最新の GitHub Actions のログを確認（gh コマンドが使える場合）
echo "=== GitHub Actions の最新実行状況 ==="
gh run list --limit 5 || echo "gh command not available"
echo ""

# 最新の Deploy to Sakura のログを確認
echo "=== 最新の Deploy to Sakura ログ ==="
gh run view --log | grep -A 50 "Deploy to Sakura" || echo "gh command not available or no logs found"
echo ""
```

### Step 3: ローカルファイルとの比較

```bash
cd ~/garyohosu/magic-box-ai

echo "=== ローカルファイルの確認 ==="
echo "--- index.php ---"
wc -l src/index.php
echo ""

echo "--- home.php ---"
wc -l src/pages/home.php
echo ""

echo "--- home.php に Example Prompts が含まれているか ---"
grep -c 'Example Prompts' src/pages/home.php || echo "0"
echo ""

echo "--- BOM の確認 ---"
od -c src/index.php | head -1
od -c src/pages/home.php | head -1
echo ""
```

### Step 4: デプロイの再実行（もし必要なら）

```bash
cd ~/garyohosu/magic-box-ai

# もしファイルが古い場合、手動で rsync デプロイ
echo "=== 手動デプロイの実行 ==="

# SSH 秘密鍵のパスを確認
SSH_KEY_PATH="$HOME/.ssh/id_rsa"
if [ ! -f "$SSH_KEY_PATH" ]; then
  SSH_KEY_PATH="$HOME/.ssh/id_ed25519"
fi

if [ -f "$SSH_KEY_PATH" ]; then
  echo "Using SSH key: $SSH_KEY_PATH"
  
  # rsync で src/ ディレクトリをデプロイ
  rsync -avz --delete \
    -e "ssh -i $SSH_KEY_PATH" \
    --exclude='.git' \
    --exclude='.github' \
    --exclude='tests' \
    --exclude='vendor' \
    --exclude='composer.lock' \
    --exclude='README.md' \
    --exclude='.gitignore' \
    src/ garyo@garyo.sakura.ne.jp:~/public_html/magicboxai/src/
  
  echo "✅ Manual deployment completed"
else
  echo "⚠️ SSH key not found. Cannot deploy manually."
fi
```

### Step 5: キャッシュのクリア

```bash
# ブラウザキャッシュのクリアを提案
cat << 'EOF'

=== ブラウザキャッシュのクリア方法 ===

本番環境で画像が変わっていない場合、以下を試してください：

1. ブラウザの強制リロード
   - Windows: Ctrl + F5 または Ctrl + Shift + R
   - Mac: Cmd + Shift + R
   
2. ブラウザのキャッシュをクリア
   - Chrome: Ctrl+Shift+Delete → キャッシュをクリア
   - Firefox: Ctrl+Shift+Delete → キャッシュをクリア
   
3. シークレットモード/プライベートブラウジングで開く
   - これでキャッシュを無視して最新版を確認できます

4. Sakura サーバー側で PHP キャッシュをクリア
   ssh garyo@garyo.sakura.ne.jp
   # もし OPcache が有効な場合
   touch ~/public_html/magicboxai/src/index.php
   # これでタイムスタンプが更新され、キャッシュが無効化される

EOF
```

---

## ✅ 検証項目

### 1. ファイルの確認
- [ ] index.php が存在する（~/public_html/magicboxai/src/index.php）
- [ ] index.php のサイズが正しい（約 4.5KB、150行）
- [ ] home.php が存在する（~/public_html/magicboxai/src/pages/home.php）
- [ ] home.php のサイズが正しい（約 21KB、419行）

### 2. コンテンツの確認
- [ ] home.php に "Example Prompts" が含まれている
- [ ] home.php に "Tailwind" が含まれている
- [ ] home.php に "Alpine" が含まれている
- [ ] index.php の最後が `</html>` で終わっている
- [ ] BOM がない（`357 273 277` が先頭にない）

### 3. デプロイの確認
- [ ] 最終更新日時が最近（2026-02-01 以降）
- [ ] .htaccess が正しく配置されている
- [ ] ディレクトリ構造が正しい

### 4. 本番環境の確認
- [ ] https://garyo.sakura.ne.jp/magicboxai/ にアクセス
- [ ] Example Prompts が表示される（オセロゲームではない）
- [ ] ボタンが表示される
- [ ] JavaScript が動作する

---

## 🔍 よくある問題と解決方法

### 問題 1: ファイルが古い
**原因**: GitHub Actions のデプロイが失敗している

**解決方法**:
```bash
# 手動で rsync デプロイを実行
cd ~/garyohosu/magic-box-ai
rsync -avz --delete \
  -e "ssh -i ~/.ssh/id_rsa" \
  src/ garyo@garyo.sakura.ne.jp:~/public_html/magicboxai/src/
```

### 問題 2: home.php がない
**原因**: デプロイ時に home.php が含まれていない

**解決方法**:
```bash
# ローカルで確認
cd ~/garyohosu/magic-box-ai
ls -la src/pages/home.php

# 存在する場合、手動でアップロード
scp -i ~/.ssh/id_rsa src/pages/home.php \
  garyo@garyo.sakura.ne.jp:~/public_html/magicboxai/src/pages/
```

### 問題 3: ブラウザキャッシュ
**原因**: ブラウザが古いバージョンをキャッシュしている

**解決方法**:
```bash
# 強制リロード: Ctrl+F5 (Windows) または Cmd+Shift+R (Mac)
# シークレットモードで開く
```

### 問題 4: PHP キャッシュ（OPcache）
**原因**: Sakura サーバーの PHP キャッシュが古いファイルを保持している

**解決方法**:
```bash
ssh garyo@garyo.sakura.ne.jp
touch ~/public_html/magicboxai/src/index.php
touch ~/public_html/magicboxai/src/pages/home.php
```

### 問題 5: .htaccess の問題
**原因**: .htaccess が正しく設定されていない

**解決方法**:
```bash
ssh garyo@garyo.sakura.ne.jp
cat > ~/public_html/magicboxai/.htaccess << 'EOF'
# PHP as CGI
AddHandler application/x-httpd-phpcgi .php

# Rewrite rules
RewriteEngine On
RewriteBase /magicboxai/

# Route all requests to src/index.php
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ src/index.php/$1 [L]
EOF
```

---

## 📊 期待される結果

### SSH 確認結果（正常な場合）
```
=== 1. ファイルの存在確認 ===
-rw-r--r-- 1 garyo garyo 4.5K Feb  1 12:34 index.php

=== 2. ファイルサイズと行数 ===
150 index.php
4500 index.php

=== 3. Example Prompts が含まれているか ===
0  (index.php には含まれない)

=== 7. home.php の確認 ===
home.php exists
419 src/pages/home.php
8  (Example Prompts の出現回数)
5  (Tailwind の出現回数)
5  (Alpine の出現回数)
```

### 本番環境（正常な場合）
- ✅ https://garyo.sakura.ne.jp/magicboxai/ にアクセス
- ✅ Example Prompts が 8 個表示される
- ✅ オセロゲームは表示されない
- ✅ Tailwind CSS のスタイルが適用される
- ✅ Alpine.js が動作する

---

## 🔗 関連リソース

- **Production URL**: https://garyo.sakura.ne.jp/magicboxai/
- **GitHub Actions**: https://github.com/garyohosu/magic-box-ai/actions
- **Deploy ワークフロー**: https://github.com/garyohosu/magic-box-ai/blob/main/.github/workflows/deploy.yml

---

## 📝 次のアクション

1. この指示書を Gemini CLI で実行
   ```bash
   cd ~/garyohosu/virtual-company
   ./scripts/gemini_wrapper.sh instructions/verify_sakura_deployment_20260201.md
   ```

2. 実行結果を確認
   ```bash
   cat results/gemini/2026-02-01_*_verify_sakura_deployment_20260201.md
   ```

3. 問題があれば、手動デプロイを実行
   ```bash
   cd ~/garyohosu/magic-box-ai
   rsync -avz --delete src/ garyo@garyo.sakura.ne.jp:~/public_html/magicboxai/src/
   ```

4. ブラウザで強制リロード（Ctrl+F5）

---

## 📌 Status

- **Current**: 指示書作成完了
- **Next**: Gemini CLI で実行
- **Created At**: 2026-02-01

---

**この指示書を Gemini CLI で実行すれば、Sakura サーバーの状態を確認し、問題があれば修正できます！**
