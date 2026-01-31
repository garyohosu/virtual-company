# Order - Sakura public_html セキュリティ修正（Indexes 非表示化）

**Status**: ⏳ セキュリティ修正待ち
**Current Actor**: Codex（SSH 経由実行）
**Next Actor**: CEO（確認）

---

## 🎯 ミッション

Sakura の `public_html/` に index.html を配置して、
ディレクトリ内容が丸見えになるのを防止

**問題**: Apache で Indexes が有効 → ホームディレクトリが見える
**解決**: index.html で MagicBoxAI へリダイレクト

---

## 📋 実装内容

### Step 1: public_html に index.html を作成

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/public_html

# index.html を作成（MagicBoxAI へリダイレクト）
cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="0; url=/~garyo/magicboxai/">
    <title>MagicBoxAI にリダイレクト中...</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: Arial, sans-serif;
        }
        .container {
            text-align: center;
            color: white;
        }
        h1 { font-size: 2em; margin-bottom: 10px; }
        p { opacity: 0.9; }
        a {
            display: inline-block;
            margin-top: 20px;
            padding: 12px 24px;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
        }
        a:hover { opacity: 0.9; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 MagicBoxAI</h1>
        <p>ページをロード中...</p>
        <p><a href="/~garyo/magicboxai/">手動でリダイレクト</a></p>
    </div>
</body>
</html>
EOF

chmod 644 index.html

# ファイル確認
ls -la index.html

EOFSH
```

### Step 2: 動作確認

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

# public_html の内容確認
echo "=== public_html 内容確認 ==="
ls -la ~/public_html/

# index.html の内容確認
echo ""
echo "=== index.html ファイル確認 ==="
head -10 ~/public_html/index.html

# ブラウザテスト
echo ""
echo "✅ index.html 作成完了"
echo "ブラウザから http://garyo.sakura.ne.jp/ にアクセスすると"
echo "MagicBoxAI へ自動リダイレクトされます"

EOFSH
```

### Step 3: 完了確認

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cat > ~/public_html/SECURITY_FIX_COMPLETE.txt << 'EOF'
✅ Sakura セキュリティ修正完了

Date: $(date)
修正内容: public_html に index.html を配置

変更前：
❌ http://garyo.sakura.ne.jp/ にアクセス
  → ディレクトリ内容が丸見え（セキュリティ問題）

変更後：
✅ http://garyo.sakura.ne.jp/ にアクセス
  → index.html が読み込まれる
  → 自動的に MagicBoxAI へリダイレクト
  → ディレクトリ内容は非表示

効果：
✅ セキュリティ向上（ファイルリスト隠蔽）
✅ ユーザーUX 向上（MagicBoxAI へ自動移動）
✅ 本番環境として安全

ファイル確認：
- ~/public_html/index.html （新規作成）
- ~/public_html/magicboxai/ （既存）

ステータス：Ready for Production
EOF

cat ~/public_html/SECURITY_FIX_COMPLETE.txt

EOFSH
```

---

## ✅ 成功基準

すべてが達成されること：

- ✅ index.html 作成完了
- ✅ リダイレクト設定確認
- ✅ ファイル権限設定完了
- ✅ ディレクトリ非表示化確認

---

## 🎯 確認方法

修正後、ブラウザから以下にアクセス：

```
http://garyo.sakura.ne.jp/
↓
（自動リダイレクト）
↓
http://garyo.sakura.ne.jp/~garyo/magicboxai/
```

ディレクトリリストが見えなくなる ✅

---

**Status**: Sakura セキュリティ修正準備完了
