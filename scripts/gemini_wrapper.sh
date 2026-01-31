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
    # jqがない場合はPythonスクリプトを使用
    if [ -f "$REPO_ROOT/scripts/log_result.py" ]; then
        python3 "$REPO_ROOT/scripts/log_result.py" "$REPO_ROOT" "$INSTRUCTIONS_FILE" "$OUTPUT_FILE" "$STATUS" "$EXIT_CODE" "$DURATION"
    else
        echo "WARNING: jq and log_result.py not found. JSON log not updated."
    fi
fi

# ========================================  
# Gitへの自動コミット (成功時のみ)  
# ========================================  
if [ $EXIT_CODE -eq 0 ]; then
    echo "📝 結果をGitにコミット中..."
    git add "$OUTPUT_FILE" "$LOG_FILE"
    git commit -m "chore: Add Gemini CLI execution result - $(basename "$OUTPUT_FILE" .md)"
    # git push origin main  # 安全のためコメントアウト。必要に応じて有効化
    echo "✅ Gitにコミット完了"
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
echo "  cat $LOG_FILE"
echo "========================================="

# 一時ファイルを削除
rm -f "$TEMP_OUTPUT" "$TEMP_ERROR"

# 終了コードを返す
exit $EXIT_CODE