# Order - MagicBoxAI Save/View 機能修復

**Status**: ⏳ 修復待ち
**Current Actor**: Gemini CLI
**Problem**: 保存した HTML の View URL が 404、UX が不便
**Output**: `results/diagnosis/MAGICBOXAI_SAVE_VIEW_DIAGNOSTIC.md`

---

## 🎯 ミッション

1. **Save 機能診断**: ファイルが正しく保存されているか
2. **View 機能診断**: view.php が存在して動作しているか
3. **UX 改善**: 「開く」「コピー」ボタン を追加

---

## 📋 診断スクリプト

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cat > /tmp/magicboxai_save_view_diagnostic.md << 'EOF'
# MagicBoxAI Save/View 診断レポート

**実行日時**: $(date)

---

## 1️⃣ ファイル構成確認

### ~/www/magicboxai/ の内容

\`\`\`bash
ls -la ~/www/magicboxai/
find ~/www/magicboxai -type f | sort
\`\`\`

結果：
\`\`\`
$(ls -la ~/www/magicboxai/)

$(find ~/www/magicboxai -type f | sort)
\`\`\`

---

## 2️⃣ view.php の存在確認

\`\`\`bash
ls -lah ~/www/magicboxai/view.php
file ~/www/magicboxai/view.php
head -20 ~/www/magicboxai/view.php
\`\`\`

結果：
\`\`\`
$(ls -lah ~/www/magicboxai/view.php 2>&1)

$(file ~/www/magicboxai/view.php 2>&1)

$(head -20 ~/www/magicboxai/view.php 2>&1)
\`\`\`

---

## 3️⃣ data/ ディレクトリ内容

\`\`\`bash
echo "=== data/ ディレクトリ ==="
ls -lah ~/www/magicboxai/data/

echo ""
echo "=== 保存されたファイル数 ==="
find ~/www/magicboxai/data -type f | wc -l

echo ""
echo "=== 保存ファイル一覧 ==="
find ~/www/magicboxai/data -type f | head -10
\`\`\`

結果：
\`\`\`
$(ls -lah ~/www/magicboxai/data/)

$(find ~/www/magicboxai/data -type f | wc -l)

$(find ~/www/magicboxai/data -type f | head -10)
\`\`\`

---

## 4️⃣ index.php の routing 確認

\`\`\`bash
echo "=== index.php で '/view/' ルーティングをサポートしているか ==="
grep -n "view" ~/www/magicboxai/index.php
\`\`\`

結果：
\`\`\`
$(grep -n "view" ~/www/magicboxai/index.php)
\`\`\`

---

## 5️⃣ API エンドポイント確認

\`\`\`bash
echo "=== GET /api/health ==="
curl -s https://garyo.sakura.ne.jp/magicboxai/index.php/api/health

echo ""
echo "=== POST /api/save テスト ==="
curl -X POST https://garyo.sakura.ne.jp/magicboxai/index.php/api/save \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "html=<html><body>Test</body></html>" \
  2>&1 | head -20
\`\`\`

結果：
\`\`\`
$(curl -s https://garyo.sakura.ne.jp/magicboxai/index.php/api/health 2>&1)

$(curl -X POST https://garyo.sakura.ne.jp/magicboxai/index.php/api/save \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "html=<html><body>Test</body></html>" \
  2>&1 | head -20)
\`\`\`

---

## 🎯 診断結果

### view.php の存在

$(test -f ~/www/magicboxai/view.php && echo "✅ 存在する" || echo "❌ 見つかりません")

### data/ に保存されたファイル

$(test -d ~/www/magicboxai/data && echo "✅ ディレクトリ存在" || echo "❌ ディレクトリなし")

$(find ~/www/magicboxai/data -type f 2>/dev/null | wc -l) 個のファイルが保存されている

### ルーティング対応

$(grep -q "view" ~/www/magicboxai/index.php && echo "✅ view ルーティングあり" || echo "❌ view ルーティングなし")

---

## 🔧 修復方針

$(if test ! -f ~/www/magicboxai/view.php; then
  echo "❌ **view.php が見つかりません**"
  echo ""
  echo "修復内容："
  echo "1. view.php を作成"
  echo "2. トークンからファイルを検索・表示"
  echo "3. ルーティングを設定"
elif ! grep -q "view" ~/www/magicboxai/index.php; then
  echo "❌ **index.php に view ルーティングがありません**"
  echo ""
  echo "修復内容："
  echo "1. index.php に /view/{token} ルーティングを追加"
  echo "2. view.php と連携"
else
  echo "✅ **ファイルとルーティングは OK**"
  echo ""
  echo "UX 改善内容："
  echo "1. 「開く」ボタン追加（JavaScript で新タブオープン）"
  echo "2. 「コピー」ボタン追加（クリップボード API）"
  echo "3. QR コード表示オプション"
fi)

EOF

cat /tmp/magicboxai_save_view_diagnostic.md

EOFSH
```

---

## ✅ 成功基準

- ✅ view.php の存在確認
- ✅ ルーティングの確認
- ✅ 保存されたファイルの確認
- ✅ 修復方針の判定
- ✅ UX 改善案の提示

---

**Status**: Save/View 診断 Order 準備完了
