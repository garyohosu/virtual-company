# 🔧 Gemini CLI ファイル名検出の修正

**作成日**: 2026-01-31  
**対象リポジトリ**: garyohosu/virtual-company  
**対象AI**: Gemini CLI（ローカルPC）  
**優先度**: 🔴 最優先  

---

## 🐛 発見された問題

### 現象
Gemini CLIが以下のように誤ったファイル名で実行しようとしている：
```
C:\project\virtual-company\instructions\order_magicboxai_cron_variable_days.md
```

### 正しいファイル名
```
C:\project\virtual-company\instructions\order_magicboxai_cron_variable_days_20260131.md
```

**日付サフィックス `_20260131` が抜けている！**

---

## 🔍 原因

`.last_agent_run` ファイルまたは自動検出スクリプトが、以下のいずれかの問題を抱えている：

1. **パターンマッチの問題**
   - `order_*.md` のワイルドカードが正しく機能していない
   - 日付サフィックスを含むファイル名を検出できていない

2. **タイムスタンプ比較の問題**
   - ファイルの更新時刻を正しく取得できていない
   - Windows環境特有のパスの問題

3. **ログ解析の問題**
   - `git pull` のログから新しいファイルを検出する際に、ファイル名を誤って抽出している

---

## 🎯 修正方法

### 修正案1: パス区切り文字を統一

Windows環境では `\` と `/` が混在する可能性があります。

**修正前**:
```python
# ファイル検出時にパス区切りが統一されていない
filepath = "C:\project\virtual-company\instructions\order_magicboxai_cron_variable_days.md"
```

**修正後**:
```python
# パス区切り文字を統一
import os
filepath = os.path.normpath("C:/project/virtual-company/instructions/order_magicboxai_cron_variable_days_20260131.md")
```

---

### 修正案2: ファイル名の完全一致検出

**修正前**:
```python
# 曖昧なパターンマッチ
pattern = "order_magicboxai_cron_variable_days*.md"
```

**修正後**:
```python
# 正確なファイル名検出
import glob
from pathlib import Path

instructions_dir = Path("C:/project/virtual-company/instructions")
new_files = []

# すべての order_*.md を取得
for filepath in instructions_dir.glob("order_*.md"):
    # 日付サフィックス付きのファイルも含める
    if "_20260131" in filepath.name or filepath.stat().st_mtime > last_run_time:
        new_files.append(filepath)

print(f"検出されたファイル: {new_files}")
```

---

### 修正案3: git pull ログからの正確なファイル名抽出

**問題の原因**:
`git pull` のログを解析する際に、ファイル名を誤って抽出している可能性があります。

**修正前**:
```python
# git pull のログからファイル名を抽出（不正確）
output = subprocess.check_output(["git", "pull", "origin", "main"])
# 例: "instructions/order_magicboxai_cron_variable_days_20260131.md" 
#     → "order_magicboxai_cron_variable_days" として抽出（誤り）
```

**修正後**:
```python
import subprocess
import re
from pathlib import Path

# git pull を実行してログを取得
result = subprocess.run(
    ["git", "pull", "origin", "main"],
    capture_output=True,
    text=True,
    cwd="C:/project/virtual-company"
)

# ログからファイル名を正確に抽出
for line in result.stdout.split('\n'):
    # 例: " instructions/order_magicboxai_cron_variable_days_20260131.md | 50 +++"
    match = re.search(r'instructions/(order_[a-zA-Z0-9_]+\.md)', line)
    if match:
        filename = match.group(1)
        filepath = Path("C:/project/virtual-company/instructions") / filename
        if filepath.exists():
            print(f"✓ 検出: {filepath}")
            # このファイルを実行リストに追加
```

---

### 修正案4: .last_agent_run の正確なタイムスタンプ管理

**修正前**:
```python
# タイムスタンプの比較が不正確
last_run = datetime.fromisoformat(last_run_file.read_text().strip())
```

**修正後**:
```python
import os
from datetime import datetime
from pathlib import Path

last_run_file = Path("C:/project/virtual-company/.last_agent_run")

# タイムスタンプを正確に読み込む
if last_run_file.exists():
    try:
        last_run_str = last_run_file.read_text(encoding='utf-8').strip()
        last_run = datetime.fromisoformat(last_run_str)
        print(f"⏰ 前回の実行: {last_run}")
    except Exception as e:
        print(f"⚠️ タイムスタンプ読み込みエラー: {e}")
        last_run = datetime(2000, 1, 1)
else:
    last_run = datetime(2000, 1, 1)

# ファイルの更新時刻を正確に比較
instructions_dir = Path("C:/project/virtual-company/instructions")
for filepath in instructions_dir.glob("order_*.md"):
    file_mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
    
    if file_mtime > last_run:
        print(f"🆕 新しいファイル: {filepath.name}")
        print(f"   更新時刻: {file_mtime}")
        # このファイルを実行リストに追加
```

---

## 🧪 テスト方法

### 1. ファイルの存在確認
```bash
# ローカルPCで実行
cd C:\project\virtual-company
ls -la instructions/order_magicboxai_cron_variable_days_20260131.md

# 出力例:
# -rw-r--r-- 1 user user 12345 Jan 31 18:14 instructions/order_magicboxai_cron_variable_days_20260131.md
```

### 2. ファイル名のパターンマッチテスト
```python
# Python で確認
from pathlib import Path

instructions_dir = Path("C:/project/virtual-company/instructions")
files = list(instructions_dir.glob("order_magicboxai_cron_variable_days*.md"))

print("検出されたファイル:")
for f in files:
    print(f"  - {f.name}")

# 期待される出力:
# 検出されたファイル:
#   - order_magicboxai_cron_variable_days_20260131.md
```

### 3. タイムスタンプ比較テスト
```python
from pathlib import Path
from datetime import datetime

filepath = Path("C:/project/virtual-company/instructions/order_magicboxai_cron_variable_days_20260131.md")
file_mtime = datetime.fromtimestamp(filepath.stat().st_mtime)

print(f"ファイル更新時刻: {file_mtime}")

last_run_file = Path("C:/project/virtual-company/.last_agent_run")
if last_run_file.exists():
    last_run_str = last_run_file.read_text(encoding='utf-8').strip()
    last_run = datetime.fromisoformat(last_run_str)
    print(f"前回の実行時刻: {last_run}")
    
    if file_mtime > last_run:
        print("✅ このファイルは新しい（実行対象）")
    else:
        print("⚪ このファイルは古い（スキップ）")
```

---

## 🔧 推奨実装（完全版）

```python
#!/usr/bin/env python3
"""
Gemini CLI: ファイル名検出の修正版
"""
import os
import subprocess
import re
from pathlib import Path
from datetime import datetime

def normalize_path(path_str):
    """パス区切り文字を統一"""
    return os.path.normpath(path_str).replace('\\', '/')

def get_last_run_timestamp(repo_dir):
    """前回の実行時刻を取得"""
    last_run_file = Path(repo_dir) / ".last_agent_run"
    
    if last_run_file.exists():
        try:
            last_run_str = last_run_file.read_text(encoding='utf-8').strip()
            return datetime.fromisoformat(last_run_str)
        except Exception as e:
            print(f"⚠️ タイムスタンプ読み込みエラー: {e}")
    
    # デフォルトは過去の日付（すべてのファイルが新しい扱い）
    return datetime(2000, 1, 1)

def scan_new_instructions(repo_dir, last_run):
    """新しい指示書を検出（日付サフィックス対応）"""
    instructions_dir = Path(repo_dir) / "instructions"
    new_files = []
    
    # order_*.md パターンで検索
    for filepath in instructions_dir.glob("order_*.md"):
        # スキップ対象を除外
        if any(skip in filepath.name for skip in ["_draft", "README", "TEMPLATE"]):
            continue
        
        # ファイルの更新時刻を取得
        file_mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
        
        if file_mtime > last_run:
            new_files.append({
                'path': filepath,
                'name': filepath.name,
                'mtime': file_mtime
            })
            print(f"🆕 新しいファイル: {filepath.name}")
            print(f"   更新時刻: {file_mtime}")
    
    # 日付順にソート（古い順）
    new_files.sort(key=lambda x: x['mtime'])
    
    return new_files

def execute_instruction(filepath):
    """指示書を実行"""
    print(f"\n{'='*50}")
    print(f"▶️  実行中: {filepath.name}")
    print(f"{'='*50}\n")
    
    try:
        # gemini --yolo で実行
        result = subprocess.run(
            ["gemini", "--yolo", str(filepath)],
            cwd=filepath.parent.parent,
            capture_output=True,
            text=True,
            timeout=600  # 10分タイムアウト
        )
        
        print(result.stdout)
        if result.stderr:
            print(f"⚠️ 警告: {result.stderr}")
        
        if result.returncode == 0:
            print(f"\n✅ 完了: {filepath.name}")
            return True
        else:
            print(f"\n❌ 失敗: {filepath.name} (exit code: {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"\n❌ タイムアウト: {filepath.name}")
        return False
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        return False

def update_last_run_timestamp(repo_dir):
    """実行時刻を記録"""
    last_run_file = Path(repo_dir) / ".last_agent_run"
    now = datetime.now().isoformat()
    
    last_run_file.write_text(now, encoding='utf-8')
    print(f"\n📝 タイムスタンプを更新: {now}")

def main():
    # リポジトリのパス（Windows環境）
    repo_dir = normalize_path("C:/project/virtual-company")
    
    print(f"📍 リポジトリ: {repo_dir}")
    
    # git pull を実行
    print("\n📦 git pull を実行中...")
    subprocess.run(["git", "pull", "origin", "main"], cwd=repo_dir, check=True)
    
    # 前回の実行時刻を取得
    last_run = get_last_run_timestamp(repo_dir)
    print(f"\n⏰ 前回の実行: {last_run}")
    
    # 新しい指示書を検出
    print("\n🔍 新しい指示書をスキャン中...")
    new_files = scan_new_instructions(repo_dir, last_run)
    
    if not new_files:
        print("\n✅ 新しいファイルはありません")
        return
    
    print(f"\n🆕 検出: {len(new_files)} 個のファイル")
    
    # 各ファイルを実行
    success_count = 0
    for file_info in new_files:
        if execute_instruction(file_info['path']):
            success_count += 1
    
    # タイムスタンプを更新
    update_last_run_timestamp(repo_dir)
    
    # 結果をサマリー
    print(f"\n{'='*50}")
    print(f"🎉 実行完了")
    print(f"   成功: {success_count}/{len(new_files)}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
```

---

## ✅ 完了確認

実行後、以下を確認してください：

- [ ] `order_magicboxai_cron_variable_days_20260131.md` が正しく検出される
- [ ] ファイル名に日付サフィックスが含まれている
- [ ] `gemini --yolo` で正しいファイルが実行される
- [ ] `.last_agent_run` が正しく更新される
- [ ] 次回以降、同じファイルが二重実行されない

---

## 📝 次のアクション

この修正を適用した後：

1. ローカルPCで Gemini CLI を再実行
2. 正しいファイル名で実行されるか確認
3. results/gemini/ に結果が保存されるか確認
4. 結果を GitHub にプッシュ

---

**Status**: 準備完了  
**Current Actor**: User（ローカルPC）  
**Next Actor**: Gemini CLI  
**Created At**: 2026-01-31 11:50:00
