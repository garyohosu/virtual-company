# 🤖 Gemini - CLI エージェント実行設定

**対象**: Gemini CLI（gemini --yolo）  
**作成日**: 2026-01-31  
**目的**: Gemini が Virtual Company 内で自動実行すべきルール

---

## 🎯 Gemini の責務

### ✅ やるべきこと

```
1️⃣ git pull でリポジトリを更新
   └─ cd ~/garyohosu/virtual-company && git pull origin main

2️⃣ instructions/ フォルダをスキャン
   └─ 新しい .sh / .md ファイルを検出
   └─ 最後の実行時刻と比較

3️⃣ 新しいファイルを自動実行
   └─ .sh ファイルを bash で実行
   └─ .md ファイルを解析 or 表示

4️⃣ 実行結果をレポート
   └─ stdout に出力
   └─ エラーログを記録

5️⃣ Git にコミット & プッシュ
   └─ .last_agent_run を更新
   └─ 自動コミット
```

### ❌ してはいけないこと

```
❌ ファイルの存在確認なしに実行
❌ 同じファイルを2回実行
❌ 実行失敗時に続行（set -e で停止）
❌ 無限ループ（タイムスタンプで防止）
❌ エラーログなしに失敗
```

---

## 🚀 Gemini 起動時の処理フロー

### 標準的な実行フロー

```bash
#!/bin/bash
# Gemini CLI: 起動時処理

# Step 1: 設定ファイルを読む
source ~/.config/agents/Agents.md
source ~/.config/agents/Gemini.md

# Step 2: リポジトリへ移動
REPO_DIR="~/garyohosu/virtual-company"
cd "$REPO_DIR"

# Step 3: git pull で更新
echo "📦 git pull を実行中..."
git pull origin main

# Step 4: Agents.md に従って新ファイルをスキャン
echo "🔍 新しい指示書をスキャン中..."

# Step 5: 新しいファイルを実行
bash instructions/scan_and_execute.sh

# Step 6: 完了
echo ""
echo "🎉 Gemini 実行完了"
```

---

## 📝 Gemini が実行すべきステップ

### Step 1: ファイルをスキャン

```bash
#!/bin/bash
# scan_and_execute.sh

INSTRUCTIONS_DIR="instructions"
LAST_RUN_FILE=".last_agent_run"

# 最後の実行時刻を読む
if [ -f "$LAST_RUN_FILE" ]; then
    LAST_RUN=$(cat "$LAST_RUN_FILE")
    LAST_RUN_EPOCH=$(date -d "$LAST_RUN" +%s)
else
    LAST_RUN_EPOCH=0
fi

echo "⏰ 前回の実行: $LAST_RUN"
```

### Step 2: 新しいファイルを検出

```bash
# 新しい .sh ファイルを検出
echo ""
echo "🔍 新しい .sh ファイルを検出..."

SETUP_FILES=$(find "$INSTRUCTIONS_DIR" -name "*SETUP*.sh" \
    -newermt "$(date -d @$LAST_RUN_EPOCH)" \
    2>/dev/null | sort)

ORDER_FILES=$(find "$INSTRUCTIONS_DIR" -name "order_*.sh" \
    -newermt "$(date -d @$LAST_RUN_EPOCH)" \
    2>/dev/null | sort)

TEST_FILES=$(find "$INSTRUCTIONS_DIR" -name "*TEST*.sh" \
    -newermt "$(date -d @$LAST_RUN_EPOCH)" \
    2>/dev/null | sort)

# 新しい .md ファイルを検出
MD_FILES=$(find "$INSTRUCTIONS_DIR" -name "order_*.md" \
    -o -name "*SETUP*.md" \
    -newermt "$(date -d @$LAST_RUN_EPOCH)" \
    2>/dev/null | sort)
```

### Step 3: 実行順序を管理

```bash
# 実行順序: SETUP > order > TEST > md

declare -a ALL_FILES
ALL_FILES+=($SETUP_FILES)
ALL_FILES+=($ORDER_FILES)
ALL_FILES+=($TEST_FILES)

if [ ${#ALL_FILES[@]} -eq 0 ]; then
    echo "✅ 新しいファイルはありません"
    exit 0
fi

echo "🆕 検出: ${#ALL_FILES[@]} 個のファイル"
```

### Step 4: 各ファイルを実行

```bash
for file in "${ALL_FILES[@]}"; do
    echo ""
    echo "▶️  実行中: $file"
    echo "=================================================="
    
    if [[ "$file" == *.sh ]]; then
        bash "$file"
        EXIT_CODE=$?
    elif [[ "$file" == *.md ]]; then
        cat "$file"
        EXIT_CODE=0
    fi
    
    echo "=================================================="
    
    if [ $EXIT_CODE -eq 0 ]; then
        echo "✅ 完了: $file"
    else
        echo "❌ 失敗: $file (exit code: $EXIT_CODE)"
        # 失敗してもスキップして続行（または stop）
    fi
done
```

### Step 5: タイムスタンプを更新

```bash
# 実行完了時刻を記録
NOW=$(date -Iseconds)
echo "$NOW" > "$LAST_RUN_FILE"

echo ""
echo "📝 タイムスタンプを更新: $NOW"

# Git にコミット
git add "$LAST_RUN_FILE"
git commit -m "chore: Update last agent run timestamp - $(date +%Y-%m-%d)"
git push origin main

echo "✅ Git にプッシュ完了"
```

---

## 🔍 ファイル検出優先度

### 実行順序

```
1️⃣ *SETUP*.sh       ← セットアップ・初期化（最優先）
2️⃣ order_*.sh      ← 標準指示スクリプト
3️⃣ *TEST*.sh       ← テスト関連
4️⃣ order_*.md      ← その他指示書
5️⃣ *README*.md     ← 読むだけ（実行しない）
```

### スキップ対象

```
CLAUDE_MEMORY.md      ← 設定ファイル
Agents.md             ← ルール定義
Claude.md             ← Claude 設定
Gemini.md             ← Gemini 設定（このファイル）
_*.md                 ← 下書きファイル
_*.sh                 ← 下書きスクリプト
```

---

## ⚠️ エラーハンドリング

### 実行失敗時

```bash
# エラーログを記録
if [ $EXIT_CODE -ne 0 ]; then
    echo "❌ エラーが発生: $file"
    echo "Exit Code: $EXIT_CODE"
    
    # エラーログをファイルに保存
    echo "[$(date -Iseconds)] Error in $file (exit: $EXIT_CODE)" \
        >> ".agent_errors.log"
    
    # 選択肢 1: 失敗しても続行
    continue
    
    # または選択肢 2: 失敗したら停止
    # exit $EXIT_CODE
fi
```

---

## 🔐 セキュリティチェック

### 実行前の確認

```bash
# 1. ファイルの所有者確認
if [ "$(stat -c %U "$file")" != "$(whoami)" ]; then
    echo "⚠️  警告: ファイルの所有者が異なります"
    # スキップするか確認
fi

# 2. 実行権限確認
if [ ! -x "$file" ]; then
    chmod +x "$file"
    echo "✓ 実行権限を追加: $file"
fi

# 3. ファイルサイズ確認（異常に大きいファイルをスキップ）
SIZE=$(stat -c %s "$file")
if [ $SIZE -gt 1000000 ]; then
    echo "⚠️  スキップ: ファイルが大きすぎます ($SIZE bytes)"
    continue
fi
```

---

## 📊 実行ログ例

```
🤖 Gemini CLI: 自動実行エージェント
================================================

📦 git pull を実行中...
Already up to date.
✓ リポジトリ: ~/garyohosu/virtual-company

🔍 新しい指示書をスキャン中...
⏰ 前回の実行: 2026-01-31T03:00:00+09:00

🆕 検出: 3 個のファイル
  1. instructions/order_magicboxai_ui.sh
  2. instructions/order_sakura_deploy.sh
  3. instructions/TEST_magicboxai.md

▶️  実行中: instructions/order_magicboxai_ui.sh
==================================================
🎯 MagicBoxAI の UI を更新
Step 1️⃣: ファイルをバックアップ
✓ バックアップ完了
Step 2️⃣: UI を更新
✓ UI 更新完了
Step 3️⃣: テストを実行
✓ テスト OK
Step 4️⃣: Git にプッシュ
✓ プッシュ完了
✅ MagicBoxAI UI 更新完了
==================================================
✅ 完了: instructions/order_magicboxai_ui.sh

▶️  実行中: instructions/order_sakura_deploy.sh
==================================================
... (実行ログ) ...
==================================================
✅ 完了: instructions/order_sakura_deploy.sh

▶️  実行中: instructions/TEST_magicboxai.md
==================================================
(内容を表示)
==================================================
✅ 完了: instructions/TEST_magicboxai.md

📝 タイムスタンプを更新: 2026-01-31T03:25:00+09:00
✅ Git にプッシュ完了

🎉 Gemini 実行完了
================================================
```

---

## 📋 Gemini 実装チェックリスト

```
□ git pull で最新を取得
□ instructions/ をスキャン
□ .last_agent_run を読み込み
□ 新しいファイルを検出
□ CLAUDE_MEMORY.md など設定をスキップ
□ .sh ファイルを bash で実行
□ .md ファイルを読んで表示
□ 実行順序を管理（SETUP > order > TEST）
□ エラーハンドリング実装
□ 実行ログを表示
□ .last_agent_run を更新
□ 実行結果を Git にコミット & プッシュ
□ 無限ループ防止（タイムスタンプ）
□ セキュリティチェック実装
```

---

## 🚀 実装用テンプレート

### Python での実装

```python
#!/usr/bin/env python3
import os
import subprocess
import glob
from datetime import datetime
from pathlib import Path

def setup_environment():
    """環境をセットアップ"""
    repo_dir = Path.home() / "garyohosu" / "virtual-company"
    os.chdir(repo_dir)
    print(f"📍 リポジトリ: {repo_dir}")

def git_pull():
    """git pull を実行"""
    print("📦 git pull を実行中...")
    subprocess.run(["git", "pull", "origin", "main"], check=True)

def scan_new_files():
    """新しいファイルをスキャン"""
    last_run_file = Path(".last_agent_run")
    
    if last_run_file.exists():
        last_run = datetime.fromisoformat(last_run_file.read_text().strip())
    else:
        last_run = datetime(2000, 1, 1)
    
    new_files = []
    for pattern in ["instructions/*SETUP*.sh", "instructions/order_*.sh", 
                    "instructions/*TEST*.sh", "instructions/order_*.md"]:
        for filepath in glob.glob(pattern):
            mtime = datetime.fromtimestamp(Path(filepath).stat().st_mtime)
            if mtime > last_run and not any(x in filepath for x in ["MEMORY", "_", "README"]):
                new_files.append(filepath)
    
    return sorted(new_files)

def execute_file(filepath):
    """ファイルを実行"""
    print(f"▶️  実行中: {filepath}")
    print("=" * 50)
    
    try:
        if filepath.endswith(".sh"):
            subprocess.run(["bash", filepath], check=True)
        elif filepath.endswith(".md"):
            with open(filepath, 'r') as f:
                print(f.read())
        print("=" * 50)
        print(f"✅ 完了: {filepath}")
    except subprocess.CalledProcessError as e:
        print(f"❌ 失敗: {filepath} (exit: {e.returncode})")

def main():
    setup_environment()
    git_pull()
    
    new_files = scan_new_files()
    if new_files:
        print(f"🆕 検出: {len(new_files)} 個のファイル")
        for f in new_files:
            execute_file(f)
        
        # 実行時刻を記録
        Path(".last_agent_run").write_text(datetime.now().isoformat())
        subprocess.run(["git", "add", ".last_agent_run"], check=True)
        subprocess.run(["git", "commit", "-m", "chore: Update agent timestamp"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    else:
        print("✅ 新しいファイルはありません")

if __name__ == "__main__":
    main()
```

---

**このルールに従って Gemini CLI を実装してください！** 🚀✨
