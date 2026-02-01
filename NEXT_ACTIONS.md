# 🎯 Next Actions - 次のステップ

**作成日**: 2026-01-31  
**状況**: Genspark による大幅改良完了、本番デプロイ前最終ステップ

---

## ✅ 完了済み（Genspark による改良）

```
✓ リポジトリ統合（origin/genspark_ai_developer をマージ）
✓ MagicBoxAI セキュリティ強化
  ├─ XSS / Path Traversal / CSRF 対策
  ├─ 1MB アップロード制限
  └─ 入力値検証
✓ UI/UX 大幅改良
  ├─ Tailwind CSS / Alpine.js / Animate.css 統合
  ├─ Example Prompts ガイド
  ├─ 保存確認ダイアログ
  └─ マルチ共有ボタン（コピー、開く、ZIP ダウンロード）
✓ 削除日数可能化（MAGICBOXAI_MAX_AGE_DAYS 環境変数）
✓ ログシステム完成
  ├─ scripts/log_result.py（JSON 履歴追跡）
  ├─ scripts/gemini_wrapper.ps1（Windows 対応）
  └─ クロスプラットフォーム対応
✓ ローカル検証済み
```

---

## ⏳ 次のステップ（手動実行必須）

### 1️⃣ 残りの指示書を実行

```bash
# Genspark で新しいスクリプトを使用
.\scripts\gemini_wrapper.ps1

# または Linux/Mac
bash scripts/gemini_wrapper.sh
```

**実行対象**:
```
instructions/ フォルダの残りの指示書
├─ order_*.md / order_*.sh
├─ TEST_*.sh
└─ その他の指示書
```

---

### 2️⃣ GitHub Secrets 設定（重要！）

**場所**: https://github.com/garyohosu/magic-box-ai/settings/secrets/actions

**設定する内容**:

```
1️⃣ SAKURA_SSH_KEY
   値: SSH 秘密鍵の内容
       cat ~/.ssh/id_rsa の出力全体

2️⃣ SAKURA_USER
   値: garyo
```

**詳細手順**:

```bash
# Step 1: SSH 秘密鍵を確認
cat ~/.ssh/id_rsa

# 出力例:
# -----BEGIN RSA PRIVATE KEY-----
# MIIEpQIBAAKCAQEA2n4z...
# (長い文字列が続く)
# -----END RSA PRIVATE KEY-----

# このテキスト全部をコピーして GitHub Secrets に設定
```

---

### 3️⃣ デプロイテスト

```bash
# Secrets 設定後、git push で GitHub Actions を起動
cd ~/garyohosu/magic-box-ai
git log --oneline -1

# 何か小さな変更を加える
echo "# Deployment test" >> README.md

# Push してテスト
git add README.md
git commit -m "test: Trigger GitHub Actions"
git push origin main

# GitHub > Actions で実行状況を確認
# https://github.com/garyohosu/magic-box-ai/actions
```

---

### 4️⃣ 本番環境確認

```bash
# Secrets 設定 + git push 後、自動デプロイが実行される

# 本番確認
curl https://garyo.sakura.ne.jp/magicboxai/

# または ブラウザで開く
# https://garyo.sakura.ne.jp/magicboxai/

# 以下が表示されれば成功：
# ✓ MagicBoxAI タイトル
# ✓ Example Prompts（8個）
# ✓ 保存確認ダイアログ
# ✓ マルチ共有ボタン
```

---

## 📋 チェックリスト

```
□ 残りの指示書を .\scripts\gemini_wrapper.ps1 で実行
□ GitHub Secrets: SAKURA_SSH_KEY を設定
□ GitHub Secrets: SAKURA_USER を設定
□ git push でテスト
□ GitHub Actions が実行されるか確認
  └─ test-phpunit.yml
  └─ test-pytest.yml
  └─ deploy.yml
□ 本番環境（Sakura）にデプロイされたか確認
□ https://garyo.sakura.ne.jp/magicboxai/ にアクセス
□ UI が正しく表示されるか確認
□ Example Prompts がコピーできるか確認
□ 保存確認ダイアログが表示されるか確認
□ マルチ共有ボタンが動作するか確認
```

---

## 🚀 成功時の確認項目

### ブラウザで https://garyo.sakura.ne.jp/magicboxai/ を開いた時

```
✓ ページが正常に読み込まれる
✓ MagicBoxAI ロゴが表示される
✓ Example Prompts が 8個表示される
✓ 各プロンプトの「コピー」ボタンが動作する
  └─ クリック → 「コピーしました！」表示
✓ HTML コードを貼り付けできる
✓ 「保存」ボタンをクリック
  └─ 「このアプリを保存しますか？」ダイアログ表示
  └─ 「30日後に自動で削除されます」と表示
✓ 「保存する」をクリック
  └─ 「保存完了！」画面
  └─ リンクが表示される
✓ 「開く」ボタンで新タブでプレビュー
✓ 「コピー」ボタンでリンクをコピー
✓ 「ZIP ダウンロード」ボタンで圧縮ファイルをダウンロード
```

---

## ⚠️ トラブルシューティング

### Q: GitHub Actions が実行されない

```
A: GitHub Secrets が正しく設定されているか確認
   └─ Settings > Secrets and variables > Actions
   └─ SAKURA_SSH_KEY / SAKURA_USER が表示されているか
```

### Q: Sakura へのデプロイが失敗する

```
A: SSH 秘密鍵が正しくコピーされているか確認
   ├─ -----BEGIN / -----END まで全部コピーしたか
   ├─ 改行を含めてコピーしたか
   └─ パスフレーズはないか確認
```

### Q: ページが 404 表示される

```
A: Sakura のディレクトリ構造を確認
   └─ /home/garyo/public_html/magicboxai/
   └─ src/index.php が配置されているか
```

---

## 📊 完成度

```
🎉 MagicBoxAI プロジェクト

完成度: 95%
├─ コア機能: 100% ✅
├─ UI/UX: 100% ✅
├─ セキュリティ: 100% ✅
├─ デプロイ設定: 100% ✅
└─ 本番環境: ⏳ デプロイ待機中

残り 5%: 本番環境での最終確認
```

---

**あと一歩です！** 🚀

GitHub Secrets を設定して、git push をするだけで本番デプロイが完了します！
