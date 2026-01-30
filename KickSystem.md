# Kick System - シンプルな実行エンジン

## 🎯 You Kick, System Runs

```
User (You):
  $ codex --kick order.md

Codex:
  ✅ order.md を読む
  ✅ 「今から誰が実行するか」を判定
  ✅ 該当する社員を起動
  ✅ 指示を実行
  ✅ 次実行者を指定
  ✅ 完了

Next Kick:
  $ codex --kick order.md  (自動で次の人が実行)
```

---

## 📋 order.md フォーマット

### シンプルな指示書

```markdown
# Order - 実行指示書

**Status**: ⏳ Waiting for sales
**Current Actor**: sales_alice
**Next Actor**: engineering_bob

---

## 📌 指示

営業チームが顧客から受け取った仕様を、
技術チームに引き渡す。

### Sales Task (営業)
- [ ] 顧客との打ち合わせ完了
- [ ] 仕様書を受け取る
- [ ] Requirements.md に纏める

### Engineering Task (技術)
- [ ] 仕様書を確認
- [ ] 実装計画を立案
- [ ] リスク評価

### QA Task (品質保証)
- [ ] テスト計画を立案
- [ ] テストケース作成

---

## 🔄 Execution Pipeline

1️⃣ **Sales** (営業_Alice)
   └─ 顧客仕様を整理
   └─ Requirements.md に記録
   └─ Next: engineering_bob

2️⃣ **Engineering** (技術_Bob)
   └─ 仕様確認・設計
   └─ Implementation_plan.md に記録
   └─ Next: qa_charlie

3️⃣ **QA** (品質保証_Charlie)
   └─ テスト計画作成
   └─ Test_plan.md に記録
   └─ Next: Done

---

## 📊 Current Status

✅ Sales_Alice: 完了 (2025-01-30 10:00)
⏳ Engineering_Bob: 実行中 (2025-01-30 10:30 start)
⏹️ QA_Charlie: 待機中
```

### 実行フロー

```markdown
**Status**: ⏳ Waiting for engineering
**Current Actor**: engineering_bob
**Next Actor**: qa_charlie

---

(中身は指示)
```

---

## 🚀 CLI の使い方

### 1️⃣ キックする（あなたがやること）

```bash
$ codex --kick order.md

📖 Reading: order.md
🔍 Finding current actor...
  → Current: engineering_bob
  → Next: qa_charlie

🚀 Starting execution...
```

### 2️⃣ Codex が自動的にやること

```
1. order.md を読む
2. **Current Actor** を判定
3. 該当社員を起動
   Employees/engineering_bob/ を読み込み
   - WhoAmI.md
   - これまでやっていたこと.md
   - Skills.md
   - order.md
4. 指示を実行
5. 完了時、**Next Actor** を更新
6. result.md に出力
7. order.md の Status を更新
8. Git push
```

### 3️⃣ 次のキック

```bash
$ codex --kick order.md

📖 Reading: order.md
🔍 Finding current actor...
  → Current: qa_charlie (自動で次の人になっている)
  → Next: (QA完了で None)

🚀 Starting execution...
```

---

## 🧑‍💼 管理職機能

### 管理職がやる2つのこと

#### 1️⃣ 部下の WhoAmI を編集

```bash
# 営業部長が Alice の役割を変更
$ vim Employees/sales_alice/WhoAmI.md

# Before
**Name**: Alice
**Role**: Sales Manager
**Department**: Sales

# After
**Name**: Alice
**Role**: Senior Sales Manager  ← 昇進！
**Department**: Sales
**Team**: Senior Sales Team

$ git add & push
```

#### 2️⃣ 新しい部下を追加（フォルダ作成）

```bash
# 製造部門を追加
$ mkdir -p Employees/manufacturing_dave/Mail/inbox

# 新しい社員の WhoAmI を作成
$ cat > Employees/manufacturing_dave/WhoAmI.md << 'EOF'
# WhoAmI

**Name**: Dave
**Role**: Manufacturing Manager
**Department**: Manufacturing
**Manager**: Director_Manufacturing

## Responsibilities
- Production planning
- Quality control
- Equipment maintenance

## Team
None yet (新規)

---

**Status**: Active
EOF

# これで自動的に Dave が部下になる
# order.md で "manufacturing_dave" を指定するだけで実行される
$ git add & push
```

---

## 👥 会社の構成例

```
Employees/
├── sales_alice/           # 営業
│   ├── WhoAmI.md
│   ├── これまでやっていたこと.md
│   ├── Skills.md
│   └── Mail/
│
├── sales_bob/             # 営業
│   ├── WhoAmI.md
│   └── ...
│
├── engineering_charlie/   # 技術
│   ├── WhoAmI.md
│   └── ...
│
├── engineering_dave/      # 技術
│   ├── WhoAmI.md
│   └── ...
│
├── manufacturing_eve/     # 製造
│   ├── WhoAmI.md
│   └── ...
│
├── qa_frank/              # 品質保証
│   ├── WhoAmI.md
│   └── ...
│
├── hr_grace/              # 総務
│   ├── WhoAmI.md
│   └── ...
│
└── manager_helen/         # 管理職
    ├── WhoAmI.md
    └── (部下の WhoAmI を編集権限)
```

---

## 📋 WhoAmI.md の部門別テンプレート

### 営業（Sales）
```markdown
**Name**: Alice
**Role**: Sales Representative
**Department**: Sales
**Manager**: Manager_Sales

## Responsibilities
- Client meetings
- Proposal creation
- Deal closing

## KPI
- Monthly target: $100k
- Close rate: >30%
```

### 技術（Engineering）
```markdown
**Name**: Bob
**Role**: Software Engineer
**Department**: Engineering
**Manager**: Manager_Engineering

## Responsibilities
- Code implementation
- Code review
- Architecture design

## Technology Stack
- Python
- PostgreSQL
- Docker
```

### 製造（Manufacturing）
```markdown
**Name**: Eve
**Role**: Production Manager
**Department**: Manufacturing
**Manager**: Manager_Manufacturing

## Responsibilities
- Production scheduling
- Quality control
- Equipment maintenance

## Line
- Assembly Line #2
- Staff: 5 people
```

### 品質保証（QA）
```markdown
**Name**: Frank
**Role**: QA Engineer
**Department**: QA
**Manager**: Manager_QA

## Responsibilities
- Test case design
- Test execution
- Bug tracking

## Tools
- TestNG
- Selenium
- JIRA
```

### 総務（HR）
```markdown
**Name**: Grace
**Role**: HR Manager
**Department**: HR
**Manager**: CEO

## Responsibilities
- Recruitment
- Employee relations
- Payroll

## Headcount
- Current: 25
- Target: 30
```

---

## 🔄 実行例：営業 → 技術 → 品質保証

### Step 1: 営業がキック

```bash
$ codex --kick order.md

📖 order.md読み込み中...
🔍 Current Actor: sales_alice
   Next Actor: engineering_bob

👤 Alice (Sales) がタスク実行中...
  - 顧客打ち合わせ実施
  - 仕様書取得
  - Requirements.md 作成

✅ Alice 完了
📝 order.md 更新:
   Status: ⏳ Waiting for engineering
   Current Actor: engineering_bob  ← 自動更新
   Last: sales_alice (2025-01-30 11:00)
```

### Step 2: 技術がキック（あなたが再度キック）

```bash
$ codex --kick order.md

📖 order.md読み込み中...
🔍 Current Actor: engineering_bob
   Next Actor: qa_charlie

👤 Bob (Engineering) がタスク実行中...
  - 仕様確認
  - 設計実施
  - Implementation_plan.md 作成

✅ Bob 完了
📝 order.md 更新:
   Status: ⏳ Waiting for QA
   Current Actor: qa_charlie  ← 自動更新
   Last: engineering_bob (2025-01-30 15:00)
```

### Step 3: 品質保証がキック

```bash
$ codex --kick order.md

📖 order.md読み込み中...
🔍 Current Actor: qa_charlie
   Next Actor: None (完了)

👤 Charlie (QA) がタスク実行中...
  - テスト計画作成
  - テストケース設計
  - Test_plan.md 作成

✅ Charlie 完了
📝 order.md 更新:
   Status: ✅ DONE
   Current Actor: None
   Last: qa_charlie (2025-01-30 17:00)
```

---

## 🔀 複雑なパイプライン例

### 営業 → 技術 → 製造 → 品質保証 → 総務

```markdown
# Order - 新製品立ち上げ

**Status**: ⏳ Waiting for sales
**Current Actor**: sales_alice
**Actors**: sales_alice → engineering_bob → manufacturing_eve → qa_frank → hr_grace

---

## Pipeline

1️⃣ Sales (営業_Alice)
   └─ 市場調査・顧客要件確認
   └─ Next: engineering_bob

2️⃣ Engineering (技術_Bob)
   └─ 製品設計・仕様確定
   └─ Next: manufacturing_eve

3️⃣ Manufacturing (製造_Eve)
   └─ 生産計画・生産準備
   └─ Next: qa_frank

4️⃣ QA (品質保証_Frank)
   └─ テスト実施・品質確認
   └─ Next: hr_grace

5️⃣ HR (総務_Grace)
   └─ 販売研修・ドキュメント配布
   └─ Next: Done
```

---

## 🎯 分岐パイプライン例

複数の並列実行も可能：

```markdown
# Order - 複数部門対応

**Status**: ⏳ Multi-actor execution
**Current Actors**: 
  - sales_alice (営業)
  - engineering_bob (技術)
  - manufacturing_eve (製造)

**Next Actors**:
  - qa_frank (全部門の成果を統合テスト)

---

各部門が並列実行后、
QAが集約テスト → 完了
```

実装はシンプル：
```markdown
**Current Actors**: [sales_alice, engineering_bob, manufacturing_eve]
**Next Actors**: [qa_frank]

Codex は複数を並列実行、全て完了後に qa_frank へ
```

---

## 💾 order.md の最小フォーマット

```markdown
# Order

**Status**: ⏳ Waiting for sales_alice
**Current Actor**: sales_alice
**Next Actor**: engineering_bob

---

営業は顧客から仕様を取得してください。
```

それだけでOK。
- Codex が sales_alice を起動
- Sales_alice の WhoAmI, Skills, Memory を全て読み込む
- 指示を実行
- 完了時に Status を更新
- Next Actor が自動的に「現在のActor」になる

---

## 🛠️ CLI 実装（Pseudocode）

```python
def kick_system(order_file: str):
    """
    キックシステムの実行エンジン
    """
    
    # Step 1: order.md を読む
    order = read_markdown(order_file)
    
    # Step 2: Current Actor を判定
    current_actor = order['Current Actor']
    next_actor = order['Next Actor']
    
    if not current_actor:
        print("✅ Pipeline complete!")
        return
    
    # Step 3: 社員フォルダを起動
    employee_folder = f"Employees/{current_actor}/"
    
    # Step 4: 社員のコンテキストを読み込む
    whoami = read(f"{employee_folder}/WhoAmI.md")
    memory = read(f"{employee_folder}/これまでやっていたこと.md")
    skills = read(f"{employee_folder}/Skills.md")
    mails = list_files(f"{employee_folder}/Mail/inbox/")
    
    print(f"👤 {whoami['Name']} ({whoami['Role']}) がタスク実行中...")
    
    # Step 5: 指示を実行
    result = execute_order(order, whoami, skills)
    
    # Step 6: 結果を出力
    write_file(f"{employee_folder}/result.md", result)
    
    # Step 7: order.md を更新 ← 重要！
    order['Status'] = f"⏳ Waiting for {next_actor}" if next_actor else "✅ DONE"
    order['Current Actor'] = next_actor
    order['Last Completed By'] = current_actor
    order['Last Completed At'] = get_timestamp()
    
    write_markdown(order_file, order)
    
    # Step 8: Git push
    git_commit(f"chore: Update order - {current_actor} completed")
    git_push()
    
    print(f"✅ {current_actor} completed")
    if next_actor:
        print(f"👉 Next: {next_actor}")
    else:
        print("🎉 Pipeline complete!")
```

---

## 👨‍💼 管理職の権限

### 権限1: 部下の WhoAmI 編集

```bash
# Manager が部下を昇進させたい
$ vim Employees/sales_alice/WhoAmI.md

# Role を更新
**Name**: Alice
**Role**: Senior Sales Manager  ← 昇進
**Salary**: $150k  ← 給与更新

$ git add & commit & push
# Alice が次回起動時に新しいロールで実行される
```

### 権限2: 新しい部下を追加

```bash
# 新しい製造マネージャーを雇用
$ mkdir -p Employees/manufacturing_dave/Mail/inbox

$ cat > Employees/manufacturing_dave/WhoAmI.md << 'EOF'
**Name**: Dave
**Role**: Manufacturing Manager
**Department**: Manufacturing
**Manager**: Manager_Manufacturing
EOF

$ git add & commit & push

# これでもう Dave は "manufacturing_dave" として
# order.md で使用可能
```

### 権限3: order.md でパイプラインを指定

```bash
# 新しいプロセスを定義
$ cat > order_new_product_launch.md << 'EOF'
# Order - 新製品立ち上げ

**Current Actor**: sales_alice
**Next Actor**: engineering_bob
...
EOF

$ git add & commit & push
$ codex --kick order_new_product_launch.md
```

---

## ✨ 完璧なシンプルさ

**あなたがやること**:
```bash
$ codex --kick order.md
```

**管理職がやること**:
- WhoAmI.md を vim で編集（昇進、部門変更など）
- フォルダを mkdir で作成（新人採用）
- order.md で実行フロー指定

**Codex がやること**:
- 全自動実行
- コンテキスト読み込み
- 次の人に自動バトンタッチ
- 全て Git に記録

---

**Status**: 🟢 **Kick System Ready**

これが本当のシンプルさです。 🚀
