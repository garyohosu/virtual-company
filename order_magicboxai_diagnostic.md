# Order - MagicBoxAI ファイル配置確認（診断用）

**Status**: ⏳ ファイル存在確認待ち
**Current Actor**: Codex（SSH 診断実行）
**Output Format**: Markdown（Claude が読む）

---

## 🎯 ミッション

MagicBoxAI のファイルが正しく ~/www/ に配置されているか確認

**出力**: `results/diagnosis/MAGICBOXAI_FILE_CHECK.md`

---

## 📋 診断スクリプト

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cat > /tmp/magicboxai_check.md << 'EOF'
# MagicBoxAI ファイル配置診断レポート

**実行日時**: $(date)
**ホスト**: Sakura FreeBSD

---

## 1️⃣ ディレクトリ構造確認

### ~/www/ の内容

\`\`\`
$(ls -lR ~/www/ 2>&1 | head -50)
\`\`\`

### ~/www/magicboxai/ は存在するか？

\`\`\`
$(test -d ~/www/magicboxai && echo "✅ 存在する" || echo "❌ 存在しない")
$(ls -la ~/www/magicboxai 2>&1)
\`\`\`

---

## 2️⃣ 重要ファイル確認

### index.html

\`\`\`
$(ls -la ~/www/index.html 2>&1)
\`\`\`

### .htaccess

\`\`\`
$(ls -la ~/www/.htaccess 2>&1)
\`\`\`

### magicboxai/index.php

\`\`\`
$(ls -la ~/www/magicboxai/index.php 2>&1)
\`\`\`

### magicboxai/pages/home.php

\`\`\`
$(ls -la ~/www/magicboxai/pages/home.php 2>&1)
\`\`\`

---

## 3️⃣ public_html との比較

### ~/public_html/ の内容

\`\`\`
$(ls -la ~/public_html 2>&1 | head -30)
\`\`\`

### ~/public_html/magicboxai は存在するか？

\`\`\`
$(test -d ~/public_html/magicboxai && echo "✅ 存在する" || echo "❌ 存在しない")
\`\`\`

---

## 4️⃣ ファイル数確認

\`\`\`bash
echo "www/magicboxai 内のファイル数:"
find ~/www/magicboxai -type f 2>/dev/null | wc -l

echo ""
echo "public_html/magicboxai 内のファイル数:"
find ~/public_html/magicboxai -type f 2>/dev/null | wc -l
\`\`\`

結果：
\`\`\`
$(echo "www/magicboxai 内のファイル数:" && find ~/www/magicboxai -type f 2>/dev/null | wc -l && echo "" && echo "public_html/magicboxai 内のファイル数:" && find ~/public_html/magicboxai -type f 2>/dev/null | wc -l)
\`\`\`

---

## 5️⃣ Apache 設定確認

\`\`\`bash
echo "DocumentRoot 確認:"
grep -r "DocumentRoot" /etc/apache2/sites-enabled/ 2>/dev/null || grep -r "DocumentRoot" /usr/local/etc/apache24/ 2>/dev/null || echo "設定ファイル見つかりません"
\`\`\`

結果：
\`\`\`
$(grep -r "DocumentRoot" /etc/apache2/sites-enabled/ 2>/dev/null || grep -r "DocumentRoot" /usr/local/etc/apache24/ 2>/dev/null || echo "設定ファイル見つかりません")
\`\`\`

---

## 🎯 診断結果

### ファイルの配置状況

| ファイル | ~/www/ | ~/public_html/ | 状態 |
|---------|--------|----------------|------|
| index.html | $(test -f ~/www/index.html && echo "✅" || echo "❌") | $(test -f ~/public_html/index.html && echo "✅" || echo "❌") | $(test -f ~/www/index.html && test -f ~/public_html/index.html && echo "両方ある" || echo "差異あり") |
| .htaccess | $(test -f ~/www/.htaccess && echo "✅" || echo "❌") | $(test -f ~/public_html/.htaccess && echo "✅" || echo "❌") | $(test -f ~/www/.htaccess && test -f ~/public_html/.htaccess && echo "両方ある" || echo "差異あり") |
| magicboxai/ | $(test -d ~/www/magicboxai && echo "✅" || echo "❌") | $(test -d ~/public_html/magicboxai && echo "✅" || echo "❌") | $(test -d ~/www/magicboxai && test -d ~/public_html/magicboxai && echo "両方ある" || echo "片方のみ") |
| magicboxai/index.php | $(test -f ~/www/magicboxai/index.php && echo "✅" || echo "❌") | $(test -f ~/public_html/magicboxai/index.php && echo "✅" || echo "❌") | - |

---

## 🔍 判定

$(if test -d ~/www/magicboxai && test -f ~/www/magicboxai/index.php; then
  echo "✅ **OK**: MagicBoxAI は ~/www/ に正しく配置されている"
elif test -d ~/public_html/magicboxai && test -f ~/public_html/magicboxai/index.php; then
  echo "⚠️ **配置エラー**: MagicBoxAI は ~/public_html/ にのみ存在する"
  echo ""
  echo "**対応**: ~/www/ に正しくコピーする必要があります"
  echo ""
  echo "修正コマンド:"
  echo "\`\`\`bash"
  echo "cp ~/public_html/index.html ~/www/"
  echo "cp ~/public_html/.htaccess ~/www/"
  echo "cp -r ~/public_html/magicboxai ~/www/"
  echo "chmod 644 ~/www/index.html ~/www/.htaccess"
  echo "chmod 755 ~/www/magicboxai"
  echo "\`\`\`"
else
  echo "❌ **ERROR**: MagicBoxAI が見つかりません"
  echo ""
  echo "**対応**: order_sakura_php_cgi版.md を再実行してください"
fi)

---

## 📝 次のステップ

$(if test -d ~/www/magicboxai && test -f ~/www/magicboxai/index.php; then
  echo "✅ ファイルは正しく配置されています"
  echo ""
  echo "確認事項:"
  echo "1. http://garyo.sakura.ne.jp/ へアクセス → リダイレクト確認"
  echo "2. http://garyo.sakura.ne.jp/~garyo/magicboxai/ へ直接アクセス"
  echo "3. MagicBoxAI UI が表示されるか確認"
else
  echo "❌ ファイル配置に問題があります"
  echo ""
  echo "修正手順:"
  echo "1. 上記「対応」の修正コマンドを実行"
  echo "2. ファイル配置確認"
  echo "3. ブラウザでアクセス"
fi)

EOF

# ファイルの内容を表示
cat /tmp/magicboxai_check.md

EOFSH
```

### Step 2: 結果ファイルを results/ に保存

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

# 結果をローカルにコピー
cd /tmp
cat magicboxai_check.md

EOFSH
```

### Step 3: GitHub に保存

```bash
cd ~/virtual-company

# 診断結果をファイルに保存
mkdir -p results/diagnosis

cat > results/diagnosis/MAGICBOXAI_FILE_CHECK.md << 'DIAGNOSTIC_OUTPUT'
[SSH 診断スクリプトの出力がここに入る]
DIAGNOSTIC_OUTPUT

git add results/diagnosis/MAGICBOXAI_FILE_CHECK.md
git commit -m "diag: Add MAGICBOXAI_FILE_CHECK.md - ファイル配置診断"
git push

echo "✅ 診断結果を GitHub に保存しました"
echo "Claude が読んでください: results/diagnosis/MAGICBOXAI_FILE_CHECK.md"

```

---

## ✅ 成功基準

- ✅ SSH で診断実行
- ✅ 結果を MD ファイルで出力
- ✅ GitHub に保存
- ✅ Claude が MD を読む

---

**Status**: ファイル配置診断準備完了
