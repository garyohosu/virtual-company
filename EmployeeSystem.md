# Employee System - ファイルベースメール + 永続的記憶

## 🎯 社員ごとのコンテキストシステム

各社員が起動時に読むファイル構成です。

```
Employees/
├── alice/
│   ├── WhoAmI.md                    ← 「私は誰か」
│   ├── これまでやっていたこと.md      ← 永続的記憶（アップデート）
│   ├── Skills.md                    ← 失敗パターン学習
│   ├── order_alice_yoro.md          ← 今の指示書
│   ├── result.md                    ← 仕事結果
│   └── Mail/
│       ├── inbox/
│       │   ├── from_bob_001.md      ← Bob からのメール
│       │   └── from_charlie_001.md  ← Charlie からのメール
│       └── outbox/
│           ├── to_bob_001.md        ← Bob への返信（自動作成）
│           └── to_charlie_001.md    ← Charlie への返信
│
├── bob/
│   ├── WhoAmI.md
│   ├── これまでやっていたこと.md
│   ├── Skills.md
│   ├── order_bob_yoro.md
│   ├── result.md
│   └── Mail/
│       ├── inbox/
│       │   └── from_alice_001.md
│       └── outbox/
│
└── charlie/
    ├── WhoAmI.md
    ├── これまでやっていたこと.md
    ├── Skills.md
    ├── order_charlie_yoro.md
    ├── result.md
    └── Mail/
        ├── inbox/
        └── outbox/
```

---

## 📋 CLI起動時の読み込みフロー

```
$ your-cli --employee alice

1️⃣ WhoAmI.md を読む
   「私は Alice です。データベース管理者です。」

2️⃣ これまでやっていたこと.md を読む
   「昨日 DB をバックアップした。
    先週 インデックスを最適化した。
    今月のタスク: 完了度 60%」

3️⃣ Skills.md を読む
   「Pattern #1: SQL Injection 対策
    Pattern #2: Connection pool timeout
    → これから実行するコードをチェックしよう」

4️⃣ order_alice_yoro.md を読む
   「タスク: テーブル設計レビュー
    期限: 2025-02-15
    優先度: HIGH」

5️⃣ Mail/inbox/ を確認
   「Bob からメール: 『テーブル定義が必要』
    Charlie からメール: 『バックアップ確認したい』」

6️⃣ 仕事実行
   「OK、分かった。テーブル設計をレビューしよう」

7️⃣ 結果を result.md に出力
   「✅ テーブル設計レビュー完了
    発見: インデックス不足
    推奨: 複合インデックスを追加」

8️⃣ 必要に応じて相手にメール
   「Bob のメールに返信
    Employees/bob/Mail/inbox/from_alice_002.md に書き込み」

9️⃣ 失敗を記録
   「SQL のパフォーマンス問題を見つけた
    Skills.md に Pattern #3 として追加」

🔟 これまでやっていたこと.md を更新
   「テーブル設計レビュー: 完了
    発見: インデックス不足
    今月のタスク: 完了度 75%」
```

---

## 📄 各ファイルのテンプレート

### WhoAmI.md

```markdown
# WhoAmI - Identity

**Name**: Alice  
**Role**: Database Administrator  
**Team**: Manager_A1 (課長 A1 の部下)  
**Experience**: 5 years  

## Responsibilities
- Database design and optimization
- Backup and recovery
- Performance monitoring
- Schema migrations

## Skills
- PostgreSQL
- Query optimization
- Backup automation
- Linux administration

## Contact
- Email: alice@virtualcompany.local
- Slack: @alice_db

## Manager
- Manager: Manager_A1
- Manager Email: Employees/manager_a1/Mail/inbox/

## Team Members
- Bob (another DBA)
- Charlie (Developer)
```

### これまでやっていたこと.md

```markdown
# これまでやっていたこと - Persistent Memory

## 今月 (2025年1月)

### 完了したタスク
- [x] 日次バックアップスクリプト作成 (完了日: 2025-01-25)
  - スクリプト: `backup.sh`
  - 自動化: ✅ (毎日 02:00 実行)
  - テスト: ✅ (3回成功)

- [x] DB インデックス最適化 (完了日: 2025-01-20)
  - 対象: users テーブル
  - 効果: クエリ速度 40% 向上
  - スクリプト: `optimize_index.sql`

### 進行中のタスク
- [ ] テーブル設計レビュー (進度: 50%)
  - 開始: 2025-01-30
  - 期限: 2025-02-15
  - 依頼元: Bob, Charlie
  - Status: schema.sql レビュー中

- [ ] 接続プール設定 (進度: 30%)
  - 現在: デフォルト設定で実行中
  - 改善案: Pool size 10 → 20
  - テスト予定: 来週

### 発見した問題
1. Connection timeout が月2回発生
   - 原因: Pool size が小さすぎる
   - 対策: Skills.md Pattern #2 参照

2. SQL クエリが遅い
   - テーブル: orders
   - 理由: インデックスがない
   - 推奨: 複合インデックス追加

### 先月 (2024年12月)

- [x] ストレージ拡張 (完了)
- [x] 復旧手順 マニュアル作成 (完了)
- [x] チーム研修: バックアップ戦略 (完了)

## 重要な学習
- Pattern #1: SQL Injection は業務では避けられない → 常にチェック
- Pattern #2: Connection pool の計画が重要 → 事前に算出

## 完了度
- 1月: 60% (3/5 タスク完了予定)
- 予定: 2月は 70% 目指す

## 困ったこと
- テーブル設計レビューが遅い（Bob からのメール待ち）
- インデックス追加の優先度が不明（Manager に相談予定）
```

### Skills.md

```markdown
# Alice's Skills - Failure Patterns & Prevention

## Pattern #1: SQL Injection 🔴

**What**: SQL クエリを安全でない方法で構築してしまった

**When**: 他チームのコードレビュー時

**Why**:
- String concatenation を使ってた
- Parameterized query を忘れてた

**Prevention**:
```sql
-- ❌ Never do this
query = "SELECT * FROM users WHERE id = " + user_id;

-- ✅ Always do this
query = "SELECT * FROM users WHERE id = ?";
execute(query, [user_id]);
```

**Last Incident**: 2024-12-15  
**Status**: ✅ チーム全体に周知済み

---

## Pattern #2: Connection Pool Timeout 🟡

**What**: 接続がタイムアウトして処理が止まった

**When**: ロードテスト中

**Why**:
- Pool size がデフォルト (10) のままだった
- 並列クエリが 15 個発生した
- プールが空になった

**Prevention**:
1. 事前にピークロード を計算
2. Pool size = ピークロード × 1.5 に設定
3. Connection timeout ログを監視

**Last Incident**: 2025-01-18  
**Status**: ⏳ 修正中 (Pool size を 20 に変更予定)

---

## Pattern #3: Backup失敗（新）✨

**What**: バックアップスクリプトが失敗していたのに気づかなかった

**When**: 定期バックアップ確認時

**Why**:
- Cron ジョブのエラーログをチェックしていなかった
- 最後の成功日時を 3ヶ月追跡していなかった

**Prevention**:
- バックアップ完了 email を受け取る
- 失敗時は Slack alert
- 週1回の手動確認

**Learned**: 2025-01-30 (今日!)  
**Status**: これから実装

---

## 避けるべき判断ミス

1. セキュリティをテストに優先順位をつけない
2. バックアップを「セットして忘れる」と思う
3. インデックスなしでオンプレで動かす
4. Connection pool を デフォルトで運用する

---

## 成功パターン

✅ Parameterized queries は 100% 使う
✅ Backup 監視は自動化する
✅ Indexing は Query plan を見て判断
✅ Load test は本番の 2倍で実行
```

### order_alice_yoro.md

```markdown
# Order for Alice - Weekly Task

## Week: 2025-02-03 to 2025-02-07

### Primary Task: Table Design Review

**Status**: ⏳ In Progress  
**Priority**: HIGH  
**Due**: 2025-02-15

**Details**:
Bob と Charlie からのテーブル定義レビュー依頼

**What to do**:
1. schema.sql を確認
2. インデックス戦略をレビュー
3. パフォーマンスを予測
4. セキュリティをチェック（Pattern #1）
5. Connection pool の設計を確認（Pattern #2）

**Deliverable**:
- Review comments (GitHub)
- インデックス提案
- 修正スクリプト

---

### Secondary Task: Connection Pool Fix

**Status**: ⏳ Waiting for approval  
**Priority**: MEDIUM  
**Due**: 2025-02-10

**Details**:
Pool size を 10 → 20 に変更してテスト

**What to do**:
1. Pool size 計算を verify
2. Staging でテスト
3. ロードテスト実行
4. 本番への計画を立案

---

### Blockers

- ⏳ Bob が schema.sql を提出待ち
  - Follow-up: 今日メールを送る

- ⏳ Manager に インデックス優先度 を相談したい
  - Action: Manager_A1 にメール

---

### Pattern Check Before Starting

1. **Pattern #1: SQL Injection** ✅
   - schema.sql に入力値バリデーションあるか確認

2. **Pattern #2: Connection Pool** ✅
   - Pool size は 2025年のロード計画で OK か確認

3. **Pattern #3: Backup** ✅
   -新しいテーブルのバックアップ戦略も確認

---

**Start**: 今日 (2025-02-03)  
**Daily Report**: 毎日 17:00
```

### Mail/inbox/from_bob_001.md

```markdown
# Mail from Bob - Inbox

**From**: Bob  
**Date**: 2025-02-02 14:30  
**Subject**: テーブル定義レビューのお願い

---

## Message

Hi Alice,

Could you review the table schema for the new order system?

Files:
- schema.sql: Table definitions
- indexes.sql: Index strategy
- performance_estimate.txt: Expected query performance

I need your feedback on:
1. Design correctness
2. Index strategy
3. Connection pool sizing

Deadline: 2025-02-15

Thanks!

Bob

---

## Action Items for Alice

- [ ] schema.sql を読む
- [ ] indexes.sql を確認
- [ ] インデックス戦略を検討
- [ ] Pool size 計算を verify
- [ ] Review comments を返す

**Response**:  
Alice が返信を書いたら → Employees/bob/Mail/inbox/from_alice_002.md に書き込み
```

### Mail/outbox/to_bob_001.md

```markdown
# Mail to Bob - Outbox

**To**: Bob  
**Date**: 2025-02-03 09:15  
**Subject**: RE: テーブル定義レビューのお願い

---

## Message

Hi Bob,

Got it! I'll review schema.sql and indexes.sql by 2025-02-10.

First thoughts:
- I need to check SQL Injection prevention (my Pattern #1)
- Pool size calculation needs update for 2025 load
- Will do performance analysis

I'll send detailed comments by next week.

One question: Do you have performance targets for the new system?

Alice

---

## Files Attached
- performance_checklist.txt: My review process

---

## Status
✅ Sent to Bob's inbox: Employees/bob/Mail/inbox/from_alice_001.md
```

### result.md

```markdown
# Result - Task Completion Report

**Date**: 2025-02-03  
**Employee**: Alice  
**Manager**: Manager_A1  

---

## Summary

✅ **Status**: Completed with findings

---

## Tasks Completed Today

### Task 1: Table Schema Review (Started)
- **Status**: 🟡 In Progress (40%)
- **What**: schema.sql の初期確認
- **Findings**:
  - ✅ SQL Injection prevention: Good (using parameterized)
  - ⚠️ Indexes: Missing on `orders.user_id`
  - 🔴 Connection pool: Needs recalculation

### Task 2: Mail Handling
- **Status**: ✅ Complete
- **What**: Bob と Charlie からのメール確認
- **Actions**:
  - ✅ Bob に返信（from_alice_001.md）
  - ⏳ Charlie に返信（to_charlie_001.md 作成予定）

---

## Issues Found

### Issue #1: Missing Index 🟡
- **Table**: orders
- **Column**: user_id
- **Impact**: Slow query (scan が必要)
- **Fix**: `CREATE INDEX idx_orders_user_id ON orders(user_id);`
- **Estimate**: 5 分で修正

### Issue #2: Connection Pool Undersized 🔴
- **Current**: Pool size 10
- **Needed**: Pool size 20 (for 2025 peak load)
- **Impact**: Timeout risk under load
- **Fix**: Connection pool config を更新
- **Estimate**: 2 時間テスト + 本番適用

---

## Skills Updated

### New Pattern Added: Pattern #3: Backup Failed Silent ✨
- **Issue**: バックアップが失敗してても気づかない
- **Prevention**: Email notification + Slack alert
- **Status**: Skills.md に追加（新パターン）

---

## これまでやっていたこと 更新

**Updated**: これまでやっていたこと.md

```
- [x] テーブル設計レビュー (進度: 40% → 40%)
- [x] Bob, Charlie からのメール確認 (完了)
- 新しく見つけた問題: Missing index on orders.user_id
- 新しく見つけた問題: Pool size needs update

今月の進度: 60% → 65%
```

---

## Communication

### Emails Sent
- ✅ to_bob_001.md (返信)
  - Destination: Employees/bob/Mail/inbox/from_alice_001.md

### Emails Received
- ✅ from_bob_001.md (テーブル定義レビュー依頼)
- ⏳ from_charlie_001.md (確認予定)

### Escalations
- ⏳ Manager_A1 に相談予定
  - Subject: インデックス追加の優先度

---

## Tomorrow's Plan

- [ ] Charlie からのメール確認・返信
- [ ] schema.sql の詳細レビュー続行
- [ ] インデックス修正スクリプト作成
- [ ] Manager に相談（優先度確認）

---

## Manager Check-in

**For Manager_A1**:
- テーブルレビューは順調に進捗中
- 2つの潜在的な issue を発見
- Backup 監視の新しいパターンを学習
- 明日も頑張ります！

---

**Time Log**:
- 09:00-10:00: Bob のメール確認・返信（1時間）
- 10:00-11:30: Schema.sql 初期確認（1.5時間）
- 11:30-12:00: Issues ドキュメント化（0.5時間）
- 12:00-13:00: ランチ
- 13:00-14:00: Skills.md 更新・新パターン追加（1時間）
- 14:00-15:00: これまでやっていたこと.md 更新（1時間）

**Total**: 6 hours (実務 5.5h + 記録 0.5h)

---

**Status**: Ready for Manager review  
**Next Review**: 2025-02-04
```

---

## 🔄 CLIロジック（流れ）

```python
# pseudocode

def start_cli(employee_name):
    # Step 1: WhoAmI を読む
    identity = read_file(f"Employees/{employee_name}/WhoAmI.md")
    print(f"👋 {identity.name} がログインしました")
    
    # Step 2: これまでやっていたこと を読む
    memory = read_file(f"Employees/{employee_name}/これまでやっていたこと.md")
    print(f"📝 先月のタスク完了度: {memory.completion_rate}")
    print(f"⏳ 進行中: {memory.in_progress_tasks}")
    
    # Step 3: Skills を読む（失敗防止）
    skills = read_file(f"Employees/{employee_name}/Skills.md")
    print(f"🎯 知ってるパターン: {len(skills.patterns)} 個")
    print(f"   - Pattern #1: {skills.patterns[0].name}")
    print(f"   - Pattern #2: {skills.patterns[1].name}")
    
    # Step 4: 指示書を読む
    order = read_file(f"Employees/{employee_name}/order_{employee_name}_yoro.md")
    print(f"📋 今週の指示: {order.primary_task}")
    print(f"   優先度: {order.priority}")
    print(f"   期限: {order.due_date}")
    
    # Step 5: メールを確認
    inbox = list_files(f"Employees/{employee_name}/Mail/inbox/")
    print(f"📧 メール: {len(inbox)} 件")
    for mail in inbox:
        print(f"   - {mail.from}: {mail.subject}")
    
    # Step 6: 仕事実行
    print("\n🚀 仕事を開始します...")
    # [仕事実行]
    
    # Step 7: result.md に出力
    result = {
        "tasks_completed": [...],
        "issues_found": [...],
        "skills_updated": [...],
        "emails_sent": [...],
    }
    write_file(f"Employees/{employee_name}/result.md", result)
    
    # Step 8: メール送信
    # 相手のメールボックスに書き込む
    write_file(f"Employees/bob/Mail/inbox/from_alice_002.md", message)
    
    # Step 9: Skills 更新
    update_file(f"Employees/{employee_name}/Skills.md", new_patterns)
    
    # Step 10: これまでやっていたこと 更新
    update_file(f"Employees/{employee_name}/これまでやっていたこと.md", new_progress)
    
    print("✅ 仕事完了！")
    print("   - Result: result.md に保存")
    print("   - Skills: 新パターンを追加")
    print("   - Memory: 進捗を更新")
```

---

## 🎯 メールシステムの使い方

### 相手にメール送信する

```markdown
# Employees/bob/Mail/inbox/from_alice_002.md を作成

**From**: Alice  
**Date**: 2025-02-03 15:00  
**Subject**: RE: テーブル定義レビュー - 初期コメント

---

Hi Bob,

初期確認が終わりました：

1. SQL Injection: ✅ Good (parameterized queries)
2. Indexes: ⚠️ Missing on orders.user_id
3. Pool: 🔴 Need to increase pool size

詳細コメントは明日お送りします。

Alice
```

**Important**: 
- Bob は Employees/bob/Mail/inbox/ を見て Alice からのメール を確認
- Alice は Employees/bob/Mail/inbox/ に直接書き込む（outbox は参考用）

---

## 📊 ファイルの更新タイミング

| ファイル | いつ更新 | 誰が | 内容 |
|---------|--------|------|------|
| **WhoAmI.md** | 初回のみ | 本人 | 自己紹介（変わらない） |
| **これまでやっていたこと.md** | 毎日夕方 | 本人 | タスク進捗・学習 |
| **Skills.md** | 失敗時 | 本人 | 新しいパターン追加 |
| **order_*.md** | Manager が | Manager | 新しいタスク指示 |
| **Mail/inbox/** | 相手が | 他の人 | メール受け取り |
| **Mail/outbox/** | 送信時 | 本人 | メール送信記録 |
| **result.md** | 仕事終了時 | 本人 | 日報 |

---

**System Ready!** 🎉

各社員が起動時に自分のコンテキストを完全に思い出し、
失敗から学び、メールで同僚と連絡し、
仕事の結果を記録する。

完璧な **ファイルベース永続的記憶 + メールシステム** です。
