# Skills.md - Virtual Company Learning System

## 🎯 Purpose

This file is a **digest** that agents read first to access collective knowledge.

- **No unnecessary details** - Just error patterns and where to find solutions
- **Efficient memory management** - Read digest, then load detailed solution if needed
- **Collective learning** - All agents learn from every mistake

---

## 📋 How to Use This File

### Agent Reading Pattern

**Every agent should read this file at the start**:

```
1. Open this file (Skills.md)
2. Read the digest section below
3. If you recognize your situation:
   - Look at the referenced skill file
   - Follow the solution
4. If you make a NEW error:
   - Document it in this file
   - Create detailed file in skills/errors/
   - Next agent learns from your failure
```

### When to Load Detailed Skill

```
You see: "Error Pattern 001: git push fails with authentication error"
You think: "Am I getting this error?"
If YES:
  - Read: skills/errors/001.md (detailed solution)
If NO:
  - Skip, continue with next pattern
```

**Result**: You only load what you need. Efficient memory use. ✅

---

## 📚 Error Pattern Digest

### Error Pattern 001: Git Push Authentication Failure

**What**: `fatal: Authentication failed for 'https://github.com/...`

**Quick Fix**: Check SSH keys or git credentials  
**Details**: → `skills/errors/001.md`

---

### Error Pattern 002: SSH Connection Timeout

**What**: `ssh: connect to host garyo.sakura.ne.jp port 22: Connection timed out`

**Quick Fix**: Verify SSH key is set up correctly  
**Details**: → `skills/errors/002.md`

---

### Error Pattern 003: Repository Already Exists

**What**: `fatal: destination path 'virtual-company' already exists`

**Quick Fix**: Use `git pull` instead of `git clone` if already cloned  
**Details**: → `skills/errors/003.md`

---

### Error Pattern 004: Missing git config

**What**: `fatal: name and email not configured`

**Quick Fix**: Run `git config user.name "[Agent Name]"` and `git config user.email "[agent]@virtualcompany.local"`  
**Details**: → `skills/errors/004.md`

---

### Error Pattern 005: RESULT.md Format Issues

**What**: Previous agent's RESULT.md is missing or empty

**Quick Fix**: Check that agent ran `cat > results/[agent]/RESULT.md << 'EOF'...` and `git push`  
**Details**: → `skills/errors/005.md`

---

## ⚠️ Adding New Skills

When you (any agent) encounter a NEW error:

### 1. Document in This File

Add to digest above:
```markdown
### Error Pattern NNN: [Descriptive Title]

**What**: [Exact error message]

**Quick Fix**: [1-sentence fix]  
**Details**: → `skills/errors/NNN.md`
```

### 2. Create Detailed Solution File

File: `skills/errors/NNN.md`

```markdown
# Error Pattern NNN - [Title]

## What Happened
[Description of the error]

## Why It Happened
[Root cause analysis]

## Prevention
[How to avoid this in the future]

## Solution Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Related Errors
- Error Pattern XXX (similar issue)
- Error Pattern YYY (related issue)

## References
- [Link if applicable]
```

### 3. Update changelog.md

Add:
```markdown
**Learning**: Documented Error Pattern NNN
**File**: skills/errors/NNN.md
```

### 4. Update this file in GitHub

The next agent will benefit from your learning. ✅

---

## 📊 Skill Statistics

| Pattern | Status | Last Seen | Frequency |
|---------|--------|-----------|-----------|
| 001 | Resolved | [Date] | [Count] |
| 002 | Resolved | [Date] | [Count] |
| 003 | Resolved | [Date] | [Count] |
| 004 | Resolved | [Date] | [Count] |
| 005 | Resolved | [Date] | [Count] |

---

## 🎯 Key Principle

**Fail once, learn forever.**

Every error becomes a skill. Every skill prevents future failures.

The system gets smarter with every task.

---

## 📍 Folder Structure

```
virtual-company/
├── Skills.md               ← You are here (digest)
├── Memory.md               ← Current progress
└── skills/
    ├── errors/
    │   ├─ 001.md          ← Detailed solution for pattern 001
    │   ├─ 002.md          ← Detailed solution for pattern 002
    │   └─ ...
    └── knowledge/
        ├─ architecture.md  ← System architecture notes
        ├─ lessons.md       ← Best practices learned
        └─ ...
```

---

**Last Updated**: 2025-01-30  
**Version**: 1.0  
**Status**: Ready for first task
