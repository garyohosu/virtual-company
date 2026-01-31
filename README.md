# Virtual Company 🏢

**AI 指示書管理 + MagicBoxAI 開発ハブ**

---

## ✨ What is Virtual Company?

Virtual Company は、以下の目的で運用されるリポジトリです：

1. **指示書の一元管理** - すべての指示書を `instructions/` に集約
2. **MagicBoxAI の開発ハブ** - PHP + CGI による HTML Paste & Share サービス
3. **AI CLI との統合** - Gemini / Codex / Claude が指示書を読んで実行

```
Virtual Company (指示書管理)
    ↓ (git pull)
Gemini CLI が instructions/*.md を読む
    ↓ (実行)
garyohosu/magic-box-ai リポジトリで実装
    ↓ (git push)
GitHub に反映
```

---

## 🎯 プロジェクト構成

### 1️⃣ MagicBoxAI - PHP + CGI 実装

**対象**: Sakura レンタルサーバー（PHP 7.4+）

```
garyohosu/magic-box-ai/
├── src/                      # PHP ソースコード
│   ├── index.php             # メイン（HTML Paste & Save）
│   ├── cron_cleanup.php      # 30日自動削除
│   ├── pages/home.php        # ホームページ
│   ├── .htaccess             # Apache 設定
│   ├── cgi-bin/              # CGI スクリプト
│   └── data/                 # データディレクトリ
│
├── tests/                    # テスト
│   ├── Unit/                 # PHPUnit
│   │   ├── IndexTest.php
│   │   └── CronCleanupTest.php
│   └── integration/          # pytest
│       ├── test_api_save.py
│       └── test_api_view.py
│
├── .github/workflows/        # CI/CD
│   ├── test-phpunit.yml      # PHPUnit 自動テスト
│   ├── test-pytest.yml       # pytest 自動テスト
│   └── deploy.yml            # Sakura へ自動デプロイ
│
├── composer.json             # PHPUnit 依存
├── phpunit.xml               # PHPUnit 設定
├── requirements.txt          # pytest 依存
├── pytest.ini                # pytest 設定
└── README.md
```

### 2️⃣ Virtual Company - 指示書管理

**目的**: すべての AI 指示書を一元管理

```
garyohosu/virtual-company/
├── instructions/             # 📍 すべての指示書がここ
│   ├── CLAUDE_MEMORY.md      # Claude の永続記憶ファイル
│   ├── MAGICBOXAI_FINAL_SETUP.md
│   ├── cleanup_organize_files.sh
│   ├── order_*.md            # 44+ ファイル
│   └── ... その他指示書
│
├── magicboxai/               # 開発ドキュメント
├── results/                  # 実行結果
├── Employees/                # 予約済み（未実装）
├── README.md                 # このファイル
└── ... その他
```

---

## 🚀 ワークフロー

### Step 1: Claude が指示書を作成
```bash
# GitHub MCP で virtual-company/instructions/ に作成
github:create_or_update_file
  ├─ owner: garyohosu
  ├─ repo: virtual-company
  ├─ path: instructions/FILENAME.md
  └─ branch: main
```

### Step 2: ユーザーが git pull
```bash
cd ~/garyohosu/virtual-company
git pull origin main
```

### Step 3: AI CLI が実行
```bash
# Gemini が指示書を読んで実行
cd ~/garyohosu/magic-box-ai
gemini --yolo ~/garyohosu/virtual-company/instructions/FILENAME.md

# または

codex --kick ~/garyohosu/virtual-company/instructions/FILENAME.md
```

### Step 4: 実行結果が反映
```bash
# magic-box-ai に変更が適用されて Git push される
cd ~/garyohosu/magic-box-ai
git log --oneline -1
# feat: Add PHP source, test suites, and CI/CD pipeline
```

---

## 📊 完了済みタスク

### ✅ MagicBoxAI Phase 1-4 完了

```
✅ Step 1: Python コード削除
   └─ virtual-company の magicboxai/ フォルダ空

✅ Step 2-2: PHP コード同期
   └─ src/, pages/, cron_cleanup.php 配置完了

✅ Step 3: テスト戦略実装
   └─ PHPUnit + pytest テスト環境完備

✅ Step 4: CI/CD ワークフロー設定
   └─ GitHub Actions 3つのワークフロー配置完了
      ├─ test-phpunit.yml
      ├─ test-pytest.yml
      └─ deploy.yml

✅ Step X: order*.md ファイル整理
   └─ 44+ ファイルを instructions/ に集約完了

✅ 永続記憶設定
   └─ CLAUDE_MEMORY.md で Claude の状態管理
```

### ⏳ 次のステップ

```
⏳ GitHub Secrets 設定（手動）
   ├─ SAKURA_HOST = garyo.sakura.ne.jp
   ├─ SAKURA_USER = garyo
   └─ SAKURA_KEY = SSH 秘密鍵

⏳ ローカルテスト（オプション）
   ├─ composer install
   ├─ ./vendor/bin/phpunit tests/Unit
   └─ pytest tests/integration -v

⏳ 本番デプロイ
   └─ GitHub Secrets 設定後、自動デプロイ開始
```

---

## 📂 ディレクトリ構造

### virtual-company （このリポジトリ）

```
virtual-company/
├── README.md                    ← 新（実態版）
├── instructions/                ← 📍 重要
│   ├── CLAUDE_MEMORY.md         # Claude の永続記憶
│   ├── MAGICBOXAI_FINAL_SETUP.md
│   ├── cleanup_organize_files.sh
│   ├── order_*.md               # 44+ ファイル
│   └── ... 指示書
├── magicboxai/                  # 設計・プランドキュメント
├── results/                     # 実行結果
├── Employees/                   # 予約済み（未実装）
├── Skills/                      # 予約済み（未実装）
└── ... その他
```

### magic-box-ai （実装リポジトリ）

```
magic-box-ai/
├── src/                         # PHP ソース
├── tests/                       # テスト
├── .github/workflows/           # CI/CD
├── composer.json                # PHPUnit
├── requirements.txt             # pytest
└── ... 設定ファイル
```

---

## 💡 Key Features

### ✅ 指示書の一元管理
- すべての `order*.md` / `instructions/*.md` を一箇所に集約
- Git で全履歴が保存される
- ユーザーが何をしたのか完全に可視化

### ✅ AI CLI との統合
```bash
# 複雑な指示もファイルに書いて実行するだけ
gemini --yolo instructions/order_name.md

# 指示ファイルの形式（Bash スクリプト）
#!/bin/bash
# Phase 1: ...
# Phase 2: ...
# Phase 3: ...
git add ...
git commit ...
git push ...
```

### ✅ テスト駆動開発
- PHPUnit: PHP 単体テスト
- pytest: API/CLI テスト
- GitHub Actions: 自動テスト & 自動デプロイ

### ✅ 完全な監査証跡
- すべての操作が Git に記録
- いつ、誰が、何をしたか明確
- 必要に応じてロールバック可能

---

## 🔄 Claude の永続記憶システム

### CLAUDE_MEMORY.md

```
重要な制約：
❌ Claude からはローカル PC が見えない
✅ 指示書は garyohosu/virtual-company/instructions/ に作成
✅ 忘れたときはこのファイルを参照

完了済み：
✅ Step 1-4: MagicBoxAI 完全実装
✅ Step X: order*.md ファイル整理
✅ 永続記憶設定
```

### 使用方法

```bash
# Claude が忘れそうになったら
cat https://raw.githubusercontent.com/garyohosu/virtual-company/main/instructions/CLAUDE_MEMORY.md

# 新しい指示書を作成する前に確認
# 常に instructions/ フォルダに作成
```

---

## 🛣️ Roadmap

### Phase 1: MagicBoxAI 開発 ✅ 完了

- [x] Python コード削除
- [x] PHP コード同期
- [x] テスト戦略実装
- [x] CI/CD 設定
- [x] 指示書整理

### Phase 2: 本番デプロイ ⏳ 進行中

- [ ] GitHub Secrets 設定（手動）
- [ ] ローカルテスト実行
- [ ] Sakura 自動デプロイ開始
- [ ] 本番環境確認

### Phase 3: 機能追加 ⏳ 予定

- [ ] UI/UX 改善
- [ ] ドメイン設定
- [ ] セキュリティ強化
- [ ] パフォーマンス最適化

### Phase 4: 拡張機能 ⏳ 予定

- [ ] Admin パネル
- [ ] 統計情報表示
- [ ] API 公開
- [ ] モバイル対応

---

## 📞 使い方

### 1. 新しい指示書を作成したい

```bash
# Claude が GitHub に直接作成
# 必ず以下のパスに作成：
# garyohosu/virtual-company/instructions/FILENAME.md
```

### 2. 指示書を実行したい

```bash
# ユーザーが git pull で取得
cd ~/garyohosu/virtual-company
git pull origin main

# AI CLI で実行
cd ~/garyohosu/magic-box-ai
gemini --yolo ~/garyohosu/virtual-company/instructions/FILENAME.md
```

### 3. 結果を確認したい

```bash
# GitHub で確認
https://github.com/garyohosu/magic-box-ai

# ローカルで確認
cd ~/garyohosu/magic-box-ai
git log --oneline -5
```

---

## 🎯 Philosophy

> **指示書 → 自動実行 → 検証 → 改善**

```
従来：
  手動実行 → エラー → 調査 → 修正 → 再実行

Virtual Company:
  指示書作成 → 自動実行 → テスト → 結果報告 → 改善
  （Git で全て記録）
```

---

## 📊 実装状態

| 項目 | 状態 | 詳細 |
|------|------|------|
| MagicBoxAI PHP 実装 | ✅ 完成 | src/, tests/, CI/CD 完備 |
| 指示書管理 | ✅ 完成 | 44+ ファイル整理完了 |
| Claude 永続記憶 | ✅ 完成 | CLAUDE_MEMORY.md で管理 |
| GitHub Actions CI/CD | ✅ 完成 | 3つのワークフロー設定 |
| **本番デプロイ** | ⏳ 進行中 | GitHub Secrets 設定待ち |
| **テスト実行** | ⏳ 進行中 | ローカルテスト準備中 |
| Employee System | 🔮 計画中 | 将来の拡張機能 |

---

## 🌟 特徴

✨ **AI 指示書駆動開発** - 複雑な操作をファイルに書いて実行  
✨ **完全な監査証跡** - すべてが Git に記録される  
✨ **自動テスト** - GitHub Actions が自動的にテスト実行  
✨ **自動デプロイ** - テスト成功で自動的に Sakura へデプロイ  
✨ **スケーラブル** - 複数の AI CLI に対応可能  

---

## 📞 Support

- **CLAUDE_MEMORY.md**: Claude の永続記憶＆制約条件
- **instructions/**: すべての指示書
- **GitHub Issues**: バグ報告・機能提案

---

## 📄 License

MIT License - 自由に使用・改変・配布可能

---

## 🎉 Ready to Go!

**Virtual Company** は指示書ベースの自動開発システムです。

1. 指示書を作成
2. AI CLI で実行
3. 結果を確認
4. Git に全て記録

**シンプルで、スケーラブルで、完全に自動化された開発フロー** 🚀

---

**Status**: 🟢 Phase 2 進行中  
**Latest Update**: 2026-01-31  
**Next Step**: GitHub Secrets 設定 → 本番デプロイ
