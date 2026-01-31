# Virtual Company 🏢

**AI 部下システム：失敗を学習して自己改革する組織**

---

## ✨ What is Virtual Company?

Virtual Company は、**複数の AI ツール（Claude, Gemini, Codex）が連携して、失敗から学び、成長し続けるシステム**です。

```
指示書作成（Claude.ai）
     ↓
GitHub に保存
     ↓
Gemini CLI が pull して実行
     ↓
結果をレポート
     ↓
次のステップに進む
```

---

## 🎯 システム構成（3層）

### 1️⃣ Instruction Layer（指示書層）
```
garyohosu/virtual-company/instructions/
├── CLAUDE_MEMORY.md              # Claude の永続記憶
├── MAGICBOXAI_FINAL_SETUP.md     # MagicBoxAI セットアップ
├── cleanup_organize_files.sh     # 自動クリーンアップ
├── order_magicboxai_*.md         # MagicBoxAI 関連の指示
├── order_sakura_*.md             # Sakura デプロイ指示
└── ... 50+ 指示書
```

**特徴**:
- すべての指示書が GitHub に集約
- Gemini CLI で実行可能な形式
- 失敗パターンを記録・改善

### 2️⃣ Project Layer（プロジェクト層）

#### MagicBoxAI（PHP 版）
```
garyohosu/magic-box-ai/
├── src/                          # PHP ソースコード
│   ├── index.php                 # メイン
│   ├── cron_cleanup.php          # 30日自動削除
│   ├── .htaccess                 # Apache 設定
│   └── pages/
│
├── tests/
│   ├── Unit/                     # PHPUnit テスト
│   └── integration/              # pytest API テスト
│
├── .github/workflows/            # CI/CD
│   ├── test-phpunit.yml
│   ├── test-pytest.yml
│   └── deploy.yml
│
├── composer.json                 # PHPUnit 依存
├── phpunit.xml                   # PHPUnit 設定
├── requirements.txt              # pytest 依存
└── pytest.ini                    # pytest 設定
```

**特徴**:
- PHP + CGI（Sakura レンタルサーバー対応）
- PHPUnit + pytest 両対応テスト
- GitHub Actions で自動テスト＆デプロイ

### 3️⃣ Memory Layer（記憶層）

```
garyohosu/virtual-company/
├── Employees/                    # AI 従業員フォルダ
│   ├── alice/
│   │   ├── WhoAmI.md             # 身分証
│   │   ├── Skills.md             # 失敗パターン学習
│   │   ├── order_alice_*.md      # Alice 用指示書
│   │   └── Mail/
│   │       ├── inbox/
│   │       └── outbox/
│   ├── bob/
│   └── charlie/
│
├── instructions/                 # 指示書集約
├── skills/                       # スキル・パターン
├── tasks/                        # タスク管理
└── results/                      # 実行結果
```

**特徴**:
- 完全な永続記憶
- 失敗パターンを自動記録
- メール（ファイルベース）で通信

---

## 🔄 ワークフロー

### 実行フロー

```
① Claude.ai が指示書を作成
   ↓
② GitHub に instructions/ に登録
   ↓
③ ユーザーが git pull
   ↓
④ Gemini CLI で実行
   gemini --yolo instructions/FILENAME.md
   ↓
⑤ 実行結果をレポート
   ↓
⑥ Claude が次のステップ作成
```

### 失敗学習フロー

```
実行 → 失敗検出 → Skills.md に記録
  ↓
パターン分析 → CLAUDE_MEMORY.md 更新
  ↓
次回実行時に自動回避
  ↓
Success!
```

---

## 📊 実装状態

| 項目 | 状態 | 説明 |
|------|------|------|
| **指示書システム** | ✅ 完了 | 50+ 指示書が instructions/ に集約 |
| **MagicBoxAI** | ✅ 完了 | PHP版完全実装（テスト含む） |
| **テスト戦略** | ✅ 完了 | PHPUnit + pytest 両対応 |
| **CI/CD** | ✅ 完了 | GitHub Actions 3ワークフロー |
| **永続記憶** | ✅ 完了 | CLAUDE_MEMORY.md 実装 |
| **Employee System** | ⏳ 進行中 | Alice まで完成、Bob/Charlie は予定 |
| **Mail System** | ⏳ 計画中 | ファイルベースメール |
| **CLI実装** | ✅ 稼働中 | Gemini CLI で実行可能 |
| **自動デプロイ** | ⏳ 手動 | GitHub Secrets 設定後に自動化 |

---

## 🚀 使い方

### ステップ 1: 指示書を取得
```bash
cd ~/garyohosu/virtual-company
git pull origin main
```

### ステップ 2: 指示書を確認
```bash
cat instructions/MAGICBOXAI_FINAL_SETUP.md
cat instructions/CLAUDE_MEMORY.md
```

### ステップ 3: Gemini で実行
```bash
cd ~/garyohosu/magic-box-ai
gemini --yolo ~/garyohosu/virtual-company/instructions/MAGICBOXAI_FINAL_SETUP.md
```

### ステップ 4: 結果確認
```bash
git log --oneline -3
git status
```

---

## 📂 リポジトリ構成

### virtual-company（メインリポジトリ）
```
virtual-company/
├── instructions/                      # 📋 すべての指示書（50+）
│   ├── CLAUDE_MEMORY.md               # 🧠 Claude 永続記憶
│   ├── MAGICBOXAI_FINAL_SETUP.md      # 🎯 最終セットアップ
│   ├── cleanup_organize_files.sh      # 🧹 自動クリーンアップ
│   ├── order_magicboxai_*.md
│   ├── order_sakura_*.md
│   └── ... 40+ その他
│
├── Employees/                         # 👥 AI従業員
│   ├── alice/
│   │   ├── WhoAmI.md
│   │   ├── Skills.md
│   │   ├── Mail/
│   │   └── order_*.md
│   ├── bob/
│   └── charlie/
│
├── magicboxai/                        # レガシー（削除予定）
├── skills/                            # スキルパターン
├── tasks/                             # タスク
├── results/                           # 実行結果
├── scripts/                           # 自動化スクリプト
├── tests/                             # テスト
├── README.md                          # ← ここ
└── ... その他
```

### magic-box-ai（MagicBoxAI 実装）
```
magic-box-ai/
├── src/                               # 🐘 PHP ソース
│   ├── index.php                      # メイン実装
│   ├── cron_cleanup.php               # 30日自動削除
│   ├── pages/
│   ├── cgi-bin/
│   └── data/
│
├── tests/                             # 🧪 テスト
│   ├── Unit/                          # PHPUnit
│   │   ├── IndexTest.php
│   │   └── CronCleanupTest.php
│   └── integration/                   # pytest
│       └── test_api_save.py
│
├── .github/workflows/                 # ⚙️ CI/CD
│   ├── test-phpunit.yml               # PHPUnit 自動テスト
│   ├── test-pytest.yml                # pytest 自動テスト
│   └── deploy.yml                     # Sakura 自動デプロイ
│
├── composer.json                      # PHPUnit 依存
├── phpunit.xml                        # PHPUnit 設定
├── requirements.txt                   # pytest 依存
└── pytest.ini                         # pytest 設定
```

---

## 🎯 フェーズ

### Phase 1: 基本システム（✅ 完了）
- [x] 指示書システム（instructions/ 集約）
- [x] MagicBoxAI 実装（PHP版）
- [x] テスト戦略（PHPUnit + pytest）
- [x] CI/CD パイプライン（GitHub Actions）
- [x] 永続記憶（CLAUDE_MEMORY.md）
- [x] Gemini CLI 実行可能

### Phase 2: Employee System（⏳ 進行中）
- [x] Alice フォルダ構成
- [ ] Bob フォルダ実装
- [ ] Charlie フォルダ実装
- [ ] 従業員間通信

### Phase 3: Mail System（⏳ 計画中）
- [ ] ファイルベースメール
- [ ] 既読マーク機能
- [ ] 返信追跡
- [ ] 自動修復

### Phase 4: 本運用（⏳ 予定）
- [ ] GitHub Secrets 設定
- [ ] 自動デプロイ開始
- [ ] 複数従業員運用
- [ ] 完全自動化

---

## 💡 Key Features

### ✅ 指示書の集約化
- すべての指示書が `instructions/` に集約
- Gemini CLI で直接実行可能
- 履歴が GitHub に永続化

### ✅ PHP + テスト完全対応
- PHPUnit で PHP 単体テスト
- pytest で API テスト
- 両者が独立して動作

### ✅ CI/CD の完全自動化
- GitHub Actions で自動テスト
- テスト成功時に Sakura にデプロイ
- Secrets 設定後はすべて自動

### ✅ 永続記憶システム
- CLAUDE_MEMORY.md で指示書作成ルール記録
- ユーザー記憶機能で重要情報保持
- 忘れずに常に同じ場所に指示書を作成

### ✅ Gemini CLI 統合
- `gemini --yolo instructions/FILENAME.md` で実行
- order*.md ファイルもすべて実行可能

---

## 🔧 セットアップ

### 前提条件
- Git
- GitHub アカウント
- Gemini CLI（garyohosu の環境）
- PHP 7.4+
- Composer
- Python 3.10+

### インストール

```bash
# 1. virtual-company をクローン
git clone https://github.com/garyohosu/virtual-company.git
cd virtual-company

# 2. 最新の指示書を pull
git pull origin main

# 3. magic-box-ai をクローン（別ディレクトリ）
cd ../
git clone https://github.com/garyohosu/magic-box-ai.git
cd magic-box-ai

# 4. 指示書を実行
gemini --yolo ../virtual-company/instructions/MAGICBOXAI_FINAL_SETUP.md

# 5. GitHub Secrets を設定（手動）
# Settings > Secrets and variables > Actions
# - SAKURA_HOST = garyo.sakura.ne.jp
# - SAKURA_USER = garyo
# - SAKURA_KEY = (SSH private key)
```

---

## 📊 ワークフロー例

### Example 1: 指示書を新しく作成
```
① Claude が github:create_or_update_file を実行
② garyohosu/virtual-company/instructions/ に保存
③ メッセージで報告
④ ユーザーが git pull
⑤ gemini --yolo で実行
```

### Example 2: テストを実行
```bash
# ローカル PHPUnit
cd ~/garyohosu/magic-box-ai
composer install
./vendor/bin/phpunit tests/Unit

# ローカル pytest
pip install -r requirements.txt
pytest tests/integration -v

# GitHub Actions（自動）
git push origin main
# → test-phpunit.yml 実行
# → test-pytest.yml 実行
# → すべて成功したら deploy.yml 実行
```

---

## 📈 スケーリング

```
単一実行:
  Claude → 指示書 → Gemini → 実行

複数従業員:
  Claude → 指示書 → Gemini → Alice 実行
                  ↓
                  → Gemini → Bob 実行
                  ↓
                  → Gemini → Charlie 実行

組織全体:
  各従業員が独立して実行
  + Employee System で記憶共有
  + Mail System で通信
  + 自動修復
```

---

## 🌟 今後の展開

```
現在: 
  ✅ 指示書自動生成 + 実行
  ✅ 単一プロジェクト管理

3ヶ月後:
  + Employee System 複数従業員
  + Mail System 実装
  + 失敗パターン自動学習

6ヶ月後:
  + 複数プロジェクト同時管理
  + 自動修復機能
  + 組織全体の知見共有

1年後:
  + 完全自動化
  + Expert レベル進化
  + 自己改革システム完成
```

---

## 🎓 ドキュメント

| ファイル | 説明 |
|---------|------|
| **CLAUDE_MEMORY.md** | 🧠 Claude 用永続記憶 |
| **MAGICBOXAI_FINAL_SETUP.md** | 🎯 MagicBoxAI セットアップ |
| **cleanup_organize_files.sh** | 🧹 指示書整理スクリプト |
| **order_*.md** | 📋 各種指示書（50+） |

---

## 📞 トラブルシューティング

### Q: 指示書の場所がわからない
**A**: `garyohosu/virtual-company/instructions/` を確認

### Q: 指示書を新しく作成したい
**A**: GitHub に `instructions/` 内に作成

### Q: Gemini で実行方法
**A**: `gemini --yolo instructions/FILENAME.md`

### Q: テスト結果を見たい
**A**: GitHub Actions の Workflows タブを確認

---

## 🎯 Philosophy

> **失敗から学び、成長し続ける組織**

```
従来型:
  指示 → 実行 → 完了

Virtual Company:
  指示（GitHub） → 実行（Gemini）
                → 失敗検出
                → 学習（Memory）
                → 予防
                → 次の指示（改善版）
                → 実行（成功）
```

---

## 💬 Quick Start

```bash
# 1. リポジトリをクローン
git clone https://github.com/garyohosu/virtual-company.git
cd virtual-company

# 2. 指示書を確認
cat instructions/CLAUDE_MEMORY.md

# 3. MagicBoxAI セットアップ
cd ../magic-box-ai
git pull origin main

# 4. テスト実行
composer install
./vendor/bin/phpunit tests/Unit

# 5. デプロイ（Secrets 設定後）
git push origin main
# → GitHub Actions で自動テスト＆デプロイ
```

---

## 📄 License

MIT License - 自由に使用・改変・配布可能

---

## 🎉 Ready to Go!

**Virtual Company** は「AI が失敗から学び、成長する組織」です。

- 指示書を作成して（Claude）
- 実行して（Gemini）
- 失敗から学んで（Memory）
- 改善して（Next Order）
- 成長させてください（Expert）

**1年後、あなたの AI システムは Expert に進化しています。** 🚀

---

**Created**: 2025-01-30  
**Latest Update**: 2025-01-31  
**Status**: 🟢 Production Ready  
**Phase**: Phase 1 ✅ + Phase 2 ⏳

[詳細は instructions/CLAUDE_MEMORY.md を参照](https://github.com/garyohosu/virtual-company/blob/main/instructions/CLAUDE_MEMORY.md)
