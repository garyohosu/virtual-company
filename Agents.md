# 🤖 Agents - 自動実行ルール

**作成日**: 2026-01-31  
**目的**: すべての AI エージェント（Claude, Gemini など）が従うべき統一ルール

---

## ⚠️ 重要: CLIツール が「git pull」を検出して自動実行する仕組み

```
🎯 このシステムの流れ：

ユーザーが CLI ツール（Gemini CLI）のチャットに「git pull」と書く
   ↓
CLI ツール が「git pull」を実行
   ↓
CLI ツール が実行ログを読む
   ↓
「新しいファイルが追加された」と判断
   ↓
このファイル（Agents.md / Claude.md / Gemini.md）のルール に従う
   ↓
instructions/ の新しいファイルを自動実行
```

**キーポイント**: 
- ユーザーはCLIツールのチャットに「git pull」と書くだけ
- CLIツール が ログから 新しいファイルを検出
- 自動実行される（手動操作不要）
```

---

## 🔄 自動実行フロー（詳細）

```
1️⃣ ユーザーが CLI ツール（Gemini CLI）のチャットに「git pull」と書く
   └─ 例: ユーザーが「git pull」とメッセージ送信

2️⃣ CLI ツールが「git pull」コマンドを実行
   └─ cd ~/garyohosu/virtual-company && git pull origin main

3️⃣ CLI ツール が実行ログを読む
   ├─ stdout に以下のように表示される：
   │  ├─ 「Updated c088e02..0f36df1」（新しいコミット）
   │  ├─ 「 Agents.md | 2 +-」（ファイル更新）
   │  ├─ 「 instructions/order_xxx.sh | 50 +++」（新規ファイル）
   │  └─ 「 instructions/order_yyy.md | 30 +++」（新規ファイル）
   └─ ログを解析して「新しいファイルが追加された」と判断

4️⃣ CLI ツール が ルートの設定ファイルを読む
   ├─ ./Agents.md     ← 統一ルール
   ├─ ./Claude.md     ← Claude 設定
   └─ ./Gemini.md     ← 自分の役割

5️⃣ CLI ツール が instructions/ をスキャン
   ├─ git pull のログから検出された新ファイルを リスト化
   ├─ .last_agent_run でタイムスタンプを管理
   └─ 実行順序を決定：SETUP > order > TEST

6️⃣ CLI ツール が 新ファイルを自動実行
   ├─ instructions/order_magicboxai_ui.sh
   ├─ instructions/order_sakura_deploy.sh
   ├─ instructions/TEST_magicboxai.md
   └─ 実行ログをユーザーに表示

7️⃣ 実行結果をレポート
   ├─ stdout に「✅ 完了」と表示
   ├─ .last_agent_run を更新
   └─ Git に自動コミット & プッシュ

8️⃣ 完了（ユーザーに結果を報告）
   └─ すべて自動で完了！
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
00_README_START_HERE.md                ← 説明ファイル
```

---

## 🛠️ CLI ツール実装のポイント

### キーポイント 1: ログ解析

```python
# git pull の実行ログから新ファイルを検出
import subprocess
import re

def detect_new_files_from_log():
    """git pull のログから新ファイルを検出"""
    
    result = subprocess.run(
        ['git', 'pull', 'origin', 'main'],
        capture_output=True,
        text=True
    )
    
    log = result.stdout + result.stderr
    
    # git pull の出力から新ファイルを検出
    # 例: " instructions/order_xxx.sh | 50 +++"
    new_files = re.findall(
        r'^\s+(instructions/\S+)\s+\|',
        log,
        re.MULTILINE
    )
    
    return new_files
```

### キーポイント 2: 自動実行判定

```python
def should_execute(filepath):
    """ファイルを実行すべきか判断"""
    
    # 実行対象
    if filepath.endswith('.sh'):
        return True
    
    if filepath.endswith('.md') and 'order_' in filepath:
        return True
    
    # スキップ対象
    if 'CLAUDE_MEMORY' in filepath:
        return False
    
    if filepath.startswith('_'):
        return False
    
    return False
```

### キーポイント 3: 実行順序の管理

```python
def get_execution_order(files):
    """実行順序を決定"""
    
    setup_files = [f for f in files if 'SETUP' in f and f.endswith('.sh')]
    order_files = [f for f in files if f.startswith('order_') and f.endswith('.sh')]
    test_files = [f for f in files if 'TEST' in f and f.endswith('.sh')]
    md_files = [f for f in files if f.endswith('.md')]
    
    # 優先度順
    return setup_files + order_files + test_files + md_files
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

## 🔐 セキュリティ注意事項

```
⚠️ ログ解析の正確性
  └─ git pull の出力フォーマットに依存
  └─ エッジケース（削除ファイル等）に対応

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

## ✅ チェックリスト（CLI実装時）

```
□ ユーザーからの「git pull」コマンドを受け取る
□ git pull を実行
□ 実行ログを読む
□ ログからファイル変更を検出
□ ルートの Agents.md を読み込み
□ ルートの Claude.md を読み込み（if available）
□ ルートの Gemini.md を読み込み（if available）
□ instructions/ をスキャン
□ 新しいファイルを検出
□ CLAUDE_MEMORY.md など設定ファイルをスキップ
□ ファイルの実行順序を管理
□ .sh ファイルを bash で実行
□ .md ファイルを表示 or 解析
□ 実行結果をレポート
□ .last_agent_run タイムスタンプを更新
□ Git にコミット & プッシュ
□ 無限ループ防止（タイムスタンプ）
```

---

## 💡 実装例（Gemini CLI 用）

```python
#!/usr/bin/env python3
import os
import subprocess
import glob
import re
from datetime import datetime
from pathlib import Path

class VirtualCompanyAgent:
    def __init__(self):
        self.repo_dir = Path.home() / "garyohosu" / "virtual-company"
        self.instructions_dir = self.repo_dir / "instructions"
        self.last_run_file = self.repo_dir / ".last_agent_run"
    
    def run(self, command):
        """コマンドを実行してログを取得"""
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=self.repo_dir
        )
        return result.stdout, result.stderr, result.returncode
    
    def detect_new_files(self):
        """git pull のログから新ファイルを検出"""
        print("📦 git pull を実行中...")
        stdout, stderr, code = self.run("git pull origin main")
        
        log = stdout + stderr
        print(f"ログ:\n{log}\n")
        
        # git pull の出力から instructions/ のファイルを検出
        new_files = re.findall(
            r'^\s+(instructions/\S+)\s+\|',
            log,
            re.MULTILINE
        )
        
        return new_files
    
    def load_config(self):
        """ルートの設定ファイルを読む"""
        print("📖 設定ファイルを読み込み...")
        for f in ["Agents.md", "Claude.md", "Gemini.md"]:
            if (self.repo_dir / f).exists():
                print(f"✓ {f} 読み込み完了")
    
    def should_execute(self, filepath):
        """ファイルを実行すべきか判断"""
        # スキップ対象
        skip_patterns = ['CLAUDE_MEMORY', '_', 'README', 'backup']
        for pattern in skip_patterns:
            if pattern in filepath:
                return False
        
        # 実行対象
        if filepath.endswith('.sh') or (filepath.endswith('.md') and 'order_' in filepath):
            return True
        
        return False
    
    def get_execution_order(self, files):
        """実行順序を決定"""
        setup = sorted([f for f in files if 'SETUP' in f and f.endswith('.sh')])
        order = sorted([f for f in files if 'order_' in f and f.endswith('.sh')])
        test = sorted([f for f in files if 'TEST' in f and f.endswith('.sh')])
        md = sorted([f for f in files if f.endswith('.md')])
        
        return setup + order + test + md
    
    def execute_file(self, filepath):
        """ファイルを実行"""
        print(f"\n▶️  実行中: {filepath}")
        print("=" * 50)
        
        full_path = self.repo_dir / filepath
        
        if full_path.suffix == '.sh':
            stdout, stderr, code = self.run(f"bash {filepath}")
        elif full_path.suffix == '.md':
            stdout = full_path.read_text()
            code = 0
        else:
            return False
        
        print(stdout)
        if stderr:
            print(f"stderr: {stderr}")
        
        print("=" * 50)
        
        if code == 0:
            print(f"✅ 完了: {filepath}")
        else:
            print(f"❌ 失敗: {filepath} (exit: {code})")
        
        return code == 0
    
    def update_timestamp(self):
        """タイムスタンプを更新"""
        now = datetime.now().isoformat()
        self.last_run_file.write_text(now)
        
        print(f"\n📝 タイムスタンプを更新: {now}")
        self.run("git add .last_agent_run")
        self.run("git commit -m 'chore: Update agent timestamp'")
        self.run("git push origin main")
    
    def main(self):
        """メイン処理"""
        os.chdir(self.repo_dir)
        
        print("🤖 Virtual Company エージェント実行\n")
        
        # Step 1: git pull で新ファイルを検出
        new_files = self.detect_new_files()
        
        if not new_files:
            print("✅ 新しいファイルはありません")
            return
        
        # Step 2: 設定を読む
        self.load_config()
        
        # Step 3: 実行対象を決定
        executable_files = [f for f in new_files if self.should_execute(f)]
        
        if not executable_files:
            print("✅ 実行対象のファイルはありません")
            return
        
        # Step 4: 実行順序を決定
        ordered_files = self.get_execution_order(executable_files)
        
        print(f"\n🆕 実行対象: {len(ordered_files)} 個のファイル")
        
        # Step 5: 実行
        for filepath in ordered_files:
            self.execute_file(filepath)
        
        # Step 6: タイムスタンプを更新
        self.update_timestamp()
        
        print("\n🎉 すべて完了！")

if __name__ == "__main__":
    agent = VirtualCompanyAgent()
    agent.main()
```

---

**このシステムで「git pull」と書くだけで完全自動化！** 🚀✨
