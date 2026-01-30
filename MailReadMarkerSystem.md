# Mail System with Read Markers - 既読機能実装

## 🎯 メールシステムの既読機能

各メールに「ここまで読んだ」という印を入れて、Git に push します。

---

## 📧 メールファイルのフォーマット

### Before (読む前)

```markdown
# Mail from Bob - Request for Schema Review

**From**: Bob
**Date**: 2025-01-29 16:30
**Subject**: テーブル定義レビューのお願い
**Priority**: HIGH
**Status**: Awaiting Alice's Response

---

## Message

Hi Alice,

新しいテーブル定義をレビューしてもらえますか？

[内容...]
```

### After (読んだ後)

```markdown
# Mail from Bob - Request for Schema Review

**From**: Bob
**Date**: 2025-01-29 16:30
**Subject**: テーブル定義レビューのお願い
**Priority**: HIGH
**Status**: ✅ READ by Alice at 2025-01-30 09:15

---

## 📨 Message Status
- ✅ Read at: 2025-01-30 09:15
- 📝 Processed at: 2025-01-30 09:30
- ✅ Git push completed

---

## Message

Hi Alice,

新しいテーブル定義をレビューしてもらえますか？

[内容...]
```

---

## 🔄 CLIの既読処理フロー

```
Step 5: Mail/inbox/ を確認

Alice CLI:
  1. from_bob_001.md を見つける
  2. Status を確認 → "Awaiting Alice's Response"
  3. メール内容を読む
  4. 🎯 ここまで読んだ ← マーク
  5. Status を更新:
     "✅ READ by Alice at 2025-01-30 09:15"
  6. Git commit & push
     "chore: Mark mail as read - from_bob_001.md"
  7. 次のメール確認へ

結果:
  - ✅ from_bob_001.md に timestamp が記録される
  - ✅ Git history に「何時に読んだ」が残る
  - ✅ 次回起動時に「このメールは読んだ」と自動判定
```

---

## 📝 実装例：Alice がメールを読んで既読にする

### Scenario

Alice が朝起動：
```bash
$ your-cli --start alice

📧 メール確認中...
  from_bob_001.md: 未読 ❌
```

Alice がメール内容を読む → CLI がメール内容を処理 → 既読化：

```bash
📧 メール #1 を処理中: from_bob_001.md
   From: Bob
   Subject: テーブル定義レビューのお願い
   
   [メール内容の処理...]
   
✅ メール #1 を既読にしました
   Time: 2025-01-30 09:15
   Git push: Waiting...
   
📧 メール確認完了 (1 件処理)
   git commit & push 中...
```

### Git History

```bash
$ git log --oneline

b6cd23b chore: Mark mail as read - from_bob_001.md (Alice, 2025-01-30 09:15)
a089852 chore: Add Alice - Skills (Failure Patterns)
...
```

---

## 📊 既読フラグ機能の詳細

### ファイルのメタデータ部分

```markdown
**From**: Bob
**Date**: 2025-01-29 16:30
**Subject**: テーブル定義レビューのお願い
**Priority**: HIGH

---

## 📨 Mail Status
- Status: ✅ READ
- Read by: Alice
- Read at: 2025-01-30 09:15 (JST)
- Processing started: 2025-01-30 09:20
- Processing ended: 2025-01-30 09:30
- Action taken: Responded to Bob
- Response file: Employees/bob/Mail/inbox/from_alice_001.md

---

## 📋 Processing Checklist
- [x] Message read
- [x] Patterns checked (Skills.md)
- [x] Response drafted
- [x] Response sent
- [x] Progress updated
```

### メール一覧での既読状態表示

Alice が起動時：
```
📧 Mail Summary:
   ✅ from_bob_001.md (read: 2025-01-30 09:15)
   ❌ from_charlie_001.md (unread)
   ✅ from_manager_001.md (read: 2025-01-29 14:30)

Unread: 1
Total: 3
```

---

## 🔍 未読判定ロジック

```python
def is_mail_read(mail_file: str) -> bool:
    """
    メールが既読か判定
    """
    content = read_file(mail_file)
    
    # Mail Status セクションを見つける
    if "## 📨 Mail Status" not in content:
        return False  # Status section なし = 未読
    
    # Status を確認
    status_section = extract_section(content, "## 📨 Mail Status")
    if "Status: ✅ READ" in status_section:
        return True  # 既読
    elif "Status: Awaiting" in status_section:
        return False  # 未読
    else:
        return False  # 不明 = 未読扱い

def get_mail_read_time(mail_file: str) -> str:
    """
    メールを読んだ時刻を取得
    """
    content = read_file(mail_file)
    status_section = extract_section(content, "## 📨 Mail Status")
    
    # "Read at: 2025-01-30 09:15" を抽出
    match = re.search(r'Read at: (.+)', status_section)
    if match:
        return match.group(1)
    return None
```

---

## 🔄 自動既読処理（CLIロジック）

```python
def process_mail(employee_name: str, mail_file: str):
    """
    メールを読んで自動的に既読化する
    """
    
    # Step 1: メールが既読かチェック
    if is_mail_read(mail_file):
        print(f"✅ This mail is already read at {get_mail_read_time(mail_file)}")
        return
    
    # Step 2: メール内容を読む
    mail_content = read_file(mail_file)
    print(f"📧 Processing mail from {mail_content['from']}...")
    
    # Step 3: 内容を処理（Skills チェック、返信作成など）
    response = process_mail_content(mail_content, employee_name)
    
    # Step 4: メールファイルに既読マークを追加 ← 重要!
    read_marker = f"""
---

## 📨 Mail Status
- Status: ✅ READ
- Read by: {employee_name}
- Read at: {get_current_timestamp()}
- Processing started: {get_current_timestamp()}
- Processing ended: {get_current_timestamp()}
- Response: {response.filename if response else 'No response'}
- Updated: Yes (auto-marked by CLI)
"""
    
    # Step 5: ファイルを更新
    updated_content = mail_content + read_marker
    write_file(mail_file, updated_content)
    
    # Step 6: Git commit & push
    git_commit(
        f"chore: Mark mail as read - {os.path.basename(mail_file)}",
        mail_file
    )
    git_push()
    
    print(f"✅ Mail marked as read at {get_current_timestamp()}")
```

---

## 📬 マルチメール処理（複数メール対応）

Alice に複数メールが来た場合：

### Initial State
```
Employees/alice/Mail/inbox/
├── from_bob_001.md           ❌ 未読
├── from_charlie_001.md        ❌ 未読
└── from_manager_001.md        ✅ 既読 (昨日)
```

### Processing
```bash
$ your-cli --start alice

📧 Mail check...
   ✅ from_manager_001.md (already read: 2025-01-29)
   ❌ from_bob_001.md (new)
   ❌ from_charlie_001.md (new)

Processing mail 1/2: from_bob_001.md
   [メール内容処理...]
   ✅ Marked read at 2025-01-30 09:15
   ✅ Committed & pushed
   
Processing mail 2/2: from_charlie_001.md
   [メール内容処理...]
   ✅ Marked read at 2025-01-30 09:25
   ✅ Committed & pushed

📧 Mail processing complete!
   - Total processed: 2
   - Still unread: 0
```

### Final State
```
Employees/alice/Mail/inbox/
├── from_bob_001.md           ✅ 既読 (2025-01-30 09:15)
├── from_charlie_001.md       ✅ 既読 (2025-01-30 09:25)
└── from_manager_001.md       ✅ 既読 (2025-01-29 14:30)
```

### Git History
```bash
$ git log --oneline | head -5

def8a23 chore: Mark mail as read - from_charlie_001.md
1a2b3c4 chore: Mark mail as read - from_bob_001.md
b6cd23b chore: Mark mail as read - from_bob_001.md (Alice, 09:15)
a089852 chore: Add Alice - Skills
...
```

---

## 🔧 Self-healing（自己修復）機能

失敗時の自動修復：

```python
def check_mail_integrity():
    """
    メールの完全性をチェック
    """
    issues = []
    
    # 問題1: メール内容があるのに既読マークがない
    for mail_file in list_unread_mails():
        content = read_file(mail_file)
        if len(content) > 500 and "Mail Status" not in content:
            issues.append(f"Large mail without read marker: {mail_file}")
            
    # 問題2: 既読マークが古い（>30日）
    for mail_file in list_all_mails():
        read_time = get_mail_read_time(mail_file)
        if read_time and is_older_than(read_time, 30_days):
            issues.append(f"Old unresponded mail: {mail_file}")
    
    # 問題3: メール処理ログが不完全
    for mail_file in list_mails():
        if not has_processing_record(mail_file):
            issues.append(f"No processing record: {mail_file}")
    
    if issues:
        print("⚠️ Mail system issues detected:")
        for issue in issues:
            print(f"   - {issue}")
        
        # 自動修復を試みる
        for issue in issues:
            if "without read marker" in issue:
                auto_add_read_marker(issue)
            elif "No processing record" in issue:
                auto_create_processing_record(issue)
    
    return len(issues) == 0
```

---

## 📈 メール処理の可視化

```
Timeline of Mail Processing:

2025-01-29 16:30 - Bob sends schema review request
                   └─ Message arrives in Alice's inbox

2025-01-30 09:00 - Alice CLI starts up
                   └─ Detects unread mail: from_bob_001.md

2025-01-30 09:15 - Alice CLI reads message
                   └─ ✅ Marked as read
                   └─ 📝 Processing started

2025-01-30 09:30 - Alice finishes review
                   └─ ✅ Processing ended
                   └─ 💌 Response sent to Bob
                   └─ 🔀 Git commit: mark mail as read

2025-01-30 10:00 - Bob CLI checks inbox
                   └─ Finds from_alice_001.md
                   └─ Reads Alice's response
                   └─ ✅ Marks as read
                   └─ 🔀 Git commit: mark mail as read

Result: Complete message trail in Git history
```

---

## 🎯 エラーから学ぶシステム

メール処理失敗例：

### Scenario: Alice がメール返信を忘れた

```
2025-01-30 09:15: Mail marked as read
2025-01-31 00:00: Overnight - No response yet
2025-02-01 09:00: Alice starts CLI
                   └─ Alert: "Mail from Bob (3 days) - No response yet"
                   └─ System checks: from_alice_001.md exists?
                   └─ No! Response missing!
```

### Self-correction

```python
def check_mail_response_status():
    """
    メール返信の状態をチェック
    """
    for mail_file in list_read_mails():
        sender = extract_sender(mail_file)
        response_file = find_response(sender)
        
        if not response_file:
            # 返信がない!
            print(f"⚠️ No response to {mail_file}")
            
            # 学習: Skills.md に追加
            add_pattern_to_skills(
                "Forgotten Mail Response",
                f"Mail from {sender} read but not responded",
                "Always respond immediately after reading"
            )
            
            # 修復: アラーム
            create_alarm(f"Respond to {sender}")
            
            # 記録: Memory を更新
            update_memory(f"Forgot to respond to {sender}")
```

---

## 💾 メール処理記録（完全な監査証跡）

Git に全て記録されるため：

```bash
$ git log --all --grep="mail" --oneline

2025-02-01 08:30 - chore: Mark mail as read - from_manager_002.md
2025-01-31 18:00 - chore: Send response mail - to_bob_001.md
2025-01-30 09:25 - chore: Mark mail as read - from_charlie_001.md
2025-01-30 09:15 - chore: Mark mail as read - from_bob_001.md
2025-01-29 16:30 - chore: New mail received - from_bob_001.md

Complete audit trail! ✅
```

---

## 🔐 メール完全性チェック

```python
def verify_mail_system():
    """
    メールシステムの完全性を確認
    """
    
    # チェック1: 全メールに既読マークがあるか
    for mail_file in list_all_mails():
        if not has_read_marker(mail_file):
            return False, f"Missing read marker: {mail_file}"
    
    # チェック2: 既読時刻が正しいか
    for mail_file in list_all_mails():
        read_time = get_mail_read_time(mail_file)
        if read_time and read_time > get_current_time():
            return False, f"Future read time: {mail_file}"
    
    # チェック3: Git history に記録されているか
    for mail_file in list_all_mails():
        if not in_git_history(mail_file):
            return False, f"Not in Git history: {mail_file}"
    
    # チェック4: 返信が期待通りにあるか
    for mail_file in list_read_mails():
        if is_action_required(mail_file):
            if not has_response(mail_file):
                return False, f"Missing response for: {mail_file}"
    
    return True, "Mail system is healthy ✅"
```

---

## 🎓 失敗から自己改革するシステム

### Pattern: Alice が返信を忘れた

```
Day 1: Bob のメール受け取り
       → Alice が既読化 ✅
       → 返信なし ❌

Day 2: Overnight check
       → Alert: "Unresponded mail for 24h"
       → Skills.md に新パターン追加
       
Pattern #4: Forgotten Mail Response
├─ When: After reading urgent mail
├─ Why: Forgot to respond immediately
├─ Prevention: 
│   - [x] Add reminder system
│   - [x] Auto-create response template
│   - [x] Alert if >6h no response
└─ Status: Implemented

Day 3: Alice starts CLI
       → System shows: "Remember to respond to Bob!"
       → Alice sees Pattern #4 in Skills.md
       → Response sent ✅
```

---

## 📊 メール処理パイプライン

```
Email arrives
    ↓
[未読チェック]
    ├─ 既読? → Skip
    └─ 未読? → Continue
    ↓
[内容読む]
    ├─ Pattern確認（Skills.md）
    ├─ 返信が必要? → Response準備
    └─ 学習? → New pattern記録
    ↓
[既読マーク]
    ├─ Timestamp追加
    ├─ Status更新
    └─ Git commit & push
    ↓
[返信処理]
    ├─ 相手のinboxに書き込み
    ├─ Outbox に記録
    └─ 関連ファイル更新
    ↓
[完了]
    ✅ Memory.md更新
    ✅ result.md 記録
    ✅ 全てGit push
```

---

## ✨ 完璧なメールシステム

**特徴**:
- ✅ 自動既読化（Timestamp付き）
- ✅ Git で全履歴管理
- ✅ 返信忘れの自動検出
- ✅ 失敗から自動学習
- ✅ Self-healing機能
- ✅ 完全な監査証跡

**結果**:
- メール処理が漏れない
- 何時に読んだかが分かる
- 失敗から自動改善
- 1年後、システムは自動修復されている

---

**Status**: 🟢 **Mail System with Read Markers Complete**

これが「失敗を学習して自己改革できるシステム」の完成です！ 🎉
