#!/bin/bash

# WEB版AIが実行するコマンド
# 最新の実行結果を簡潔に表示

set -e

REPO_DIR="${1:-$(pwd)}"
cd "$REPO_DIR"

echo "# 📊 Virtual Company - 実行状況レポート"
echo ""
echo "**生成日時**: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# ========================================
# 最新の実行結果
# ========================================
echo "## ✨ 最新の実行"
echo ""

LATEST=$(ls -t results/gemini/*.md 2>/dev/null | grep -v "ANALYSIS\|RESULT\|EXECUTION" | head -1)
if [ -f "$LATEST" ]; then
  BASENAME=$(basename "$LATEST")
  MODTIME=$(date -r "$LATEST" '+%Y-%m-%d %H:%M:%S' 2>/dev/null || stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" "$LATEST" 2>/dev/null)
  
  echo "- **ファイル**: \`$BASENAME\`"
  echo "- **実行日時**: $MODTIME"
  
  # ステータスを確認
  if grep -q "✅ SUCCESS" "$LATEST" 2>/dev/null; then
    echo "- **ステータス**: ✅ 成功"
  elif grep -q "❌ FAILED" "$LATEST" 2>/dev/null; then
    echo "- **ステータス**: ❌ 失敗"
    echo ""
    echo "### ⚠️ エラー詳細"
    echo ""
    echo "\`\`\`"
    grep -A 10 "エラー出力\|Error\|ERROR" "$LATEST" 2>/dev/null | head -20
    echo "\`\`\`"
  elif grep -q "⏳ IN_PROGRESS" "$LATEST" 2>/dev/null; then
    echo "- **ステータス**: ⏳ 実行中"
  else
    echo "- **ステータス**: ⚪ 不明"
  fi
else
  echo "- **ステータス**: まだ実行されていません"
fi

echo ""

# ========================================
# 未実行の指示書
# ========================================
echo "## 📋 未実行の指示書"
echo ""

PENDING_COUNT=0
for instruction in instructions/order_*.md instructions/fix_*.md; do
  if [ -f "$instruction" ]; then
    BASENAME=$(basename "$instruction" .md)
    # results/gemini/ に対応する結果があるかチェック
    if ! ls results/gemini/*${BASENAME}*.md 1> /dev/null 2>&1; then
      echo "- \`$(basename $instruction)\`"
      PENDING_COUNT=$((PENDING_COUNT + 1))
    fi
  fi
done

if [ $PENDING_COUNT -eq 0 ]; then
  echo "なし（すべて実行済み）"
fi

echo ""

# ========================================
# 最近の実行履歴（直近5件）
# ========================================
echo "## 📜 最近の実行履歴（直近5件）"
echo ""

RECENT_FILES=$(ls -t results/gemini/*.md 2>/dev/null | grep -v "ANALYSIS\|RESULT\|EXECUTION" | head -5)
if [ -n "$RECENT_FILES" ]; then
  echo "| 日時 | 指示書 | ステータス |"
  echo "|------|--------|-----------|"
  
  echo "$RECENT_FILES" | while read file; do
    if [ -f "$file" ]; then
      BASENAME=$(basename "$file")
      MODTIME=$(date -r "$file" '+%m-%d %H:%M' 2>/dev/null || stat -f "%Sm" -t "%m-%d %H:%M" "$file" 2>/dev/null)
      
      # ステータスを判定
      if grep -q "✅ SUCCESS" "$file" 2>/dev/null; then
        STATUS="✅ 成功"
      elif grep -q "❌ FAILED" "$file" 2>/dev/null; then
        STATUS="❌ 失敗"
      elif grep -q "⏳ IN_PROGRESS" "$file" 2>/dev/null; then
        STATUS="⏳ 実行中"
      else
        STATUS="⚪ 不明"
      fi
      
      echo "| $MODTIME | \`${BASENAME:0:40}...\` | $STATUS |"
    fi
  done
else
  echo "実行履歴がありません"
fi

echo ""

# ========================================
# 統計情報
# ========================================
echo "## 📈 統計情報"
echo ""

TOTAL=$(ls results/gemini/*.md 2>/dev/null | grep -v "ANALYSIS\|RESULT\|EXECUTION" | wc -l | tr -d ' ')
SUCCESS=$(grep -l "✅ SUCCESS" results/gemini/*.md 2>/dev/null | wc -l | tr -d ' ')
FAILED=$(grep -l "❌ FAILED" results/gemini/*.md 2>/dev/null | wc -l | tr -d ' ')

echo "- **総実行数**: $TOTAL"
echo "- **成功**: $SUCCESS"
echo "- **失敗**: $FAILED"

if [ "$TOTAL" -gt 0 ]; then
  SUCCESS_RATE=$((SUCCESS * 100 / TOTAL))
  echo "- **成功率**: ${SUCCESS_RATE}%"
fi

echo ""

# ========================================
# 次のアクション
# ========================================
echo "## 🎯 次のアクション"
echo ""

if [ $PENDING_COUNT -gt 0 ]; then
  echo "### 未実行の指示書を実行してください"
  echo ""
  echo "\`\`\`bash"
  echo "# ローカルPCで実行"
  echo "cd ~/garyohosu/virtual-company"
  echo "git pull origin main"
  echo ""
  for instruction in instructions/order_*.md instructions/fix_*.md; do
    if [ -f "$instruction" ]; then
      BASENAME=$(basename "$instruction" .md)
      if ! ls results/gemini/*${BASENAME}*.md 1> /dev/null 2>&1; then
        echo "./scripts/gemini_wrapper.sh $instruction"
      fi
    fi
  done
  echo "\`\`\`"
elif [ "$FAILED" -gt 0 ]; then
  echo "### 失敗した指示書を確認してください"
  echo ""
  echo "最新の失敗したファイルを確認："
  FAILED_FILE=$(grep -l "❌ FAILED" results/gemini/*.md 2>/dev/null | head -1)
  if [ -n "$FAILED_FILE" ]; then
    echo ""
    echo "\`\`\`bash"
    echo "cat $FAILED_FILE"
    echo "\`\`\`"
  fi
else
  echo "✅ すべての指示書が正常に実行されました！"
fi

echo ""
echo "---"
echo ""
echo "**📝 このレポートの生成コマンド**: \`./scripts/web_ai_status.sh\`"
