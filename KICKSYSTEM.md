# Virtual Company - Kick System Edition

**You Kick. System Runs. Forever.**

---

## ⚡ Quick Start

```bash
# That's it. Just kick.
$ codex --kick order.md

# System automatically:
# 1. Reads order.md
# 2. Finds Current Actor: sales_alice
# 3. Launches Sales_Alice (with full context)
# 4. Executes instructions
# 5. Updates order.md: Next Actor becomes Current
# 6. Git push
# 
# Next kick: engineering_bob auto-starts
```

---

## 🎯 Three Simple Rules

### Rule 1: You Kick
```bash
$ codex --kick order.md
```

### Rule 2: Managers Manage
```bash
# Edit employee's role
vim Employees/sales_alice/WhoAmI.md
git add & push

# Create new employee
mkdir -p Employees/manufacturing_dave/Mail/inbox
# Add WhoAmI.md
git add & push

# Create new workflow
cat > order_new_product.md
git add & push
```

### Rule 3: System Learns
```
Every execution:
✅ Updates Memory.md
✅ Learns from Skills.md
✅ Records in Git
✅ Auto-commits

Next kick: System smarter
```

---

## 📊 System Architecture

```
┌─────────────────────────────────────────┐
│          Kick System                    │
│      (You: codex --kick order.md)       │
├─────────────────────────────────────────┤
│                                         │
│  1. Parse order.md                      │
│     ├─ Current Actor: sales_alice       │
│     └─ Next Actor: engineering_bob      │
│                                         │
│  2. Launch Employee Context             │
│     ├─ WhoAmI.md (who am I?)           │
│     ├─ Memory.md (what did I do?)      │
│     ├─ Skills.md (prevent failures)    │
│     └─ Mail/inbox/ (any messages?)     │
│                                         │
│  3. Execute Instructions                │
│     └─ sales_alice does sales tasks    │
│                                         │
│  4. Update State                        │
│     ├─ result.md (what I did)          │
│     ├─ Memory.md (update progress)     │
│     ├─ Skills.md (new patterns)        │
│     └─ order.md (next actor)           │
│                                         │
│  5. Git Push                            │
│     └─ All changes recorded            │
│                                         │
└─────────────────────────────────────────┘
```

---

## 👥 Company Structure

```
Employees/
├── sales_alice/           ← Sales Team
├── sales_bob/
├── engineering_charlie/   ← Engineering Team
├── engineering_dave/
├── manufacturing_eve/     ← Manufacturing Team
├── manufacturing_frank/
├── qa_grace/              ← QA Team
├── qa_henry/
├── hr_iris/               ← HR Team
└── manager_jack/          ← Management
```

Each is just a **folder**. Each folder has:
```
[department_name]/
├── WhoAmI.md              # Who they are
├── Memory.md              # What they did
├── Skills.md              # What they learned
├── Mail/inbox/            # Messages
└── result.md              # What they output
```

---

## 🔄 Example Workflow: Sales → Engineering

### Step 1: Initial State

```
order.md:
  Current Actor: sales_alice
  Next Actor: engineering_bob
```

### Step 2: You Kick

```bash
$ codex --kick order.md

👤 Alice (Sales) is executing...
  - Customer meeting notes
  - Create customer_requirements.md
  - Create sales_proposal.md

✅ Alice completed at 2025-01-30 17:00
```

### Step 3: System Updates

```
order.md (auto-updated):
  Current Actor: engineering_bob  ← Was "Next"
  Next Actor: manufacturing_eve   ← New next
  Last: sales_alice (2025-01-30 17:00)
  Status: ⏳ Waiting for engineering

Git: auto-committed
```

### Step 4: Next Kick

```bash
$ codex --kick order.md

👤 Bob (Engineering) is executing...
  - Read customer_requirements.md
  - Create implementation_plan.md
  - Create system_design.md

✅ Bob completed at 2025-01-31 15:00
```

### Magic: Bob didn't need instructions!
- He read the order.md
- He read what Alice did
- He knew what to do next
- **Automatic context continuity**

---

## 🎓 Learning System Integration

```
Each Employee Has:

WhoAmI.md
├─ Name, Role, Department
├─ Responsibilities
└─ Authority level

Memory.md
├─ Previous tasks completed
├─ Current status
├─ What worked/didn't work
└─ Lessons learned

Skills.md
├─ Pattern #1: Common mistake
├─ Pattern #2: Common mistake
├─ Pattern #3: Common mistake
└─ [Auto-grows with experience]

Mail/inbox/
├─ Messages from manager
├─ Messages from other teams
├─ Requests for info
└─ [Auto-marked as read when processed]
```

**Result**: System remembers. System learns. System gets smarter.

---

## 👨‍💼 Management Operations

### 1️⃣ Promote Employee

```bash
vim Employees/sales_alice/WhoAmI.md

# Change:
**Role**: Sales Representative
# To:
**Role**: Senior Sales Manager

git add & push
# Alice is now promoted. Next kick she runs as manager.
```

### 2️⃣ Hire New Employee

```bash
mkdir -p Employees/manufacturing_david/Mail/inbox

cat > Employees/manufacturing_david/WhoAmI.md << 'EOF'
**Name**: David
**Role**: Production Manager
**Department**: Manufacturing
**Manager**: Manager_Manufacturing
EOF

git add & push
# David is now in the system. Can be used in order.md
```

### 3️⃣ Create New Workflow

```bash
cat > order_product_launch.md << 'EOF'
**Current Actor**: sales_alice
**Next Actor**: engineering_bob
**Next Next**: manufacturing_eve
**Next Next Next**: qa_frank

# Product Launch Workflow
...
EOF

git add & push

# Ready to kick:
$ codex --kick order_product_launch.md
```

### 4️⃣ Organize Multiple Projects

```
orders/
├── order_customer_integration.md
├── order_product_launch.md
├── order_bug_fix.md
└── order_infrastructure_upgrade.md

# Each can run independently
$ codex --kick order_customer_integration.md
$ codex --kick order_product_launch.md
# etc.
```

---

## 💾 State Management

### order.md evolves:

```markdown
# Initial
**Status**: ⏳ Waiting for sales_alice
**Current Actor**: sales_alice
**Next Actor**: engineering_bob

---
[after kick 1]

**Status**: ⏳ Waiting for engineering_bob
**Current Actor**: engineering_bob
**Next Actor**: manufacturing_eve
**Completed**: [sales_alice at 2025-01-30 17:00]

---
[after kick 2]

**Status**: ⏳ Waiting for manufacturing_eve
**Current Actor**: manufacturing_eve
**Next Actor**: qa_frank
**Completed**: [engineering_bob at 2025-01-31 15:00]

---
[after kick 3]

**Status**: ⏳ Waiting for qa_frank
**Current Actor**: qa_frank
**Next Actor**: None
**Completed**: [manufacturing_eve at 2025-02-01 12:00]

---
[after kick 4]

**Status**: ✅ DONE
**Current Actor**: None
**Next Actor**: None
**Completed**: [qa_frank at 2025-02-02 16:00]
```

---

## ✨ Why This Works

### 1. Simple for You
```bash
$ codex --kick order.md
# Done. One command.
```

### 2. Self-Healing System
```
Each employee has their full context:
✅ Who they are (WhoAmI)
✅ What they did (Memory)
✅ What they learned (Skills)
✅ What they need (Mail)

→ No "context loss"
→ No "miscommunication"
→ Every step correct
```

### 3. Automatic Learning
```
Year 1:
- Employee encounters error
- Records in Skills.md
- Next similar situation → knows the fix

Year 2:
- Same employee encounters new error
- But similar to old pattern
- Recognizes it, avoids it

Year 5:
- Employee is expert
- Has learned 365 patterns
- Makes no mistakes
```

### 4. Scales to Infinity
```
1 employee: Works
10 employees: Works
100 employees: Works
1000 employees: Works

Why? Because each employee only manages their own:
✅ Memory (their history)
✅ Skills (their lessons)
✅ Tasks (their work)

No central "god controller"
Each is independent
System scales effortlessly
```

---

## 🚀 Roadmap

### ✅ Done
- [x] KickSystem.md (architecture)
- [x] order.md (template)
- [x] Employees/sales_alice/ (example)
- [x] Employees/engineering_bob/ (example)

### ⏳ Next
- [ ] Implement CLI: `codex --kick order.md`
- [ ] Test with Alice → Bob pipeline
- [ ] Add manufacturing_eve
- [ ] Add qa_frank
- [ ] Run complete 4-step workflow

### 🎯 Final
- [ ] 10+ employees working
- [ ] Multiple concurrent workflows
- [ ] Full production use

---

## 📂 Folder Structure (Complete)

```
virtual-company/
├── README.md                     # Main entry
├── SYSTEM.md                     # Full vision
├── KickSystem.md                 # This file (THE CORE)
├── order.md                      # Template workflow
│
├── Employees/
│   ├── sales_alice/
│   │   ├── WhoAmI.md            # Saleswoman
│   │   ├── Memory.md            # What she did
│   │   ├── Skills.md            # What she learned
│   │   └── Mail/inbox/
│   │
│   ├── engineering_bob/
│   │   ├── WhoAmI.md            # Engineer
│   │   ├── Memory.md
│   │   ├── Skills.md
│   │   └── Mail/inbox/
│   │
│   ├── manufacturing_eve/       # (To be created)
│   ├── qa_frank/                # (To be created)
│   └── ...
│
└── (Other docs)
```

---

## 🎉 The Beauty of Simplicity

```
Before:
  - Slack messages everywhere
  - Email chains confused
  - "Who was supposed to do this?"
  - Context lost
  - Mistakes repeated
  
After (Kick System):
  - One file per workflow
  - Clear actor sequence
  - "Who's next?" = In the file
  - Context preserved
  - Mistakes learned and prevented

Tool: $ codex --kick order.md
Cost: 1 command
Result: Entire organization runs automatically
```

---

## 🎯 Remember

- **You**: `codex --kick order.md`
- **Manager**: Edit WhoAmI.md, mkdir new employees
- **System**: Learns, remembers, improves forever
- **Result**: Self-running organization

---

**Status**: 🟢 **Ready to Implement**

Let's build this. 🚀
