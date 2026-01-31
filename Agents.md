# 🤖 Agents - 自動実行ルール

**作成日**: 2026-01-31  
**目的**: すべての AI エージェント（Claude, Gemini など）が従うべき統一ルール

---

## ⚠️ 重要: このフォルダ（instructions/）について

```
🎯 このフォルダ = すべての自動実行ファイルが入っているフォルダ

git pull するだけで：
  ✅ このフォルダのファイルが自動実行される
  ✅ 新しく追加されたファイルが検出される
  ✅ Agents.md / Claude.md / Gemini.md のルール に従って実行

詳細は 00_README_START_HERE.md を参照：
https://github.com/garyohosu/virtual-company/blob/main/instructions/00_README_START_HERE.md
```

---

## 🎯 自動実行ルール（必須）

### ✅ git pull 時の自動実行

**トリガー**: ユーザーが `git pull` を実行した時

**実行内容**:

```bash
# Step 1: 新しいファイルを検出
cd ~/garyohosu/virtual-company
git pull origin main

# Step 2: instructions/ フォルダをスキャン
ls -la instructions/*.md instructions/*.sh 2>/dev/null | while read -r line; do
    filename=$(echo "$line" | awk '{print $NF}')
    
    # Step 3: 新しいファイルか確認
    if [ -f "$filename" ]; then
        echo "🆕 新しいファイルを検出: $filename"
        
        # Step 4: 自動実行
        execute_file "$filename"
    fi
done
```

---

## 📋 実行するファイルのパターン

### ✅ 実行対象

```
instructions/*.sh          ← Bash スクリプト（最優先）
instructions/order_*.md    ← 指示書（Markdown）
instructions/*SETUP*.md    ← セットアップ関連
instructions/*TEST*.sh     ← テスト関連
```

### ❌ スキップ対象

```
instructions/CLAUDE_MEMORY.md          ← 設定ファイル
instructions/*_backup.md               ← バックアップ
instructions/_*.md                     ← 下書き
```

---

## 🔄 自動実行フロー

```
1️⃣ ユーザーが git pull を実行
   └─ cd ~/garyohosu/virtual-company && git pull origin main

2️⃣ CLIツール（Gemini など）が自動起動
   └─ ~/.bashrc or ~/.zshrc で設定

3️⃣ CLIツール が このファイル（Agents.md）を読む
   └─ ルートの Agents.md をロード

4️⃣ CLIツール が instructions/ をスキャン
   └─ 最後の実行時刻を記録したファイルと比較
   └─ それ以降に追加/更新されたファイルをリスト化

5️⃣ CLIツール が Agents.md のルール に従って実行
   ├─ SETUP_*.sh（最優先）
   ├─ order_*.sh
   ├─ TEST_*.sh
   └─ order_*.md

6️⃣ 実行結果をレポート
   └─ stdout に結果を表示
   └─ Git に自動コミット

7️⃣ 完了
```

---

## 🛠️ CLI ツール起動時の処理

### CLIツールが起動時に読むべき順序

```bash
#!/bin/bash
# CLI ツール起動スクリプト

# Step 1: リポジトリのルートに移動
cd ~/garyohosu/virtual-company

# Step 2: ルートの設定ファイルを読む（この順序で）
echo "📖 設定ファイルを読み込み中..."
source ./Agents.md    # すべてのエージェント共通ルール
source ./Claude.md    # Claude の設定（if available）
source ./Gemini.md    # Gemini の設定（if available）

# Step 3: git pull で最新を取得
echo "📦 git pull を実行中..."
git pull origin main

# Step 4: instructions/ をスキャン
echo "🔍 新しい指示書をスキャン中..."
bash ./scan_and_execute.sh

# Step 5: 完了
echo "🎉 完了"
```

---

## 📝 実行ファイルの命名規則

### ✅ 推奨形式

```
instructions/order_PROJECTNAME_DESCRIPTION.md
instructions/order_PROJECTNAME_DESCRIPTION.sh

examples:
  ✓ instructions/order_magicboxai_ui_update.sh
  ✓ instructions/order_sakura_deploy.md
  ✓ instructions/SETUP_phase3.md
  ✓ instructions/TEST_local.sh
```

### 実行優先度

```
1️⃣ *SETUP*.sh       ← セットアップ（最優先）
2️⃣ order_*.sh      ← 指示スクリプト
3️⃣ *TEST*.sh       ← テスト
4️⃣ order_*.md      ← その他指示書
```

---

## 🔍 ファイル検出ロジック

### Python での実装例

```python
import os
import glob
from datetime import datetime

def scan_new_instructions():
    """新しい指示書ファイルをスキャン"""
    
    instructions_dir = "instructions"
    last_run_file = ".last_agent_run"
    
    # 最後の実行時刻を読む
    if os.path.exists(last_run_file):
        with open(last_run_file, 'r') as f:
            last_run = datetime.fromisoformat(f.read().strip())
    else:
        last_run = datetime(2000, 1, 1)
    
    # 新しいファイルをリスト化
    new_files = []
    for pattern in ["*.sh", "*.md"]:
        for filepath in glob.glob(f"{instructions_dir}/{pattern}"):
            # スキップ対象
            basename = os.path.basename(filepath)
            if basename in ["CLAUDE_MEMORY.md", "README.md"]:
                continue
            if basename.startswith("_"):
                continue
            
            # 新しいか確認
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            if mtime > last_run:
                new_files.append((filepath, mtime))
    
    # 実行順序でソート
    new_files.sort(key=lambda x: (
        0 if "SETUP" in x[0] else
        1 if x[0].endswith(".sh") else
        2 if "TEST" in x[0] else 3
    ), reverse=False)
    
    return new_files

def execute_instruction(filepath):
    """指示ファイルを実行"""
    
    print(f"▶️  実行中: {filepath}")
    print("=" * 50)
    
    if filepath.endswith(".sh"):
        os.system(f"bash {filepath}")
    elif filepath.endswith(".md"):
        with open(filepath, 'r') as f:
            print(f.read())
    
    print("=" * 50)
    print(f"✅ 完了: {filepath}")

# メイン
if __name__ == "__main__":
    os.chdir(os.path.expanduser("~/garyohosu/virtual-company"))
    
    # git pull
    os.system("git pull origin main")
    
    # スキャン
    new_files = scan_new_instructions()
    
    if new_files:
        print(f"🆕 新しいファイルを検出: {len(new_files)} 個")
        for filepath, _ in new_files:
            execute_instruction(filepath)
        
        # タイムスタンプを更新
        with open(".last_agent_run", 'w') as f:
            f.write(datetime.now().isoformat())
        
        os.system("git add .last_agent_run")
        os.system("git commit -m 'chore: Update last agent run'")
        os.system("git push origin main")
    else:
        print("✅ 新しいファイルはありません")
```

---

## ✅ チェックリスト（CLI実装時）

```
□ ルートの Agents.md を読み込み
□ ルートの Claude.md を読み込み（if available）
□ ルートの Gemini.md を読み込み（if available）
□ git pull で最新を取得
□ instructions/ をスキャン
□ 新しいファイルを検出
□ CLAUDE_MEMORY.md など設定ファイルをスキップ
□ ファイルの実行順序を管理
□ .sh ファイルを bash で実行
□ .md ファイルを表示 or 解析
□ 実行結果をレポート
□ .last_agent_run タイムスタンプを更新
□ Git にコミット & プッシュ
```

---

## 🔐 セキュリティ注意事項

```
⚠️ 実行ファイルの検証
  └─ Git の署名確認を推奨
  └─ 信頼できるリポジトリのみ

⚠️ 無限ループの防止
  └─ 同じファイルの2回実行を避ける
  └─ .last_agent_run で管理

⚠️ エラーハンドリング
  └─ 実行失敗時も記録
  └─ ロールバック機構
```

---

**このファイルを CLI ツール起動時に読んでください！** 🚀
