# Skills - Error Patterns & Solutions

## 📌 How to Use This System

**Context Efficiency First**:
- Do NOT read all files every time
- Read DIGEST.md only when you start
- Use it as an INDEX to find specific information
- Load detailed files ONLY if you recognize a pattern

**When to Load Details**:
- You encounter an error that feels familiar
- You're about to try something
- You want to check if there's a known solution
- You need to avoid a known pitfall

---

## 🎯 Quick Digest (Read This First)

This page is your INDEX. Use it to find specific errors and solutions.

### Error Categories

| Category | Errors | Solutions |
|----------|--------|-----------|
| **Git** | #G001, #G002, #G003 | #SG001, #SG002, #SG003 |
| **GitHub** | #GH001, #GH002 | #SGH001, #SGH002 |
| **SSH/Server** | #S001, #S002 | #SS001, #SS002 |
| **Code Gen** | #C001, #C002 | #SC001, #SC002 |
| **Agent Communication** | #A001, #A002 | #SA001, #SA002 |
| **Environment** | #E001, #E002 | #SE001, #SE002 |

---

## 🔍 How to Find What You Need

### Scenario 1: "I'm getting a git error"
1. Look above for "Git" category
2. Find the error ID that matches
3. Read `Errors/git_G001.md` (if matching)
4. Read `Solutions/git_SG001.md` for fix

### Scenario 2: "I remember we had this issue before"
1. Think about the category (Git, SSH, etc.)
2. Search in that section
3. Load the relevant error file
4. Load the relevant solution file

### Scenario 3: "I'm about to do something, want to avoid mistakes"
1. Describe the action to yourself
2. Match it to a category
3. Skim the error descriptions
4. Load relevant error/solution pair

---

## 📂 File Structure

```
Skills/
├── DIGEST.md                    ← YOU ARE HERE (This file)
├── Errors/
│   ├── git_G001.md             ← Specific error details
│   ├── git_G002.md
│   ├── ssh_S001.md
│   └── ...
├── Solutions/
│   ├── git_SG001.md            ← How to fix
│   ├── git_SG002.md
│   └── ...
└── Index.md                     ← Complete index with descriptions
```

---

## 🔗 Links to Details

**When you see an error ID (#G001, #S001, etc.), use this to find the file**:

| ID | Error File | Solution File |
|----|-----------|----|
| #G001 | `Errors/git_G001.md` | `Solutions/git_SG001.md` |
| #G002 | `Errors/git_G002.md` | `Solutions/git_SG002.md` |
| #S001 | `Errors/ssh_S001.md` | `Solutions/ssh_SS001.md` |

---

## 📝 How to Add New Failures

When you encounter a new failure:

1. **Create error file**: `Errors/category_ID.md`
   - What went wrong
   - Why it happened
   - What error message appeared

2. **Create solution file**: `Solutions/category_SID.md`
   - How to fix it
   - Prevention tips
   - Related issues

3. **Update this DIGEST.md**
   - Add new row to table
   - Update category count

4. **git commit**: "skills: Add error #XXX and solution"

---

## 🎯 Philosophy

**"I don't need to remember everything. I just need to remember where to look."**

- DIGEST.md = Your memory INDEX
- Detailed files = Searchable knowledge base
- Use Index.md for detailed descriptions
- Reference from Agents.md when needed

---

## ✅ Next Steps

1. **When you start**: Skim this DIGEST.md
2. **When you encounter error**: Use table to find category/ID
3. **If ID matches your issue**: Read `Errors/[file].md`
4. **For solution**: Read `Solutions/[file].md`
5. **If you add new failure**: Add to DIGEST.md and create files

---

**Status**: System initialized, ready for failures to be recorded  
**Updated**: 2025-01-30  
**Philosophy**: Efficient, on-demand knowledge retrieval
