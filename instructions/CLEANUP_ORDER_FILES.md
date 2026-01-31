# 📋 Cleanup Order: order*.md ファイルを instructions/ に移動

**実行者**: ユーザー（手動）または Gemini  
**実行方法**: `bash instructions/CLEANUP_ORDER_FILES.sh` または 手動実行  
**対象**: virtual-company リポジトリ  
**内容**: ルートの order*.md ファイルを instructions/ フォルダに整理

---

## 🎯 目的

```
現在：
virtual-company/
├── order_magicboxai_sales.md      ❌ ルート
├── order_magicboxai_development.md ❌ ルート
├── order_github_actions_cicd.md   ❌ ルート
├── order_sakura_php_repository_management.md ❌ ルート
├── instructions/                  ✅
│   ├── MAGICBOXAI_FINAL_SETUP.md
│   └── ... (他の指示書)
└── ... その他

目的：
virtual-company/
├── instructions/                  
│   ├── order_magicboxai_sales.md          ✅ 移動
│   ├── order_magicboxai_development.md    ✅ 移動
│   ├── order_github_actions_cicd.md       ✅ 移動
│   ├── order_sakura_php_repository_management.md ✅ 移動
│   ├── MAGICBOXAI_FINAL_SETUP.md
│   └── ... (他の指示書)
└── ... その他
```

---

## 🚀 実行手順

### Step 1: 現在のファイルを確認

```bash
cd ~/garyohosu/virtual-company

# ルートの order*.md ファイル一覧
ls -la order*.md

# 出力例:
# -rw-r--r-- order_magicboxai_sales.md
# -rw-r--r-- order_magicboxai_development.md
# -rw-r--r-- order_github_actions_cicd.md
# -rw-r--r-- order_sakura_php_repository_management.md
```

### Step 2: ファイルを instructions/ に移動

```bash
# 方法 A: git mv で移動（推奨）

git mv order_magicboxai_sales.md instructions/
git mv order_magicboxai_development.md instructions/
git mv order_github_actions_cicd.md instructions/
git mv order_sakura_php_repository_management.md instructions/

# 確認
git status
```

または

```bash
# 方法 B: 手動移動

mv order_magicboxai_sales.md instructions/
mv order_magicboxai_development.md instructions/
mv order_github_actions_cicd.md instructions/
mv order_sakura_php_repository_management.md instructions/

# Git に追加
git add order*.md instructions/order*.md
git status
```

### Step 3: Commit & Push

```bash
git commit -m "chore: Organize order*.md files into instructions/ directory

移動ファイル：
- order_magicboxai_sales.md
- order_magicboxai_development.md
- order_github_actions_cicd.md
- order_sakura_php_repository_management.md

理由：
ルートをシンプルに保つため
すべての指示書を instructions/ フォルダに集約
"

git push origin main
```

---

## 📊 完了確認

```bash
# 確認
ls -la instructions/order*.md

# 出力例:
# -rw-r--r-- instructions/order_magicboxai_sales.md
# -rw-r--r-- instructions/order_magicboxai_development.md
# -rw-r--r-- instructions/order_github_actions_cicd.md
# -rw-r--r-- instructions/order_sakura_php_repository_management.md

# ルートに order*.md がないか確認
ls order*.md 2>/dev/null || echo "✅ ルートに order*.md はありません"

# Git ログ確認
git log --oneline -2
```

---

## 🔄 その後の使用方法

移動後は以下のように使用：

```bash
# before（古い）
gemini --yolo order_magicboxai_development.md

# after（新しい）
gemini --yolo instructions/order_magicboxai_development.md

# または
cd ~/garyohosu/magic-box-ai
gemini --yolo ~/garyohosu/virtual-company/instructions/order_magicboxai_development.md
```

---

## 📝 自動実行スクリプト（オプション）

手動で実行したくない場合：

```bash
#!/bin/bash
cd ~/garyohosu/virtual-company

# ファイル移動
git mv order_magicboxai_sales.md instructions/ 2>/dev/null || mv order_magicboxai_sales.md instructions/
git mv order_magicboxai_development.md instructions/ 2>/dev/null || mv order_magicboxai_development.md instructions/
git mv order_github_actions_cicd.md instructions/ 2>/dev/null || mv order_github_actions_cicd.md instructions/
git mv order_sakura_php_repository_management.md instructions/ 2>/dev/null || mv order_sakura_php_repository_management.md instructions/

# Commit & Push
git add -A
git commit -m "chore: Organize order*.md files into instructions/ directory" && git push origin main

echo "✅ Cleanup complete!"
ls -la instructions/order*.md
```

このスクリプトを `cleanup_order_files.sh` として保存して実行：

```bash
bash cleanup_order_files.sh
```

---

**では実行してください！** 🚀

手動でいいですか？それとも Gemini に実行させます？
