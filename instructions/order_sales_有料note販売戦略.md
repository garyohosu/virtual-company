# Order - Sales 部門：有料note販売戦略 + ブログ宣伝

**Status**: ⏳ 実行待ち
**Current Actor**: Sales 部門
**Next Actor**: (完了時)

---

## 🎯 ミッション

MagicBoxAI の成功を note 有料記事として販売し、
garyohosu.github.io で宣伝ページを作成して、最大の売上を獲得します。

---

## 📋 タスク 1: 有料note販売戦略

### 1.1 記事企画書作成

`results/sales/NOTE_ARTICLE_PLAN.md` を作成：

```markdown
# note 有料記事企画書

## 記事タイトル（案3つ）

1. 「AIエージェントで一人起業ができた。ChatGPT 3年間では不可能だった『完全自動化』の実装記録」
2. 「月1万円のAI課金で『仮想会社』を実装。その実験結果と『一人起業』の可能性」
3. 「素人がプログラミングできる『MagicBoxAI』を作った話。AIが自動で会社を動かすシステム」

## 想定読者

- AI興味ある起業志望者（20-50代）
- エンジニア・リーダー層
- AI ツール使いこなせる層
- 「一人起業」に興味ある人

## 価格設定

### 推奨価格: ¥5,000～10,000

根拠：
- 高度な専門知識：¥5,000以上
- 実装記録で再現可能：¥10,000まで可能
- 市場相場：AI関連記事の平均 ¥3,000～8,000

### 販売予測

価格 ¥5,000：
- 初月：50～100部
- 売上：¥250,000～500,000

価格 ¥8,000：
- 初月：30～50部
- 売上：¥240,000～400,000

## 販売スケジュール

- 企画確定：今週
- 執筆：1週間
- 宣伝期間：3日
- 販売開始：2週間以内

## note での宣伝文（プレビュー版）

```
「月1万円のAI課金で、本当に『一人起業』ができるのか」

3年間 ChatGPT を使ってきた私が、
「Claude + Codex CLI」に乗り換えた。

結果？

完全に自動化された「AI従業員だけの仮想会社」が誕生。

MagicBoxAI という事業も実装できた。

ChatGPT では不可能だった「完全自動化」。
その実装記録を、すべて公開します。

- 設計から本番デプロイまで
- 失敗と解決策
- 月1万円で何ができるか
- 一人起業は本当に可能か

実装コード・ドキュメント・思考プロセスまで、
すべて GitHub で追跡可能。

再現可能、実装可能、あなたの参考になる記事です。
```

## 販売チャネル

- note（メイン）：https://note.com/garyohosu
- Twitter/X：宣伝ツイート
- GitHub.io：詳細ページ
- 知人ネットワーク：口コミ

## KPI

- 目標販売数（初月）：50部以上
- 目標売上（初月）：¥250,000以上
- リピート率：30%以上（継続記事販売）
```

---

## 📋 タスク 2: Twitter/X 宣伝文作成

`results/sales/TWITTER_PROMOTION.md` を作成：

```markdown
# Twitter/X 宣伝ツイート群

## ツイート 1: 興味喚起

【速報】ChatGPT 3年間できなかったことを、Claude + AI エージェントで実現した。

月1万円のAI課金で「AI従業員だけの仮想会社」を実装。
MagicBoxAI という事業も完全自動化で構築。

その全実装記録を note で販売開始。
再現可能、追跡可能。

#AI #起業 #自動化

---

## ツイート 2: 詳細・認知

「一人起業」ってホントに可能？

実装してみました。

- Virtual Company（仮想会社システム）
- Kick System（自動実行）
- MagicBoxAI（事業実装）
- note（販売）

すべて GitHub に記録。
すべて再現可能。

この記録が有料記事に。

#AIエージェント #起業 #GitHub

---

## ツイート 3: CTA（Call to Action）

note 記事が販売開始になりました。

「AI エージェントで一人起業ができた」

月1万円のAI課金で何ができるか。
ChatGPT では何ができなかったか。
すべて記録しました。

¥5,000～

link: https://note.com/...

#note #AI #起業

---

## ツイート 4: 後日追い

「素人がプログラミングできるサービス」も実装した。

MagicBoxAI = HTML 貼り付けたら動く note

初心者向けプログラミング教育。
自動削除で法的リスク最小。

この発想も note 記事に。

#MagicBoxAI #プログラミング教育
```

---

## 📋 タスク 3: Sakura サーバー デプロイ戦略

`results/sales/SAKURA_DEPLOYMENT.md` を作成：

```markdown
# Sakura レンタルサーバー デプロイ計画

## サーバースペック確認

- CPU、メモリ、ディスク容量
- Python 対応状況（FastAPI 実行可能か）
- DB 対応状況（SQLite OK か、MySQL 可能か）

## デプロイ方法

### オプション 1: WSGI アプリとして Sakura に配置
```bash
git clone https://github.com/garyohosu/magic-box-ai.git
pip install -r requirements.txt
gunicorn magicboxai.main:app
```

### オプション 2: Docker + Sakura VPS
Sakura VPS なら Docker で実行可能

### オプション 3: 静的ファイル + API

- フロント：静的ホスティング（GitHub Pages 使用可）
- API：Sakura サーバーで実行

## 本番 URL

```
https://magicboxai.example.com
```

（DNS: Sakura サーバーのネームサーバー指定）

## SSL 証明書

Sakura の無料 SSL or Let's Encrypt で対応

## バックアップ・運用

- 日次バックアップ
- エラーログ監視
- アクセスログ記録
```

---

## 📝 成果物

実行後、以下が生成されること：

```
results/sales/
├── NOTE_ARTICLE_PLAN.md（企画書）
├── TWITTER_PROMOTION.md（ツイート群）
├── SAKURA_DEPLOYMENT.md（デプロイ計画）
├── SALES_EXECUTION_LOG.md
└── RESULT.md
```

---

## ✅ 成功基準

- ✅ note 記事企画書完成
- ✅ 価格設定・販売予測決定
- ✅ Twitter/X ツイート案 5-10 個
- ✅ Sakura デプロイ計画完成
- ✅ すべて GitHub に記録

---

## 🎯 Next Step

この Sales 部門の後、Engineering / QA / Ops が実装を完了し、
その後あなたが note で記事を販売開始。

---

**Status**: Sales 部門 実行準備完了
