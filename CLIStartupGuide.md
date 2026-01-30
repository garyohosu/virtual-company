# CLI Startup Guide - Employee Context Loading

## 🎯 CLIの起動フロー（完全版）

あなたのCLIツールが起動する時、以下の順序でファイルを読み込みます。

---

## 📖 10ステップの完全フロー

### Step 1: WhoAmI.md を読む（「自分は誰か？」）

```bash
$ your-cli --start alice

💙 WhoAmI.md を読み込み中...
```

**ファイル**: `Employees/alice/WhoAmI.md`

**出力例**:
```
👋 ログイン: Alice
🏢 役職: Database Administrator
👔 報告先: manager_a1
📞 連絡先: alice@virtualcompany.local
```

**目的**: アイデンティティの確認。自分がしっかり認識されているか。

---

### Step 2: これまでやっていたこと.md を読む（「思い出す」）

```bash
📚 永続的記憶を読み込み中...
```

**ファイル**: `Employees/alice/これまでやっていたこと.md`

**出力例**:
```
📋 今月のタスク進捗
   - ✅ Daily backup automation (完了)
   - ✅ Index optimization (完了)
   - 🟡 Table design review (40% 進行中)
   - 🟡 Connection pool update (30% 進行中)

📊 完了度: 65% (4/6.2 タスク)

⏳ 進行中のタスク:
   1. New Table Design Review (期限: 2025-02-15)
      - Bob からの review request 待ち中
   2. Connection Pool Fix (期限: 2025-02-10)
      - Manager approval 待ち中

💾 先月の学習:
   - SQL Injection 対策を習得
   - Connection pool 計画の重要性を学習
   - Backup monitoring の gap を発見
```

**目的**: 昨日までの進捗を思い出す。「あ、あのプロジェクトはこの状態だった」と記憶を復活させる。

---

### Step 3: Skills.md を読む（「失敗パターンを避ける」）

```bash
🎯 習得したスキル（失敗パターン）を読み込み中...
```

**ファイル**: `Employees/alice/Skills.md`

**出力例**:
```
🔴 Pattern #1: SQL Injection (CRITICAL)
   → 今から SQL を書く時は parameterized queries を使う!
   
🟡 Pattern #2: Connection Pool Sizing (HIGH)
   → デフォルト設定を使わない。計算して設定する!
   
🆕 Pattern #3: Backup Monitoring (新規)
   → 自動化タスクは「失敗通知」が必須
```

**目的**: 「あ、このエラーパターン知ってる」と思い出す。同じ失敗をしない。

---

### Step 4: order_alice_yoro.md を読む（「指示を確認」）

```bash
📋 今週の指示書を読み込み中...
```

**ファイル**: `Employees/alice/order_alice_yoro.md`

**出力例**:
```
📌 主要タスク: Table Design Review
   優先度: HIGH
   期限: 2025-02-15
   状態: 🟡 進行中 (40%)
   
   何をする：
   ✓ schema.sql を確認
   ✓ インデックス戦略をレビュー
   ✓ パフォーマンスを予測
   ✓ セキュリティをチェック（Pattern #1）
   ✓ Connection pool の設計を確認（Pattern #2）

📌 副次タスク: Connection Pool Fix
   優先度: MEDIUM
   期限: 2025-02-10
   
⚠️ ブロッカー:
   - ⏳ Bob が schema.sql を提出待ち
   - ⏳ Manager に インデックス優先度を相談したい
```

**目的**: 「今日は何をするのか」を確認。優先順位を理解。

---

### Step 5: Mail/inbox/ を確認（「メールをチェック」）

```bash
📧 メールをチェック中...
```

**ファイル**: `Employees/alice/Mail/inbox/from_bob_001.md`

**出力例**:
```
📨 メール 1 件 受け取り中

From: Bob
Date: 2025-01-29 16:30
Subject: 重要: 新しいテーブル定義のレビューをお願いします
Priority: HIGH

メッセージ：
  「schema.sql をレビューしてくれませんか？
   テーブル設計、インデックス戦略、
   接続プール設計についてコメントをください。」

添付:
  - schema.sql
  - indexes.sql
  - performance_estimate.txt
```

**目的**: 同僚からのメッセージを読む。依頼やお知らせを把握。

---

### Step 6: 仕事実行（「仕事をする」）

```bash
🚀 仕事を開始します...

[仕事中]
- schema.sql をレビュー
- インデックス戦略を検討
- コメントを作成

[エラーや発見がある場合]
✅ 発見: Missing index on orders.user_id
🔴 問題: Connection pool がまだ小さい
```

**目的**: 実際の仕事をする。Skills を使って失敗を避ける。

---

### Step 7: result.md に出力（「結果を記録」）

```bash
📝 result.md に出力中...
```

**ファイル**: `Employees/alice/result.md`

**内容例**:
```markdown
# Result - Task Completion Report

## Summary
✅ Status: Completed with findings

## Tasks Completed Today

### Task 1: Table Schema Review (Started)
- Status: 🟡 In Progress (40%)
- Findings:
  - ✅ SQL Injection: Good
  - ⚠️ Indexes: Missing on orders.user_id
  - 🔴 Pool: Needs recalculation (10 → 20)

## Issues Found

### Issue #1: Missing Index 🟡
- Fix: CREATE INDEX idx_orders_user_id...

### Issue #2: Connection Pool Undersized 🔴
- Need: Pool size 20 for 2025 peak load

## Skills Updated
- New Pattern #3: Backup Failed Silent
  → Added to Skills.md

## Communication
- ✅ Email to Bob (from_alice_001.md)
- ⏳ Email to Charlie (to_charlie_001.md)

## Time Log
- Total: 6 hours
```

**目的**: 仕事の成果を記録。何ができたか。何を見つけたか。

---

### Step 8: メール送信（「相手に連絡」）

```bash
💌 メール送信中...
```

**アクション**: Bob に返信を作成

**新しいファイル作成**: `Employees/bob/Mail/inbox/from_alice_001.md`

**内容例**:
```markdown
# Mail from Alice - Response to Schema Review

From: Alice
Date: 2025-01-30 09:15
Subject: RE: テーブル定義レビューのお願い

Hi Bob,

了解しました！schema.sql をレビューしました。

初期コメント:
✅ Design good
⚠️ Missing index on orders.user_id
🔴 Pool size needs 20 (currently 10)

詳細コメントは 2025-02-05 まで提供します。

質問: 性能目標はありますか?

Alice
```

**目的**: 同僚に返信する。メールは「相手のメールボックスに直接書き込む」。

---

### Step 9: Skills.md を更新（「新しいパターンを学習」）

```bash
🎓 新しいパターンを学習中...
```

**アクション**: Skills.md に新しいパターンを追加（Pattern #3は既に発見済み）

**例**:
```markdown
## 🆕 Pattern #3: Backup Monitoring Gap

**Status**: Just discovered (2025-01-30)
**Severity**: HIGH
**Prevention**: Email + Slack alerts
**Implementation**: Starting today
```

**目的**: 失敗から学ぶ。次回は同じ失敗をしない。

---

### Step 10: これまでやっていたこと.md を更新（「進捗を記録」）

```bash
💾 永続的記憶を更新中...
```

**ファイル**: `Employees/alice/これまでやっていたこと.md`

**更新例**:
```markdown
## 📋 月間タスク進捗（2025年1月）

### Task 4: New Table Design Review
- Status: 🟡 In Progress
- Completion: 40% → 40% (同じ)
- What done:
  - ✅ schema.sql 初期確認
  - ✅ インデックス戦略検討
  - ✅ Pool size 計算

### New Learning
- Pattern #3 (Backup Monitoring) を発見
- Bob のテーブル設計をレビュー中

### Progress Update
- Total completion: 65% → 70%
```

**目的**: 「これまでやったこと」を更新する。明日起動時に思い出せるように。

---

## 🔄 CLIツール実装例（Pseudocode）

```python
def start_employee_cli(employee_name: str):
    """
    Employee の文脈を完全に読み込む。
    """
    
    # Step 1: WhoAmI を読む
    whoami = read_markdown(f"Employees/{employee_name}/WhoAmI.md")
    print(f"👋 {whoami['name']} がログインしました")
    
    # Step 2: 永続的記憶を読む
    memory = read_markdown(f"Employees/{employee_name}/これまでやっていたこと.md")
    print(f"📋 今月の進捗: {memory['completion_rate']}")
    print(f"⏳ 進行中: {len(memory['in_progress'])} タスク")
    
    # Step 3: Skills を読む
    skills = read_markdown(f"Employees/{employee_name}/Skills.md")
    print(f"🎯 習得パターン: {len(skills['patterns'])} 個")
    for pattern in skills['patterns'][:3]:
        print(f"   - Pattern #{pattern['id']}: {pattern['name']}")
    
    # Step 4: 指示書を読む
    order = read_markdown(f"Employees/{employee_name}/order_{employee_name}_yoro.md")
    print(f"📌 今週の指示: {order['primary_task']['name']}")
    print(f"   優先度: {order['primary_task']['priority']}")
    print(f"   期限: {order['primary_task']['due_date']}")
    
    # Step 5: メールをチェック
    mails = list_files(f"Employees/{employee_name}/Mail/inbox/")
    print(f"📧 メール: {len(mails)} 件")
    for mail in mails:
        print(f"   - From {mail['from']}: {mail['subject']}")
    
    # Step 6: 仕事実行
    print("\n🚀 仕事を開始します...")
    work_result = do_work(employee_name, order, skills, mails)
    
    # Step 7: result.md に出力
    write_markdown(
        f"Employees/{employee_name}/result.md",
        work_result.to_markdown()
    )
    print(f"✅ result.md に結果を出力しました")
    
    # Step 8: メール送信
    for response in work_result.email_responses:
        recipient_name = response['to']
        content = response['content']
        write_markdown(
            f"Employees/{recipient_name}/Mail/inbox/from_{employee_name}_{datetime.now().isoformat()}.md",
            content
        )
    print(f"💌 {len(work_result.email_responses)} 件のメール送信完了")
    
    # Step 9: Skills を更新
    if work_result.new_patterns:
        append_markdown(
            f"Employees/{employee_name}/Skills.md",
            work_result.new_patterns
        )
        print(f"🎓 {len(work_result.new_patterns)} 個の新パターンを学習")
    
    # Step 10: 永続的記憶を更新
    update_memory(
        f"Employees/{employee_name}/これまでやっていたこと.md",
        work_result.progress_update
    )
    print(f"💾 永続的記憶を更新しました")
    
    # 完了
    print("\n✅ 本日の仕事完了！")
    print(f"   - Result: {employee_name}/result.md")
    print(f"   - Skills: {len(work_result.new_patterns)} パターン追加")
    print(f"   - Memory: 進捗を更新")
    print(f"   - Mail: {len(work_result.email_responses)} 件送信")

# 起動方法
if __name__ == "__main__":
    start_employee_cli("alice")
```

---

## 🎯 重要なポイント

### ✅ ファイルベースのメール
- 相手にメールを送る = 相手のメールボックスに直接ファイルを書き込む
- 「Employees/bob/Mail/inbox/from_alice_001.md」に書き込む
- Bob が起動時に同じ場所を見て、Alice からのメールを読む
- No central server needed ✓

### ✅ 永続的記憶
- 「これまでやっていたこと.md」が自動更新される
- 次日起動時に「あ、昨日はこれをやってた」と思い出せる
- 単なるログではなく、生きた「記憶」

### ✅ 失敗パターン
- Skills.md に「このパターンで失敗した」を記録
- 今から同じタスクをする時に「あ、このパターン知ってる」と思い出す
- 同じ失敗を繰り返さない

### ✅ スケールフリー
- 各社員が独立した folder を持つ
- CEO は CEO/Skills.md（年間レベル）のみ
- 係は Employee/Skills.md（日次レベル）のみ
- メモリがオーバーしない

---

## 📂 ディレクトリ構造（全体像）

```
virtual-company/
├── Organization.md           # 組織図
├── EmployeeSystem.md        # このシステムの説明
├── Memory.md                 # 全社の進捗
├── Skills.md                 # 全社の失敗パターン
│
└── Employees/
    ├── alice/
    │   ├── WhoAmI.md         ← CLI起動時に読む（誰か）
    │   ├── これまでやっていたこと.md  ← CLI起動時に読む（思い出す）
    │   ├── Skills.md         ← CLI起動時に読む（パターン）
    │   ├── order_alice_yoro.md ← CLI起動時に読む（指示）
    │   ├── result.md         ← CLI実行時に出力（結果）
    │   └── Mail/
    │       ├── inbox/
    │       │   ├── from_bob_001.md      ← Bob からのメール
    │       │   └── from_charlie_001.md  ← Charlie からのメール
    │       └── outbox/
    │           └── to_bob_001.md        ← Bob への返信（記録）
    │
    ├── bob/
    │   ├── WhoAmI.md
    │   ├── これまでやっていたこと.md
    │   ├── Skills.md
    │   ├── order_bob_yoro.md
    │   ├── result.md
    │   └── Mail/
    │       ├── inbox/
    │       │   └── from_alice_001.md  ← Alice からのメール（ここに書き込み）
    │       └── outbox/
    │
    └── charlie/
        ├── WhoAmI.md
        └── ...
```

---

## 🚀 実際の使い方

### 日々のワークフロー

```bash
# 朝：仕事開始
$ your-cli --start alice
👋 Alice がログイン
📋 昨日のタスク確認: 40% 完了
🎯 パターン確認: 3個
📌 指示確認: Table Design Review
📧 メール確認: 1件（Bob から）

# 仕事中
# ... 実際のコード実行やレビュー作業 ...

# 夜：仕事終了時
$ your-cli --end alice
✅ result.md に出力
💌 Bob にメール返信
🎓 Pattern #3 を学習
💾 進捗を記録

# 翌日：また仕事開始
$ your-cli --start alice
👋 Alice がログイン
📋 昨日のタスク確認: 40% → 50% 完了 ← 更新されている!
🎯 パターン確認: 4個 ← Pattern #3 が追加されている!
🎯 Pattern #3: Backup monitoring (新パターン)
📌 指示確認: Table Design Review（続行）
📧 メール確認: 2件（Bob からの新メール）
```

---

## ✨ 完璧なシステム完成

```
入力: あなたが「codex --yoro」と言う
  ↓
処理: CLIが WhoAmI → Memory → Skills → Order → Mail を読む
  ↓
実行: あなたが仕事をする
  ↓
出力: 
  - result.md（結果）
  - Mail（メール送信）
  - Skills.md（新パターン）
  - Memory.md（進捗）
```

**No central system needed.**  
**No complex logic needed.**  
**Just read and write files.**  

✅ **完成！**
