# 📝 Gemini CLI 実行結果の自動保存システム

**作成日**: 2026-01-31  
**対象**: Gemini CLI（gemini --yolo）  
**目的**: 実行結果をMDファイルとして保存し、問題を検証できるようにする

---

## 🎯 システム概要

Gemini CLIで指示書を実行した際に、以下の情報をMDファイルとして保存：
1. 実行日時
2. 実行した指示書のパス
3. 実行結果（stdout/stderr）
4. 成功/失敗のステータス
5. エラーメッセージ（あれば）

**保存先**: `garyohosu/virtual-company/results/gemini/`

---

## 📂 ディレクトリ構造

```
results/
├── gemini/                          # Gemini CLI の実行結果
│   ├── 2026-01-31_ui_improvements.md
│   ├── 2026-01-31_security_fixes.md
│   ├── 2026-01-31_cron_variable.md
│   └── execution_log.json           # 実行履歴（機械可読）
├── claude/                          # Claude の実行結果
├── codex/                           # Codex の実行結果
└── genspark/                        # Genspark の実行結果
```

---

## 🔧 実装方法

### 方法1: ラッパースクリプト（推奨）

#### スクリプト作成: `scripts/gemini_wrapper.sh`

```bash
#!/bin/bash
# Gemini CLI Wrapper - 実行結果を自動保存
# Usage: ./scripts/gemini_wrapper.sh instructions/order_xxx.md

set -e

# ========================================
# 設定
# ========================================
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTRUCTIONS_FILE="$1"
RESULTS_DIR="$REPO_ROOT/results/gemini"
LOG_FILE="$RESULTS_DIR/execution_log.json"

# 引数チェック
if [ -z "$INSTRUCTIONS_FILE" ]; then
    echo "Usage: $0 <instructions_file.md>"
    exit 1
fi

if [ ! -f "$INSTRUCTIONS_FILE" ]; then
    echo "ERROR: File not found: $INSTRUCTIONS_FILE"
    exit 1
fi

# ディレクトリ作成
mkdir -p "$RESULTS_DIR"

# ========================================
# 実行情報
# ========================================
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
INSTRUCTIONS_BASENAME=$(basename "$INSTRUCTIONS_FILE" .md)
OUTPUT_FILE="$RESULTS_DIR/${TIMESTAMP}_${INSTRUCTIONS_BASENAME}.md"
TEMP_OUTPUT="/tmp/gemini_output_$$.txt"
TEMP_ERROR="/tmp/gemini_error_$$.txt"

echo "========================================="
echo "🤖 Gemini CLI Wrapper"
echo "========================================="
echo "実行時刻: $(date '+%Y-%m-%d %H:%M:%S')"
echo "指示書: $INSTRUCTIONS_FILE"
echo "出力先: $OUTPUT_FILE"
echo "========================================="
echo ""

# ========================================
# Gemini CLI 実行
# ========================================
START_TIME=$(date +%s)
EXIT_CODE=0

echo "📋 指示書を実行中..."
if gemini --yolo "$INSTRUCTIONS_FILE" > "$TEMP_OUTPUT" 2> "$TEMP_ERROR"; then
    EXIT_CODE=0
    STATUS="✅ SUCCESS"
    STATUS_EMOJI="✅"
else
    EXIT_CODE=$?
    STATUS="❌ FAILED"
    STATUS_EMOJI="❌"
fi

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# ========================================
# 結果をMDファイルに保存
# ========================================
cat > "$OUTPUT_FILE" << EOF
# 📝 Gemini CLI 実行結果

## 📊 実行情報

| 項目 | 内容 |
|------|------|
| **ステータス** | $STATUS |
| **実行日時** | $(date '+%Y-%m-%d %H:%M:%S') |
| **指示書** | \`$INSTRUCTIONS_FILE\` |
| **実行時間** | ${DURATION}秒 |
| **終了コード** | $EXIT_CODE |

---

## 📋 指示書の内容

\`\`\`markdown
$(cat "$INSTRUCTIONS_FILE")
\`\`\`

---

## 📤 標準出力（stdout）

\`\`\`
$(cat "$TEMP_OUTPUT")
\`\`\`

---

## 🚨 エラー出力（stderr）

\`\`\`
$(cat "$TEMP_ERROR")
\`\`\`

---

## 🎯 次のアクション

EOF

# ステータスに応じて次のアクションを記載
if [ $EXIT_CODE -eq 0 ]; then
    cat >> "$OUTPUT_FILE" << EOF
### ✅ 成功

実行は正常に完了しました。以下を確認してください：

1. **動作確認**
   - 変更内容が正しく反映されているか確認
   - テストを実行して問題がないか確認

2. **Git操作**
   - 変更をコミット
   - プッシュして他のメンバーと共有

3. **ドキュメント更新**
   - 必要に応じてREADMEやドキュメントを更新

EOF
else
    cat >> "$OUTPUT_FILE" << EOF
### ❌ 失敗

実行中にエラーが発生しました。以下を確認してください：

1. **エラーメッセージを確認**
   - 上記の「エラー出力」セクションを参照
   - エラーの原因を特定

2. **問題を修正**
   - 指示書の内容を修正
   - 必要な依存関係をインストール
   - 権限やパスの問題を解決

3. **再実行**
   - 修正後、再度実行して確認

### 🔍 トラブルシューティング

#### よくあるエラー

1. **ファイルが見つからない**
   - パスが正しいか確認
   - ファイルが存在するか確認

2. **権限エラー**
   - 実行権限を付与: \`chmod +x <file>\`

3. **依存関係エラー**
   - 必要なパッケージをインストール
   - \`npm install\` / \`pip install\` など

4. **構文エラー**
   - スクリプトの構文を確認
   - シェルスクリプトの場合: \`bash -n <file>\`

EOF
fi

# フッター
cat >> "$OUTPUT_FILE" << EOF

---

**生成日時**: $(date '+%Y-%m-%d %H:%M:%S')  
**実行者**: Gemini CLI  
**ラッパースクリプト**: \`scripts/gemini_wrapper.sh\`
EOF

# ========================================
# 実行履歴をJSONに追記
# ========================================
if [ ! -f "$LOG_FILE" ]; then
    echo "[]" > "$LOG_FILE"
fi

# 新しいエントリを作成
NEW_ENTRY=$(cat << EOF
{
  "timestamp": "$(date -Iseconds)",
  "instructions_file": "$INSTRUCTIONS_FILE",
  "output_file": "$OUTPUT_FILE",
  "status": "$STATUS",
  "exit_code": $EXIT_CODE,
  "duration_seconds": $DURATION
}
EOF
)

# JSONに追記（jqを使用）
if command -v jq &> /dev/null; then
    TMP_LOG="/tmp/execution_log_$$.json"
    jq ". += [$NEW_ENTRY]" "$LOG_FILE" > "$TMP_LOG"
    mv "$TMP_LOG" "$LOG_FILE"
else
    echo "WARNING: jq not found. JSON log not updated."
fi

# ========================================
# 結果表示
# ========================================
echo ""
echo "========================================="
echo "$STATUS_EMOJI 実行完了"
echo "========================================="
echo "ステータス: $STATUS"
echo "実行時間: ${DURATION}秒"
echo "結果ファイル: $OUTPUT_FILE"
echo ""
echo "📄 結果を確認:"
echo "  cat $OUTPUT_FILE"
echo ""
echo "📋 履歴を確認:"
echo "  cat $LOG_FILE | jq ."
echo "========================================="

# 一時ファイルを削除
rm -f "$TEMP_OUTPUT" "$TEMP_ERROR"

# 終了コードを返す
exit $EXIT_CODE
```

#### 実行権限を付与

```bash
chmod +x scripts/gemini_wrapper.sh
```

---

### 方法2: Gemini.md の更新

Gemini CLIが自動的に結果を保存するように、`Gemini.md` に記載を追加：

```markdown
## 📝 実行結果の保存

### 実行時
1. 指示書を実行
2. 結果を `results/gemini/<timestamp>_<filename>.md` に保存
3. 実行履歴を `results/gemini/execution_log.json` に追記

### 保存内容
- 実行日時
- 指示書のパス
- 標準出力（stdout）
- エラー出力（stderr）
- 終了コード
- 実行時間
```

---

## 📋 使用方法

### ラッパースクリプト経由で実行

```bash
# 基本的な使い方
cd ~/garyohosu/virtual-company
./scripts/gemini_wrapper.sh instructions/order_magicboxai_ui_improvements_20260131.md

# 複数の指示書を順番に実行
./scripts/gemini_wrapper.sh instructions/order_magicboxai_security_fixes_20260131.md
./scripts/gemini_wrapper.sh instructions/order_magicboxai_cron_variable_days_20260131.md

# 一括実行スクリプト
cat > scripts/run_all_magicboxai_updates.sh << 'EOF'
#!/bin/bash
cd ~/garyohosu/virtual-company

echo "🚀 MagicBoxAI 一括更新開始"
echo ""

# UI改善
echo "1/3: UI改善を実行中..."
./scripts/gemini_wrapper.sh instructions/order_magicboxai_ui_improvements_20260131.md

# セキュリティ修正
echo "2/3: セキュリティ修正を実行中..."
./scripts/gemini_wrapper.sh instructions/order_magicboxai_security_fixes_20260131.md

# CRON可変化
echo "3/3: CRON可変化を実行中..."
./scripts/gemini_wrapper.sh instructions/order_magicboxai_cron_variable_days_20260131.md

echo ""
echo "✅ すべての更新が完了しました"
echo "📊 結果を確認: ls -l results/gemini/"
EOF

chmod +x scripts/run_all_magicboxai_updates.sh
./scripts/run_all_magicboxai_updates.sh
```

---

## 📊 実行結果の確認

### 個別の結果を確認

```bash
# 最新の実行結果を表示
ls -lt results/gemini/ | head -5
cat results/gemini/2026-01-31_12-34-56_order_magicboxai_ui_improvements_20260131.md

# 特定の結果を検索
grep -r "❌ FAILED" results/gemini/
grep -r "✅ SUCCESS" results/gemini/
```

### 実行履歴を確認

```bash
# JSON履歴を確認（jq使用）
cat results/gemini/execution_log.json | jq .

# 失敗した実行のみ表示
cat results/gemini/execution_log.json | jq '.[] | select(.exit_code != 0)'

# 今日の実行を表示
cat results/gemini/execution_log.json | jq '.[] | select(.timestamp | startswith("2026-01-31"))'
```

---

## 🔄 Gitへの自動コミット

### 実行結果を自動でコミット

```bash
# scripts/gemini_wrapper.sh の最後に追加
if [ $EXIT_CODE -eq 0 ]; then
    echo "📝 結果をGitにコミット中..."
    git add "$OUTPUT_FILE" "$LOG_FILE"
    git commit -m "chore: Add Gemini CLI execution result - $(basename $OUTPUT_FILE .md)"
    git push origin main
    echo "✅ Gitにプッシュ完了"
fi
```

---

## 📁 .gitignore の更新

実行結果ファイルをGit管理するか選択：

### パターンA: すべて管理する（推奨）

```bash
# .gitignore に追加しない
# results/ フォルダをすべてコミット
```

### パターンB: 一部のみ管理

```bash
# .gitignore に追加
# 成功した実行結果は除外、失敗のみ管理
results/gemini/*_SUCCESS.md
```

---

## 🎯 Genspark からの確認フロー

### 1. 指示書を作成してコミット

```bash
cd /home/user/webapp
git add instructions/order_xxx.md
git commit -m "feat: Add instruction for xxx"
git push origin genspark_ai_developer
```

### 2. ユーザーがローカルで実行

```bash
# ローカルPC（ユーザー環境）
cd ~/garyohosu/virtual-company
git pull origin main
./scripts/gemini_wrapper.sh instructions/order_xxx.md
```

### 3. 実行結果がGitにプッシュされる

```bash
# 自動的に以下がコミットされる
results/gemini/2026-01-31_xxx.md
results/gemini/execution_log.json
```

### 4. Genspark が結果を確認

```bash
# Genspark環境（このサンドボックス）
cd /home/user/webapp
git pull origin main

# 最新の実行結果を確認
cat results/gemini/$(ls -t results/gemini/*.md | head -1)

# エラーがあれば修正指示書を作成
if grep -q "❌ FAILED" results/gemini/*.md; then
    echo "エラーを検出。修正指示書を作成します..."
    # 修正指示書を作成
fi
```

---

## 🔍 エラー検出と自動修正

### エラー検出スクリプト: `scripts/check_gemini_results.sh`

```bash
#!/bin/bash
# Gemini実行結果のエラーチェック

RESULTS_DIR="results/gemini"
LATEST_RESULT=$(ls -t "$RESULTS_DIR"/*.md 2>/dev/null | head -1)

if [ -z "$LATEST_RESULT" ]; then
    echo "実行結果が見つかりません"
    exit 0
fi

echo "📊 最新の実行結果を確認: $LATEST_RESULT"
echo ""

if grep -q "❌ FAILED" "$LATEST_RESULT"; then
    echo "🚨 エラーを検出しました！"
    echo ""
    echo "エラー内容:"
    echo "========================================="
    sed -n '/## 🚨 エラー出力/,/## 🎯 次のアクション/p' "$LATEST_RESULT" | head -20
    echo "========================================="
    echo ""
    echo "📝 修正が必要です。修正指示書を作成してください。"
    exit 1
else
    echo "✅ 実行は成功しました"
    exit 0
fi
```

---

## 📝 実装手順

### Step 1: スクリプトを作成

```bash
cd ~/garyohosu/virtual-company

# ディレクトリ作成
mkdir -p scripts

# ラッパースクリプトを作成
cat > scripts/gemini_wrapper.sh << 'EOF'
# ↑ 上記のスクリプト内容をコピー
EOF

chmod +x scripts/gemini_wrapper.sh

# エラーチェックスクリプトを作成
cat > scripts/check_gemini_results.sh << 'EOF'
# ↑ 上記のスクリプト内容をコピー
EOF

chmod +x scripts/check_gemini_results.sh
```

### Step 2: テスト実行

```bash
# テスト用の簡単な指示書を作成
cat > instructions/test_hello.md << 'EOF'
# テスト指示書

echo "Hello, Gemini CLI!"
echo "実行日時: $(date)"
EOF

# ラッパー経由で実行
./scripts/gemini_wrapper.sh instructions/test_hello.md

# 結果を確認
cat results/gemini/$(ls -t results/gemini/*.md | head -1)
```

### Step 3: 実際の指示書で実行

```bash
# UI改善を実行
./scripts/gemini_wrapper.sh instructions/order_magicboxai_ui_improvements_20260131.md

# 結果を確認
./scripts/check_gemini_results.sh
```

### Step 4: Gitにコミット

```bash
git add scripts/ results/
git commit -m "feat: Add Gemini CLI result logging system

- Add gemini_wrapper.sh for automatic result logging
- Add check_gemini_results.sh for error detection
- Results saved to results/gemini/ with markdown format
- Execution history tracked in JSON format"

git push origin main
```

---

## 🎨 結果ファイルのフォーマット例

```markdown
# 📝 Gemini CLI 実行結果

## 📊 実行情報

| 項目 | 内容 |
|------|------|
| **ステータス** | ✅ SUCCESS |
| **実行日時** | 2026-01-31 12:34:56 |
| **指示書** | `instructions/order_magicboxai_ui_improvements_20260131.md` |
| **実行時間** | 45秒 |
| **終了コード** | 0 |

---

## 📋 指示書の内容

```markdown
# 🎯 MagicBoxAI UI 改善指示書
...
```

---

## 📤 標準出力（stdout）

```
✅ UI改善を実装中...
✓ 保存確認ダイアログを追加
✓ URLコピーボタンを追加
✓ ZIPダウンロード機能を追加
✓ サンプルコードを追加
✅ 実装完了
```

---

## 🎯 次のアクション

### ✅ 成功

実行は正常に完了しました。以下を確認してください：

1. **動作確認**
   - https://garyo.sakura.ne.jp/magicboxai/ にアクセス
   - 新機能が正しく動作するか確認

2. **Git操作**
   - 変更をコミット
   - プルリクエストを作成

---

**生成日時**: 2026-01-31 12:35:00  
**実行者**: Gemini CLI  
**ラッパースクリプト**: `scripts/gemini_wrapper.sh`
```

---

## 📊 まとめ

### 導入効果

1. **トレーサビリティ**: すべての実行が記録される
2. **デバッグ容易性**: エラー内容が詳細に記録される
3. **自動化**: 結果の確認・修正が自動化できる
4. **履歴管理**: JSON形式で機械可読な履歴が残る

### 今後の拡張

1. **Slack/Discord通知**: エラー時に通知
2. **自動再試行**: エラー時に自動で再実行
3. **統計情報**: 成功率・実行時間の統計
4. **Webダッシュボード**: 実行結果を可視化

---

**このファイルを実行**:
```bash
cd ~/garyohosu/virtual-company
git pull origin main
gemini --yolo instructions/order_gemini_result_logging_20260131.md
```

---

**Status**: 準備完了  
**Priority**: 🟡 中  
**Current Actor**: User（ラッパースクリプト作成）  
**Next Actor**: Gemini（指示書実行）  
**Created At**: 2026-01-31
