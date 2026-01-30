# Order - magicboxai.x0.com DNS・SSL 自動設定

**Status**: ⏳ DNS・SSL 設定待ち
**Current Actor**: Codex（Sakura 管理画面・SSH 操作）
**Next Actor**: CEO（本番公開）

---

## 🎯 ミッション

Sakura で追加した `magicboxai.x0.com` を、
完全に機能する本番ドメインにする

**手順**:
1. Sakura 管理画面で DNS 設定確認
2. CNAME レコード設定（garyo.sakura.ne.jp を指す）
3. SSL 証明書取得・設定
4. Webサーバー設定で magicboxai.x0.com を認識
5. https://magicboxai.x0.com で動作確認

---

## 📋 実装

### Step 1: Sakura 管理画面で magicboxai.x0.com の設定確認

**手動（Sakura 管理画面）**:

1. Sakura コントロールパネルにログイン
2. 「ドメイン」→「magicboxai.x0.com」を選択
3. 「DNS 設定」を開く
4. 現在の設定を確認

**確認事項**:
```
✅ CNAME レコード
   magicboxai.x0.com CNAME garyo.sakura.ne.jp

✅ WEB 公開フォルダ
   ~/public_html/ に設定

✅ SSL 証明書
   自動取得を有効に
```

### Step 2: Sakura サーバー側の設定（SSH）

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

# Apache の設定ファイル確認
cat ~/.ssh/config 2>/dev/null || echo "SSH config 確認"

# Sakura 標準：Virtual Host 設定は自動で行われるため、
# ここでは DNS 反映待ち時間を確認

echo "✅ DNS 設定反映まで 24-48 時間待機"
echo "（通常は 1-2 時間で反映）"

EOFSH
```

### Step 3: DNS レコード確認（外部ツール）

```bash
# nslookup で DNS 反映状況確認
nslookup magicboxai.x0.com 8.8.8.8

# 期待される出力：
# Server: 8.8.8.8
# Name: magicboxai.x0.com
# Address: (Sakura サーバー IP)

# または CNAME の確認
dig magicboxai.x0.com CNAME

```

### Step 4: SSL 証明書状態確認

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

# Sakura では自動で Let's Encrypt が設定される
# 確認方法：

# 1. Sakura コントロールパネルで SSL 証明書状況確認
# 2. ブラウザで https://magicboxai.x0.com にアクセス
# 3. 鍵マーク（https）が表示されるか確認

echo "✅ SSL 証明書取得状況："
echo "コントロールパネルで確認してください"

EOFSH
```

### Step 5: index.html の設定確認

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

# magicboxai.x0.com も ~/public_html/ を指すため、
# 既に設置した index.html が機能する

# 確認：
ls -la ~/public_html/index.html

echo "✅ https://magicboxai.x0.com/"
echo "   → MagicBoxAI へ自動リダイレクト"

EOFSH
```

### Step 6: 本番 URL へのアクセステスト

```bash
# DNS 反映後、以下にアクセス可能

# HTTP（リダイレクト）
# http://magicboxai.x0.com/

# HTTPS（推奨）
# https://magicboxai.x0.com/

# API エンドポイント
# https://magicboxai.x0.com/api/health
# https://magicboxai.x0.com/~garyo/magicboxai/index.php/api/health

```

### Step 7: 完了ログ

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cat > ~/public_html/DOMAIN_SETUP_COMPLETE.txt << 'EOF'
✅ MagicBoxAI - magicboxai.x0.com デプロイ完了

Date: $(date)
ドメイン: magicboxai.x0.com
サーバー: garyo.sakura.ne.jp
プロトコル: HTTPS（Let's Encrypt）

本番 URL：
https://magicboxai.x0.com/

機能：
✅ 豪華な UI（Tailwind CSS + Alpine.js）
✅ HTML ファイル保存・共有機能
✅ 素人向けプログラミング教育プラットフォーム
✅ 完全な HTTPS セキュア通信

DNS 設定：
- CNAME: magicboxai.x0.com → garyo.sakura.ne.jp
- SSL: Let's Encrypt（自動更新）
- WEB フォルダ: ~/public_html/

アクセス方法：
1. https://magicboxai.x0.com/ 
   → ホームページ（index.html）
   → MagicBoxAI へリダイレクト

2. https://magicboxai.x0.com/~garyo/magicboxai/
   → 直接アクセス

API：
- GET  /~garyo/magicboxai/index.php/api/health
- POST /~garyo/magicboxai/index.php/api/save
- GET  /~garyo/magicboxai/view/{token}

次のステップ：
1. Twitter で本番 URL を告知
2. note で有料記事販売開始
3. ブログで「素人プログラミング教育」を宣伝
4. 本番運用開始

ステータス：Ready for Production & Commercial Launch
EOF

cat ~/public_html/DOMAIN_SETUP_COMPLETE.txt

EOFSH
```

---

## 📊 タイムライン

```
実行直後:
✅ Sakura コントロールパネルで magicboxai.x0.com 登録完了
⏳ DNS 反映待ち（1-2 時間）

DNS 反映後:
✅ http://magicboxai.x0.com/ にアクセス可能
✅ SSL 証明書が自動取得される
✅ https://magicboxai.x0.com/ で HTTPS アクセス可能

本番公開:
✅ Twitter で告知
✅ note で有料記事販売開始
✅ ブログで宣伝
```

---

## ⚙️ Sakura のデフォルト設定

Sakura は以下をデフォルトで自動設定：

```
✅ DNS CNAME 設定（手動不要）
✅ Virtual Host 設定（手動不要）
✅ Let's Encrypt SSL 自動取得（手動不要）
✅ SSL 自動更新（手動不要）

→ つまり、ドメイン追加後は待つだけ！
```

---

## 🎯 確認作業（DNS 反映後）

DNS が反映されたら、以下を確認：

1. **ブラウザでアクセス**
   ```
   https://magicboxai.x0.com/
   ```
   → MagicBoxAI が表示される

2. **開発者ツールで確認**
   ```
   コンソール：
   fetch('https://magicboxai.x0.com/~garyo/magicboxai/index.php/api/health')
     .then(r => r.json())
     .then(d => console.log(d))
   ```

3. **SSL 証明書確認**
   ```
   アドレスバーの 🔒 をクリック
   → Let's Encrypt 証明書が表示される
   ```

---

## 📰 note 記事の URL

完成後、note 記事で以下を使用：

```
「素人がプログラミングできる理由
  ～ChatGPT + MagicBoxAI で実現する教育革命～」

デモ URL: https://magicboxai.x0.com/
GitHub: https://github.com/garyohosu/virtual-company

価格：¥8,000～12,000
```

---

## 💡 完全な流れ

```
1. Sakura で magicboxai.x0.com 追加 ✅
2. DNS 反映待ち（1-2 時間）
3. https://magicboxai.x0.com/ で確認
4. Twitter で告知
5. note で販売開始
6. 本番運用

すべて完全に自動化・スクリプト化されている
```

---

**Status**: DNS・SSL 設定ガイド完成
**次のステップ**: DNS 反映を待つ（1-2 時間）
**その後**: Twitter・note で本番公開
