# Order - MagicBoxAI 詳細診断（Gemini CLI 用）

**Status**: ⏳ 詳細診断実行待ち
**Current Actor**: Gemini CLI（SSH 実行）
**Recommended**: `gem order_magicboxai_detailed_diagnostic.md`
**Output Format**: Markdown（Claude が読む）

---

## 🎯 ミッション

前回の Codex 診断では `.htaccess` などが確認できなかったため、
詳細な確認を実施

**出力**: `results/diagnosis/MAGICBOXAI_DETAILED_CHECK.md`

---

## 📋 詳細診断スクリプト

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cat > /tmp/magicboxai_detailed_check.md << 'EOF'
# MagicBoxAI 詳細診断レポート

**実行日時**: $(date)
**ホスト**: $(hostname)
**実行ユーザー**: $(whoami)

---

## 1️⃣ 重要ファイル詳細確認

### index.html

\`\`\`bash
ls -lah ~/www/index.html
file ~/www/index.html
head -5 ~/www/index.html
\`\`\`

結果：
\`\`\`
$(ls -lah ~/www/index.html 2>&1)

$(file ~/www/index.html 2>&1)

$(head -5 ~/www/index.html 2>&1)
\`\`\`

### .htaccess

\`\`\`bash
ls -lah ~/www/.htaccess
cat ~/www/.htaccess
\`\`\`

結果：
\`\`\`
$(ls -lah ~/www/.htaccess 2>&1)

$(cat ~/www/.htaccess 2>&1)
\`\`\`

### magicboxai/index.php

\`\`\`bash
ls -lah ~/www/magicboxai/index.php
file ~/www/magicboxai/index.php
wc -l ~/www/magicboxai/index.php
head -10 ~/www/magicboxai/index.php
\`\`\`

結果：
\`\`\`
$(ls -lah ~/www/magicboxai/index.php 2>&1)

$(file ~/www/magicboxai/index.php 2>&1)

$(wc -l ~/www/magicboxai/index.php 2>&1)

$(head -10 ~/www/magicboxai/index.php 2>&1)
\`\`\`

---

## 2️⃣ ディレクトリ構造詳細

### magicboxai/ 全構成

\`\`\`bash
find ~/www/magicboxai -type f | sort
\`\`\`

結果：
\`\`\`
$(find ~/www/magicboxai -type f | sort 2>&1)
\`\`\`

### ファイル数と合計サイズ

\`\`\`bash
echo "ファイル数:"
find ~/www/magicboxai -type f | wc -l

echo ""
echo "合計サイズ:"
du -sh ~/www/magicboxai

echo ""
echo "内容内訳:"
du -sh ~/www/magicboxai/* | sort -h
\`\`\`

結果：
\`\`\`
$(echo "ファイル数:" && find ~/www/magicboxai -type f | wc -l && echo "" && echo "合計サイズ:" && du -sh ~/www/magicboxai && echo "" && echo "内容内訳:" && du -sh ~/www/magicboxai/* | sort -h)
\`\`\`

---

## 3️⃣ Apache 設定確認

### DocumentRoot の確認

\`\`\`bash
echo "=== Apache設定ファイル検索 ==="
find /etc /usr/local/etc -name "*httpd.conf*" -o -name "*apache*" 2>/dev/null | grep -v ".so"

echo ""
echo "=== DocumentRoot 設定確認 ==="
grep -r "^DocumentRoot" /etc/apache2 2>/dev/null || grep -r "^DocumentRoot" /usr/local/etc/apache24 2>/dev/null || echo "DocumentRoot 設定が見つかりません"

echo ""
echo "=== VirtualHost 設定 ==="
grep -A 5 "<VirtualHost" /etc/apache2/sites-enabled/*.conf 2>/dev/null | head -20 || echo "VirtualHost 設定が見つかりません"
\`\`\`

結果：
\`\`\`
$(echo "=== Apache設定ファイル検索 ===" && find /etc /usr/local/etc -name "*httpd.conf*" -o -name "*apache*" 2>/dev/null | grep -v ".so" && echo "" && echo "=== DocumentRoot 設定確認 ===" && grep -r "^DocumentRoot" /etc/apache2 2>/dev/null || grep -r "^DocumentRoot" /usr/local/etc/apache24 2>/dev/null || echo "DocumentRoot 設定が見つかりません" && echo "" && echo "=== VirtualHost 設定 ===" && grep -A 5 "<VirtualHost" /etc/apache2/sites-enabled/*.conf 2>/dev/null | head -20 || echo "VirtualHost 設定が見つかりません")
\`\`\`

---

## 4️⃣ PHP 実行テスト

### PHP が実行されるか確認

\`\`\`bash
echo "=== PHP バージョン確認 ==="
php -v

echo ""
echo "=== PHP が ~/www で実行可能か ==="
cd ~/www/magicboxai && php index.php 2>&1 | head -20
\`\`\`

結果：
\`\`\`
$(php -v 2>&1)

$(cd ~/www/magicboxai && php index.php 2>&1 | head -20)
\`\`\`

### ブラウザアクセステスト

\`\`\`bash
echo "=== HTTP リダイレクト確認 ==="
curl -I http://garyo.sakura.ne.jp/ 2>&1 | head -10

echo ""
echo "=== MagicBoxAI へのアクセステスト ==="
curl -I http://garyo.sakura.ne.jp/~garyo/magicboxai/ 2>&1 | head -10

echo ""
echo "=== index.html の内容確認 ==="
curl -s http://garyo.sakura.ne.jp/ | head -15
\`\`\`

結果：
\`\`\`
$(echo "=== HTTP リダイレクト確認 ===" && curl -I http://garyo.sakura.ne.jp/ 2>&1 | head -10 && echo "" && echo "=== MagicBoxAI へのアクセステスト ===" && curl -I http://garyo.sakura.ne.jp/~garyo/magicboxai/ 2>&1 | head -10 && echo "" && echo "=== index.html の内容確認 ===" && curl -s http://garyo.sakura.ne.jp/ | head -15)
\`\`\`

---

## 5️⃣ パーミッション確認

\`\`\`bash
echo "=== 重要ファイルのパーミッション ==="
ls -la ~/www/index.html ~/www/.htaccess ~/www/magicboxai/index.php 2>&1

echo ""
echo "=== ディレクトリパーミッション ==="
ls -la ~/www/magicboxai 2>&1 | head -5

echo ""
echo "=== data ディレクトリ（書き込み必要） ==="
ls -la ~/www/magicboxai/data 2>&1
\`\`\`

結果：
\`\`\`
$(echo "=== 重要ファイルのパーミッション ===" && ls -la ~/www/index.html ~/www/.htaccess ~/www/magicboxai/index.php 2>&1 && echo "" && echo "=== ディレクトリパーミッション ===" && ls -la ~/www/magicboxai 2>&1 | head -5 && echo "" && echo "=== data ディレクトリ（書き込み必要） ===" && ls -la ~/www/magicboxai/data 2>&1)
\`\`\`

---

## 🎯 診断結果の判定

### ファイル配置状況

| 項目 | 状態 | 詳細 |
|------|------|------|
| index.html | $(test -f ~/www/index.html && echo "✅" || echo "❌") | $(test -f ~/www/index.html && ls -lh ~/www/index.html | awk '{print $5 " bytes"}' || echo "見つかりません") |
| .htaccess | $(test -f ~/www/.htaccess && echo "✅" || echo "❌") | $(test -f ~/www/.htaccess && cat ~/www/.htaccess | head -1 || echo "見つかりません") |
| magicboxai/ | $(test -d ~/www/magicboxai && echo "✅" || echo "❌") | $(test -d ~/www/magicboxai && echo "ディレクトリ存在" || echo "見つかりません") |
| index.php | $(test -f ~/www/magicboxai/index.php && echo "✅" || echo "❌") | $(test -f ~/www/magicboxai/index.php && wc -l < ~/www/magicboxai/index.php | xargs echo "行" || echo "見つかりません") |
| data/ | $(test -d ~/www/magicboxai/data && echo "✅" || echo "❌") | $(test -d ~/www/magicboxai/data && echo "書き込み可能" || echo "見つかりません") |

### PHP 実行状況

| 項目 | 状態 | 詳細 |
|------|------|------|
| PHP バージョン | $(php -v > /dev/null 2>&1 && echo "✅" || echo "❌") | $(php -v 2>&1 | head -1) |
| PHP 実行テスト | $(cd ~/www/magicboxai && php index.php > /dev/null 2>&1 && echo "✅" || echo "❌") | $(cd ~/www/magicboxai && php index.php 2>&1 | head -1 || echo "エラー") |

### Apache 設定状況

| 項目 | 状態 | 詳細 |
|------|------|------|
| DocumentRoot | $(grep -r "^DocumentRoot" /etc/apache2 /usr/local/etc/apache24 > /dev/null 2>&1 && echo "✅" || echo "❌") | $(grep -r "^DocumentRoot" /etc/apache2 /usr/local/etc/apache24 2>/dev/null | head -1 || echo "確認不可") |
| .htaccess 有効 | $([ -f ~/www/.htaccess ] && grep -q "Indexes" ~/www/.htaccess && echo "✅" || echo "❌") | Options -Indexes が設定されているか |

---

## ✅ / ⚠️ 最終判定

$(if test -f ~/www/index.html && test -d ~/www/magicboxai && test -f ~/www/magicboxai/index.php; then
  echo "✅ **基本的にはすべてのファイルが配置されています**"
  echo ""
  echo "確認事項："
  echo "1. ブラウザで http://garyo.sakura.ne.jp/ にアクセス"
  echo "2. MagicBoxAI へリダイレクトされるか確認"
  echo "3. https://magicboxai.x0.com/ で動作確認（DNS反映後）"
else
  echo "❌ **ファイルが欠けています**"
  echo ""
  echo "修正が必要："
  if ! test -f ~/www/index.html; then echo "- index.html を配置"; fi
  if ! test -d ~/www/magicboxai; then echo "- magicboxai/ ディレクトリを配置"; fi
  if ! test -f ~/www/magicboxai/index.php; then echo "- magicboxai/index.php を確認"; fi
fi)

---

## 📝 次のステップ

$(if test -f ~/www/index.html && test -d ~/www/magicboxai && test -f ~/www/magicboxai/index.php; then
  echo "1. ✅ ファイル配置は OK"
  echo "2. ⏳ ブラウザでアクセステスト"
  echo "3. ⏳ DNS 反映待ち（https://magicboxai.x0.com/）"
  echo "4. ⏳ note 記事販売開始"
else
  echo "1. ファイル配置エラーを修正"
  echo "2. 再度診断実行"
  echo "3. OK 確認後に本番公開"
fi)

EOF

# ファイルの内容を表示
cat /tmp/magicboxai_detailed_check.md

EOFSH
```

---

## ✅ 成功基準

- ✅ すべてのファイルが詳細に確認される
- ✅ Apache 設定が確認される
- ✅ PHP 実行テストが実施される
- ✅ HTTP アクセステストが実施される
- ✅ 詳細な判定レポートが生成される

---

**Status**: 詳細診断 Order 準備完了
