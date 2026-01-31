# Order - Sakura .htaccess で Indexes を完全に無効化

**Status**: ⏳ .htaccess 設定待ち
**Current Actor**: Codex（SSH 実行）
**Next Actor**: CEO（確認）

---

## 🎯 ミッション

Apache の Indexes 機能を完全に無効化して、
ディレクトリリストが見えないようにする

**方法**: `.htaccess` に `Options -Indexes` を設定

---

## 📋 実装

### Step 1: .htaccess 作成

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/public_html

# .htaccess を作成（Indexes を無効化）
cat > .htaccess << 'EOF'
Options -Indexes
EOF

# パーミッション設定
chmod 644 .htaccess

# ファイル確認
ls -la .htaccess

EOFSH
```

### Step 2: 設定確認

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/public_html

# .htaccess の内容確認
cat .htaccess

# 両方のファイルが存在するか確認
echo "=== public_html 確認 ==="
ls -la | grep -E "index.html|.htaccess"

EOFSH
```

### Step 3: 動作確認（外部ブラウザから）

**手動確認**:

ブラウザから以下にアクセス：
```
http://garyo.sakura.ne.jp/
```

**期待される結果**:
```
❌ ディレクトリリストが見えない
✅ index.html が読み込まれる
✅ MagicBoxAI へリダイレクト
```

### Step 4: 完了ログ

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cat > ~/public_html/HTACCESS_SETUP_COMPLETE.txt << 'EOF'
✅ .htaccess - Indexes 無効化完了

Date: $(date)
ファイル: ~/.htaccess

設定内容：
Options -Indexes

効果：
✅ ディレクトリリストが表示されない
✅ index.html が優先される
✅ ホームページへ自動リダイレクト

確認：
ブラウザから http://garyo.sakura.ne.jp/ にアクセス
→ MagicBoxAI へリダイレクト
→ ファイル一覧は見えない

セキュリティ状態：✅ 保護済み
EOF

cat ~/public_html/HTACCESS_SETUP_COMPLETE.txt

EOFSH
```

---

## ✅ 成功基準

- ✅ .htaccess 作成完了
- ✅ Options -Indexes 設定
- ✅ ディレクトリリスト非表示
- ✅ index.html へのリダイレクト確認

---

**Status**: .htaccess 設定準備完了
**難易度**: ⭐ 超低
**実行時間**: 1分
**成功確率**: 99%+
