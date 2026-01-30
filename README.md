# Virtual Company - AI Agent Automation Framework

## 🚀 What is Virtual Company?

Virtual Company is a **fully automated CI/CD system** where 4 AI CLI agents (Codex, Gemini, Claude, Genspark) work together to automate software development tasks.

**Simple formula**:
```
You write task → Agents read GitHub → Agents execute automatically → Results on GitHub
```

---

## ⚡ How to Use (30 seconds)

### 1. Create Task
```bash
# Edit with Claude.ai
tasks/CURRENT_TASK.md
# Describe what needs to be done
```

### 2. Kick Agents (4 commands, takes 1 minute each)
```bash
cd ~/virtual-company && git pull

# Agent 1: Generate code
codex "git pull して order_codex.md を実行してください"

# Agent 2: Review code
gemini "git pull して order_gemini.md を実行してください"

# Agent 3: Validate & approve
claude "git pull して order_claude.md を実行してください"

# Agent 4: Test & confirm
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

| File | Read When | Why |
|------|-----------|-----|
| **Agents.md** | 🔵 FIRST TIME | Understand complete framework |
| **order_codex.md** | Code gen needed | Step-by-step for Codex |
| **order_gemini.md** | Code review | Step-by-step for Gemini |
| **order_claude.md** | Validation | Step-by-step for Claude |
| **order_genspark.md** | Testing | Step-by-step for Genspark |
| **README.md** | Quick reference | This file |

---

## 🎯 The Framework (Read Agents.md for Details)

Every agent:
1. Reads Agents.md → understands the framework
2. git pull → gets latest
3. Reads tasks/CURRENT_TASK.md → understands what to do
4. Reads previous agents' RESULT.md → understands context
5. **Does their work** (generate / analyze / validate / test)
6. Creates RESULT.md (human-readable) + technical logs
7. Updates changelog.md
8. git push → results on GitHub

---

## 👥 The Four Agents

### Codex 🔵 - Code Generator
- Generates code matching specification
- Outputs: Code + RESULT.md

### Gemini 🟢 - Code Reviewer  
- Reviews code, identifies risks
- Outputs: Analysis + RESULT.md

### Claude 🔴 - Validator & Orchestrator
- Validates all outputs, makes approval decision
- Outputs: Decision + RESULT.md

### Genspark 🟣 - QA Engineer
- Tests everything, confirms production readiness
- Outputs: Test results + RESULT.md

---

## 📁 Repository Structure

```
virtual-company/
├── Agents.md              ← 🎯 Master reference
├── order_codex.md         ← Codex reads this
├── order_gemini.md        ← Gemini reads this
├── order_claude.md        ← Claude reads this
├── order_genspark.md      ← Genspark reads this
├── tasks/
│   └── CURRENT_TASK.md    ← You write tasks here
├── results/
│   ├── codex/RESULT.md
│   ├── gemini/RESULT.md
│   ├── claude/RESULT.md
│   └── genspark/RESULT.md
├── changelog.md           ← Progress tracking
└── .gitignore
```

---

## 🔄 Typical Workflow Example

```
Morning: Write task
  tasks/CURRENT_TASK.md ← "Generate greeting function in Python"

Afternoon: Kick agents
  1. codex "execute"
     → Creates results/codex/RESULT.md ✅
  
  2. gemini "execute"
     → Creates results/gemini/RESULT.md ✅
  
  3. claude "execute"
     → Creates results/claude/RESULT.md ✅
  
  4. genspark
     → Creates results/genspark/RESULT.md ✅

Evening: Review
  You read 4 RESULT.md files on GitHub
  Everything's done! 🎉
```

---

## ✅ What You Get

**Before Virtual Company**:
- Manual copy-paste between ChatGPT and local files
- Lost context between tools
- Errors from miscommunication
- Hard to track what was done

**With Virtual Company**:
- ✅ Fully automated
- ✅ One interface (GitHub)
- ✅ Complete history (changelog.md)
- ✅ Clear results (RESULT.md)
- ✅ No manual work after kickoff

---

## 🔐 Security

- All agents use safe git config
- .gitignore protects secrets
- SSH to Sakura server (garyo@garyo.sakura.ne.jp)
- No hardcoded values allowed

---

## 📚 Learn More

- **Complete framework**: Read `Agents.md`
- **Agent instructions**: Read `order_*.md`
- **Track progress**: Read `changelog.md`
- **See results**: Read `results/*/RESULT.md`

---

## 🎯 Next Steps

1. **First time**: Read `Agents.md` (10 minutes)
2. **Create task**: Edit `tasks/CURRENT_TASK.md`
3. **Kick agents**: Run the 4 commands above
4. **Review**: Check GitHub `results/` folder

---

**Status**: ✅ Production Ready  
**Updated**: 2025-01-30  
**Repository**: https://github.com/garyohosu/virtual-company
