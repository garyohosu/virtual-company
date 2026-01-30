# Virtual Company - AI Agent Automation Framework

## 🚀 What is Virtual Company?

Virtual Company is a **fully automated CI/CD system** with **persistent learning and memory**.

```
You write task → Agents read GitHub → Agents learn from past → Execute → Results
```

---

## ⚡ How to Use (30 seconds)

### 1. Create Task
```bash
# Edit with Claude.ai
tasks/CURRENT_TASK.md
# Describe what needs to be done
```

### 2. Kick Agents (4 commands)
```bash
cd ~/virtual-company && git pull

codex "git pull して order_codex.md を実行してください"
gemini "git pull して order_gemini.md を実行してください"
claude "git pull して order_claude.md を実行してください"
genspark (open browser, run order_genspark.md)
```

### 3. Read Results
```
GitHub → results/codex/RESULT.md        (What was generated)
      → results/gemini/RESULT.md        (What risks found)
      → results/claude/RESULT.md        (What approved)
      → results/genspark/RESULT.md      (What tests passed)
```

Done! 🎉

---

## 📖 Key Files to Read

| File | Purpose | Read When |
|------|---------|-----------|
| **Agents.md** | Complete framework | First time |
| **Skills.md** | Learn from past errors | Every task (digest) |
| **Memory.md** | Current project state | Every task |
| **README.md** | Quick reference | This page |
| **order_*.md** | Agent-specific steps | Agent-specific |

---

## 💡 The Three-Layer System

### Layer 1: Framework (Agents.md)
- How the system works
- Four agents explained
- Universal workflow
- Output standards

### Layer 2: Learning (Skills.md) - Persistent Learning
**How it works:**
```
Skills.md (digest, 2 minutes read)
  ├─ "Error Pattern 001: Git authentication fails"
  ├─ "Error Pattern 002: SSH timeout"
  └─ "Error Pattern NNN: ..."

When you hit an error:
  → Check if it matches a pattern
  → Click link to skills/errors/001.md
  → Follow detailed solution
  
When you find NEW error:
  → Add to Skills.md digest
  → Create skills/errors/NNN.md
  → Next agent learns from your failure ✅
```

**Advantage**: Only digest is loaded by default. Load detailed solution only if needed.

### Layer 3: Memory (Memory.md) - Persistent State
**How it works:**
```
Memory.md tracks:
- ✅ Completed milestones
- 📍 Current phase
- 🎯 Next steps
- 💾 System state
- 📊 Progress timeline
- 🔍 Key decisions made
- 📝 Lessons learned

Agents read this to understand:
  "What phase are we in?"
  "What's already been done?"
  "What comes next?"
```

---

## 🎯 The Framework

Every agent:
1. **Read Agents.md** → understand framework
2. **Read Skills.md** → learn from past errors (digest only!)
3. **Read Memory.md** → understand current state
4. **Read order_[agent].md** → get step-by-step
5. **Read tasks/CURRENT_TASK.md** → understand task
6. **Read previous RESULT.md** → get context
7. **Execute** → generate/review/validate/test
8. **Output RESULT.md** → human-readable summary
9. **git push** → results on GitHub

---

## 👥 The Four Agents

### Codex 🔵 - Code Generator
- Generates code
- Uses Skills to avoid past mistakes
- Uses Memory for context
- Outputs: Code + RESULT.md

### Gemini 🟢 - Code Reviewer  
- Reviews code against specification
- Identifies risks
- Uses Skills to recognize patterns
- Outputs: Analysis + RESULT.md

### Claude 🔴 - Validator
- Validates all outputs
- Makes approval decision
- Uses Skills and Memory
- Outputs: Decision + RESULT.md

### Genspark 🟣 - QA Engineer
- Tests everything
- Confirms production readiness
- Uses all previous outputs
- Outputs: Test results + RESULT.md

---

## 📁 Repository Structure

```
virtual-company/
├── Agents.md              ← Framework (read first)
├── Skills.md              ← Error patterns + solutions (read digest)
├── Memory.md              ← Project state (read summary)
├── README.md              ← This file
├── order_*.md             ← Agent instructions (agent-specific)
├── tasks/
│   └── CURRENT_TASK.md    ← Your tasks here
├── results/
│   ├── codex/RESULT.md    ← What Codex did
│   ├── gemini/RESULT.md   ← What Gemini found
│   ├── claude/RESULT.md   ← What Claude approved
│   └── genspark/RESULT.md ← What tests passed
├── skills/
│   └── errors/
│       ├─ 001.md         ← Detailed solution (load if needed)
│       ├─ 002.md
│       └─ ...
└── changelog.md           ← Progress tracking
```

---

## 🔄 Typical Workflow

```
Morning: Write task
  tasks/CURRENT_TASK.md ← "Generate greeting function"

Afternoon: Kick agents
  1. Codex reads Skills.md (digest), Memory.md, order_codex.md
     → Generates code
     → Creates results/codex/RESULT.md
  
  2. Gemini reads Skills.md (digest), Memory.md, order_gemini.md
     → Reviews code
     → Creates results/gemini/RESULT.md
  
  3. Claude reads Skills.md (digest), Memory.md, order_claude.md
     → Validates both
     → Creates results/claude/RESULT.md
  
  4. Genspark reads Skills.md (digest), Memory.md, order_genspark.md
     → Tests everything
     → Creates results/genspark/RESULT.md

Evening: Review
  Read 4 RESULT.md files on GitHub
  Check Memory.md for next steps
  Done! 🎉
```

---

## ✅ What You Get

**Efficiency**:
- ✅ Fully automated (no copy-paste)
- ✅ One interface (GitHub)
- ✅ Complete history (changelog.md)
- ✅ Clear results (RESULT.md)
- ✅ Learn from failures (Skills.md)
- ✅ Remember progress (Memory.md)

**Learning**:
- ✅ Error patterns documented
- ✅ Solutions linked and available
- ✅ Next agent learns from your failure
- ✅ System gets smarter every task

**Memory**:
- ✅ Project state tracked
- ✅ Decisions documented
- ✅ Progress visible
- ✅ Context preserved

---

## 💾 Persistent Learning & Memory

### Skills.md Example

```markdown
### Error Pattern 001: Git Push Authentication Failure

**What**: fatal: Authentication failed

**Quick Fix**: Check SSH keys

**Details**: → skills/errors/001.md
```

When you get that error:
1. See it in Skills.md ✅
2. Click link to 001.md ✅
3. Follow solution ✅
4. No token waste on irrelevant details ✅

### Memory.md Example

```markdown
## ✅ Completed Milestones
- Framework created
- All agents configured
- Learning system added

## 🎯 Current Phase
Ready for first task

## 🚀 Next Steps
1. First real task
2. Document errors to Skills
3. Refine workflow
```

When you return after break:
1. Read Memory.md (5 minutes) ✅
2. Know what's been done ✅
3. Know what comes next ✅
4. All in one place ✅

---

## 🔐 Security

- All agents use safe git config
- .gitignore protects secrets
- SSH to Sakura server
- No hardcoded values

---

## 📚 Learn More

- **Complete framework**: Read `Agents.md`
- **Error patterns & solutions**: Read `Skills.md` (digest first!)
- **Project state & progress**: Read `Memory.md`
- **Agent instructions**: Read `order_*.md`
- **Track history**: Read `changelog.md`

---

## 🎯 Next Steps

1. **First time**: 
   - Read `Agents.md` (10 min)
   - Read `Skills.md` digest (2 min)
   - Read `Memory.md` (5 min)

2. **Create task**: 
   - Edit `tasks/CURRENT_TASK.md`

3. **Kick agents**: 
   - Run the 4 commands above

4. **Review**: 
   - Check GitHub `results/`
   - Update `Memory.md` with lessons

---

## 🚀 Philosophy

**"The system learns. The system remembers. The system improves."**

- Every error → documented in Skills
- Every decision → recorded in Memory
- Every success → repeated next time
- Every failure → prevented next time

---

**Status**: ✅ Production Ready with Persistent Learning & Memory  
**Version**: 2.0 (Added Skills & Memory systems)  
**Updated**: 2025-01-30  
**Repository**: https://github.com/garyohosu/virtual-company
