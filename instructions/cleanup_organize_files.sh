#!/bin/bash
# Gemini 実行用: order*.md ファイルを instructions/ に整理

set -e

echo "🚀 Starting cleanup and organization of order*.md files..."
echo ""

# Step 1: ディレクトリ確認
cd ~/garyohosu/virtual-company

echo "📍 Current directory: $(pwd)"
echo ""

# Step 2: ルートの order*.md ファイルを確認
echo "📋 Files to organize:"
ls -1 order*.md 2>/dev/null | while read file; do
    echo "  - $file"
done
echo ""

# Step 3: instructions/ ディレクトリ確認・作成
if [ ! -d "instructions" ]; then
    echo "📁 Creating instructions/ directory..."
    mkdir -p instructions
else
    echo "📁 instructions/ directory already exists"
fi
echo ""

# Step 4: ファイルを git で移動（推奨）
echo "🔄 Moving files with git mv..."
for file in order_magicboxai_sales.md order_magicboxai_development.md order_github_actions_cicd.md order_sakura_php_repository_management.md; do
    if [ -f "$file" ]; then
        echo "  ✓ Moving: $file → instructions/$file"
        git mv "$file" "instructions/$file" 2>/dev/null || {
            # git mv が失敗した場合は通常の mv で対応
            mv "$file" "instructions/$file"
        }
    else
        echo "  ⊘ File not found: $file (skipped)"
    fi
done
echo ""

# Step 5: Git ステータス確認
echo "📊 Git status:"
git status --short | grep "^R\|^M\|^??" || echo "  (No changes to stage yet)"
echo ""

# Step 6: Git に追加・Commit
echo "💾 Staging files..."
git add -A
echo "  ✓ Files staged"
echo ""

echo "📝 Committing changes..."
git commit -m "chore: Organize order*.md files into instructions/ directory

Moved files:
- order_magicboxai_sales.md
- order_magicboxai_development.md
- order_github_actions_cicd.md
- order_sakura_php_repository_management.md

Reason:
Keep root directory clean
Centralize all instruction files in instructions/ folder
" 2>/dev/null || echo "  (Nothing to commit)"
echo ""

# Step 7: Push to GitHub
echo "🚀 Pushing to GitHub..."
git push origin main
echo "  ✓ Pushed successfully"
echo ""

# Step 8: 完了確認
echo "✅ Verification:"
echo ""
echo "📁 Files in instructions/:"
ls -1 instructions/order*.md 2>/dev/null || echo "  (No order*.md files found)"
echo ""

echo "⊘ Checking root for remaining order*.md files:"
if ls order*.md 2>/dev/null; then
    echo "  ⚠️ Warning: order*.md files still in root"
else
    echo "  ✓ No order*.md files in root - cleanup successful!"
fi
echo ""

# Step 9: ファイル一覧
echo "📊 Final instructions/ directory structure:"
ls -la instructions/ | grep "order_" || echo "  (No files)"
echo ""

# Step 10: Git ログ確認
echo "📝 Latest Git commits:"
git log --oneline -3
echo ""

echo "🎉 Cleanup complete!"
echo ""
echo "✅ Summary:"
echo "  - order*.md files moved to instructions/"
echo "  - Changes committed and pushed"
echo "  - Root directory cleaned up"
echo ""
echo "Next step:"
echo "  cd ~/garyohosu/magic-box-ai"
echo "  gemini --yolo ~/garyohosu/virtual-company/instructions/MAGICBOXAI_FINAL_SETUP.md"
