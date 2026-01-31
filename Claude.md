# 👤 Claude - AI エージェント設定

**対象**: Claude Haiku 4.5（claude.ai）  
**作成日**: 2026-01-31  
**目的**: Claude が Virtual Company 内で従うべきルール

---

## 🎯 Claude の責務

### ✅ やるべきこと

```
1️⃣ 指示書の作成
   └─ garyohosu/virtual-company/instructions/ に作成
   └─ GitHub MCP で操作

2️⃣ 概要の提供
   └─ 作成した指示書の概要を説明
   └─ ユーザーに報告

3️⃣ 仕様の説明
   └─ 何をするのかを明確に記述
   └─ 期待される結果を説明
```

### ❌ してはいけないこと

```
❌ ローカル PC のファイルを操作
❌ GitHub 以外の場所に指示書を保存
❌ 実行内容を確認しないで記述
❌ instructions/ 以外に作成
❌ Bash スクリプト以外の形式で複雑な処理を記述
```

---

## 📝 指示書作成のテンプレート

### ✅ 良い指示書

```bash
#!/bin/bash
# 明確なタイトル

set -e

echo "🎯 何をするのか明確に示す"
echo ""

# Step 1
echo "Step 1️⃣: xxx"
# 処理

# Step 2
echo "Step 2️⃣: xxx"
# 処理

# Step 3
echo "Step 3️⃣: xxx"
# 処理

echo ""
echo "✅ 完了"
echo ""
echo "📝 結果:"
echo "  - xxx が完了"
echo "  - yyy が更新"
```

### ❌ 悪い指示書

```bash
#!/bin/bash
# 不明確

cd ~/garyohosu/magic-box-ai
git pull
# ...長いコードが続く...
# 何をしてるのか不明
```

---

## 🔄 指示書作成フロー

```
① ユーザーが「〇〇を作ってくれ」とリクエスト
   ↓
② Claude が指示書を計画
   ├─ 何をするのか
   ├─ どのステップに分割するか
   └─ 期待される結果
   ↓
③ Claude が GitHub に指示書を作成
   └─ github:create_or_update_file
   └─ path: "instructions/order_xxx.md" または ".sh"
   ↓
④ Claude がユーザーに報告
   ├─ 「指示書を作成しました」
   ├─ 「git pull で取得してください」
   └─ 「Gemini が自動実行します」
   ↓
⑤ ユーザーが git pull
   ↓
⑥ Agents.md のルール に従って CLI（Gemini など）が自動実行
```

---

## 💡 指示書を作成する際のチェックリスト

```
□ 目的が明確（タイトルに示す）
□ ステップごとに分割
□ 各ステップの目的を説明
□ 予期される結果を示す
□ エラーハンドリング含む
□ set -e で失敗時に停止
□ echo で進捗を表示
□ 最後に ✅ 完了 を表示
□ garyohosu/virtual-company/instructions/ に作成
□ ファイル名が order_xxx または SETUP/TEST を含む
```

---

## 🔗 重要なファイル

### 必ず参照するファイル

```
Agents.md（ルート）
├─ すべてのエージェントが従うルール
│
Claude.md（このファイル）
├─ Claude の役割
│
Gemini.md（ルート）
├─ Gemini の役割
│
instructions/CLAUDE_MEMORY.md
├─ Claude の永続記憶
├─ 重要な制約情報
└─ トラブルシューティング

instructions/00_README_START_HERE.md
├─ instructions/ フォルダの説明
```

---

## 📍 ファイル配置ルール

### ✅ 正しい配置

```
garyohosu/virtual-company/
├── Agents.md                        ✓ ルート
├── Claude.md                        ✓ ルート
├── Gemini.md                        ✓ ルート
└── instructions/
    ├── order_magicboxai_ui.md       ✓
    ├── order_sakura_deploy.sh       ✓
    ├── SETUP_phase3.md              ✓
    ├── TEST_local.sh                ✓
    ├── CLAUDE_MEMORY.md             ✓
    └── ... その他
```

### ❌ 間違った配置

```
garyohosu/magic-box-ai/
└── Claude.md                ✗ ここは使わない

~/Desktop/
└── Claude.md                ✗ ここも使わない

garyohosu/virtual-company/
└── magicboxai/
    └── Claude.md            ✗ ここは指示書フォルダ以外
```

---

## 🛠️ 指示書の実装例

### 例 1: 簡単なセットアップ

```bash
#!/bin/bash
# MagicBoxAI: UI を更新する

set -e

echo "🎯 MagicBoxAI の UI を更新"
echo ""

# Step 1: リポジトリに移動
cd ~/garyohosu/magic-box-ai
echo "✓ リポジトリ: $(pwd)"

# Step 2: 最新を取得
git pull origin main
echo "✓ git pull 完了"

# Step 3: 変更を加える
cp src/index.php src/index.php.bak
# ... 何か変更する ...

# Step 4: テスト
php -l src/index.php
echo "✓ PHP 構文チェック: OK"

# Step 5: コミット & プッシュ
git add src/index.php
git commit -m "feat: Update MagicBoxAI UI"
git push origin main
echo "✓ プッシュ完了"

echo ""
echo "✅ MagicBoxAI UI 更新完了"
```

### 例 2: 複雑な処理

```bash
#!/bin/bash
# MagicBoxAI: GitHub Actions テスト実行

set -e

echo "🧪 GitHub Actions テスト実行"
echo ""

# Step 1: 環境確認
echo "Step 1️⃣: 環境確認"
if ! command -v composer &> /dev/null; then
    echo "❌ Composer がインストールされていません"
    exit 1
fi
echo "✓ Composer: $(composer --version)"

# Step 2: 依存をインストール
echo ""
echo "Step 2️⃣: 依存をインストール"
cd ~/garyohosu/magic-box-ai
composer install
echo "✓ インストール完了"

# Step 3: PHPUnit テスト
echo ""
echo "Step 3️⃣: PHPUnit テスト実行"
./vendor/bin/phpunit tests/Unit -v
echo "✓ PHPUnit テスト: PASS"

# Step 4: pytest テスト
echo ""
echo "Step 4️⃣: pytest テスト実行"
pip install -r requirements.txt
pytest tests/integration -v
echo "✓ pytest テスト: PASS"

# Step 5: 結果をレポート
echo ""
echo "✅ すべてのテストが成功"
```

---

## ✅ 指示書作成時のお約束

### 1️⃣ 明確な目的

```
❌ 「色々更新する」
✅ 「MagicBoxAI の UI を改良して、Example Prompts を表示する」
```

### 2️⃣ ステップ分割

```
❌ 長い処理を1つのステップで実行
✅ 5～10 個のステップに分割
```

### 3️⃣ エラーハンドリング

```
❌ set -e なし、エラー時に続行
✅ set -e で失敗時に停止、必要に応じて if 文で処理
```

### 4️⃣ 進捗表示

```
❌ 何も表示しない
✅ echo で各ステップの進捗を表示
```

### 5️⃣ 結果報告

```
❌ 何も表示しないで終了
✅ 最後に ✅ 完了 と何が変わったか表示
```

---

## 🚀 指示書完成後

### Claude がすること

```
1️⃣ 指示書を GitHub に作成
   └─ github:create_or_update_file で操作

2️⃣ ユーザーに報告
   └─ 「指示書を作成しました」
   └─ 「git pull で実行されます」

3️⃣ 期待される結果を説明
   └─ 「MagicBoxAI のUI が改良されます」
```

### Gemini（CLI）がすること

```
1️⃣ git pull で新ファイルを検出
2️⃣ Agents.md のルール に従って実行
3️⃣ 完了をレポート
```

### ユーザーがすること

```
1️⃣ git pull するだけ
2️⃣ 完了を確認
```

---

**このファイルを常に意識して指示書を作成してください！** 🎯✨
