# skills/sakura-deployment/URL_ROUTING.md

**対象**: Virtual Company の全 AI エージェント
**目的**: Sakura での正しい URL ルーティングを統一
**更新日**: 2026-01-31

---

## 🚨 重要な誤り発見

### 問題：`~garyo` プレフィックスの混同

```
❌ よくある間違い
https://garyo.sakura.ne.jp/~garyo/magicboxai/

✅ 正しい URL
https://garyo.sakura.ne.jp/magicboxai/
```

---

## 🔍 理由

### Sakura でのパス構成

```
ユーザーのホームディレクトリ: /home/garyo/
Webサーバーの公開フォルダ: /home/garyo/www/

つまり：
~/www/ = /home/garyo/www/
```

### URL と物理パスのマッピング

```
URL: http://garyo.sakura.ne.jp/magicboxai/
  ↓
物理パス: ~/www/magicboxai/
  ↓
実ファイル: /home/garyo/www/magicboxai/index.php
```

### `~garyo` を使う場合（異なる用途）

```
URL: http://garyo.sakura.ne.jp/~garyo/project/
  ↓
物理パス: ~/public_html/project/
  ↓
実ファイル: /home/garyo/public_html/project/index.html
```

**重要**: `~garyo` は `public_html` ディレクトリへのアクセス

---

## 📋 MagicBoxAI の正しい URL

| 用途 | URL | 物理パス |
|------|-----|---------|
| ホーム | `http://garyo.sakura.ne.jp/` | `~/www/index.html` |
| MagicBoxAI | `https://garyo.sakura.ne.jp/magicboxai/` | `~/www/magicboxai/` |
| API (健康診断) | `https://garyo.sakura.ne.jp/magicboxai/index.php/api/health` | `~/www/magicboxai/index.php` |
| 保存ファイル | `https://garyo.sakura.ne.jp/magicboxai/view/{token}` | `~/www/magicboxai/view.php` |

---

## ✅ すべての Order に追加すべき確認項目

Order 実行前に、**必ず確認**：

```bash
# 1. 物理パスの確認
ls -la ~/www/

# 2. 公開フォルダの確認
ls -la ~/www/magicboxai/

# 3. URL マッピング確認
echo "URL: https://garyo.sakura.ne.jp/magicboxai/"
echo "物理パス: ~/www/magicboxai/"
```

---

## 🎓 設計思想

```
Sakura のパス体系：
- ~/www/         → https://garyo.sakura.ne.jp/
- ~/public_html/ → https://garyo.sakura.ne.jp/~garyo/

MagicBoxAI は www/ に配置：
→ ~ プレフィックスは不要
→ 直接ドメイン配下
```

---

## 📝 Gemini の誤り

```
Gemini が生成した URL:
https://garyo.sakura.ne.jp/~garyo/magicboxai/

正しい URL:
https://garyo.sakura.ne.jp/magicboxai/

原因：
- Gemini が古い FastAPI パスを参考にした可能性
- PHP + CGI の new ファイル構成を理解していなかった

教訓：
- AI の出力は常に人間が検証すべき
- 環境特性の確認は重要
```

---

## 🚀 正しいテスト方法

```bash
# ブラウザでアクセス
https://garyo.sakura.ne.jp/magicboxai/

# API テスト
curl.exe -s https://garyo.sakura.ne.jp/magicboxai/index.php/api/health

# リダイレクト確認
curl.exe -I https://garyo.sakura.ne.jp/
  → /magicboxai/ へリダイレクトされるか
```

---

## 📚 参考：複数のディレクトリがある場合

```
~/www/           → https://garyo.sakura.ne.jp/
~/public_html/   → https://garyo.sakura.ne.jp/~garyo/
~/private/       → アクセス不可（非公開）

各ディレクトリの URL:
- ~/www/app1/        → https://garyo.sakura.ne.jp/app1/
- ~/www/app2/        → https://garyo.sakura.ne.jp/app2/
- ~/public_html/old/ → https://garyo.sakura.ne.jp/~garyo/old/
```

---

**これが「自己学習する組織」の価値です。** ✨

ユーザーの指摘 → Skill 更新 → 全 AI が学習 → 二度と起きない
