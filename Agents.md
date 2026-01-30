# Agents.md - Virtual Company Complete Agent Framework

## 🎯 Core Philosophy: Fully Automated GitHub-Driven CI/CD

### The Vision

```
User kick (one command to CLI)
  ↓
Agent reads GitHub md files
  ↓
Agent understands complete workflow from reading:
  1. Agents.md (framework)
  2. Skills.md (learned from past errors)
  3. Memory.md (current project state)
  4. order_[agent].md (specific instructions)
  5. tasks/CURRENT_TASK.md (specification)
  6. Previous agents' RESULT.md (context)
  ↓
Agent executes automatically on Sakura server
  ↓
Agent outputs RESULT.md (human-readable) + technical logs
  ↓
Agent commits & pushes to GitHub
  ↓
User sees results on GitHub

Zero manual intervention after the kick.
```

---

## 📖 Essential Files You Must Read (In This Order)

### Every Agent Should Read These BEFORE Starting Any Task

1. **Agents.md** (This file)
   - Your role
   - Universal workflow
   - Output requirements

2. **Skills.md**
   - Past error patterns (digest)
   - How to avoid known mistakes
   - Link to detailed solutions if needed
   - URL: https://raw.githubusercontent.com/garyohosu/virtual-company/main/Skills.md

3. **Memory.md**
   - Current project phase
   - What's been completed
   - Current system state
   - Next steps
   - URL: https://raw.githubusercontent.com/garyohosu/virtual-company/main/Memory.md

4. **Your order_[agent].md**
   - Step-by-step instructions specific to you

5. **tasks/CURRENT_TASK.md**
   - What needs to be done

6. **Previous agents' RESULT.md files**
   - What they accomplished
   - What issues they found

---

## 💾 Persistent Learning System

### Skills.md - Learn From Past Errors

**What it contains**:
- Digest of error patterns with solutions
- Example: "Error Pattern 001: Git Push Authentication Failure"
- Links to detailed solutions in `skills/errors/`

**How to use**:
1. Read the digest (2 minutes)
2. If you recognize your situation → click link to detailed solution
3. If you encounter NEW error → add to Skills.md and create details file

**Why efficient**:
- You only read digest (small)
- Load detailed solution only if needed
- No token waste on unnecessary details

### Memory.md - Remember Where We Are

**What it contains**:
- Current project phase
- Completed milestones
- System state
- Key decisions made
- Lessons learned
- Next tasks

**How to use**:
1. Read at start to understand context
2. Know what's been done
3. Know what comes next
4. Understand why decisions were made

**Why important**:
- Agents understand context
- User remembers progress
- System has persistent memory

---

## 📋 What Every Agent Must Do (Universal Pattern)

### When You Start (Same for All Agents)

1. **Read Agents.md** (this file)
   - Understand your role
   - Understand the complete workflow
   - Understand output requirements

2. **Read Skills.md** (persistent learning)
   - Learn from past errors
   - Avoid known pitfalls
   - Load detailed solutions if you hit error patterns

3. **Read Memory.md** (persistent memory)
   - Understand current project phase
   - Know what's been completed
   - Know what comes next
   - Understand why we made decisions

4. **git pull** the repository
   - Keep local copy up-to-date
   - See what previous agents did

5. **Read tasks/CURRENT_TASK.md**
   - Understand what needs to be done
   - See specifications and requirements

6. **Read results from previous agents** (if any)
   - Understand what was already accomplished
   - Check for issues or notes
   - Plan your work based on their outputs

7. **Execute your specific task**
   - Follow your order_[agent].md file
   - Use Skills.md to avoid known errors
   - Use RESULT.md output format

8. **Output three files:**
   - `RESULT.md` - Human-readable summary (⭐ this is what user reads)
   - `EXECUTION_LOG.md` - Technical details for debugging
   - `[output files]` - Your actual work

9. **Update changelog.md**
   - Record what you did
   - Note the status
   - Link to RESULT.md

10. **git commit & push**
    - All files to results/[agent-name]/
    - Clear, descriptive commit message
    - Always push to main

---

## 👥 The Four Agents & Their Roles

### 1️⃣ **Codex CLI** - Code Generator

**Role**: Generate code based on specifications

**Reads**:
- `Agents.md` - Framework
- `Skills.md` - Past errors (check for generation issues)
- `Memory.md` - Current state
- `tasks/CURRENT_TASK.md` - What to implement
- `order_codex.md` - Your specific instructions

**Does**:
- Implement the exact specification
- Add error handling
- Add input validation
- Add documentation
- Follow code standards

**Outputs**:
- `results/codex/[code_file]` - The generated code
- `results/codex/RESULT.md` - "Here's what I generated"
- `results/codex/EXECUTION_LOG.md` - Technical log
- `changelog.md` - Updated with your work

**Next**: Gemini reads your RESULT.md

---

### 2️⃣ **Gemini CLI** - Code Reviewer & Analyzer

**Role**: Review code and identify risks

**Reads**:
- `Agents.md` - Framework
- `Skills.md` - Past analysis patterns
- `Memory.md` - Current state
- `tasks/CURRENT_TASK.md` - Original specification
- `results/codex/RESULT.md` - What Codex generated
- `results/codex/EXECUTION_LOG.md` - Technical details
- `order_gemini.md` - Your specific instructions

**Does**:
- Verify Codex's code matches specification
- Identify security risks
- Identify performance issues
- Identify edge cases
- Provide specific, actionable recommendations

**Outputs**:
- `results/gemini/RESULT.md` - "Here's what I found"
- `results/gemini/ANALYSIS.md` - Detailed findings
- `results/gemini/EXECUTION_LOG.md` - Technical log
- `changelog.md` - Updated with your analysis

**Next**: Claude reads your RESULT.md

---

### 3️⃣ **Claude Code** - Orchestrator & Validator

**Role**: Validate all outputs and make integration decisions

**Reads**:
- `Agents.md` - Framework
- `Skills.md` - Past validation patterns
- `Memory.md` - Current state
- `tasks/CURRENT_TASK.md` - Original specification
- `results/codex/RESULT.md` - Codex's output summary
- `results/gemini/RESULT.md` - Gemini's analysis summary
- `results/codex/EXECUTION_LOG.md` - Technical details
- `results/gemini/ANALYSIS.md` - Detailed analysis
- `order_claude.md` - Your specific instructions

**Does**:
- Validate Codex's code quality
- Validate Gemini's analysis quality
- Make decision: APPROVED / APPROVED WITH NOTES / NEEDS REVISION
- Document validation results

**Outputs**:
- `results/claude/RESULT.md` - "Here's my validation"
- `results/claude/INTEGRATION_SUMMARY.md` - Validation details
- `results/claude/EXECUTION_LOG.md` - Technical log
- `changelog.md` - Updated with your decision

**Next**: Genspark reads your RESULT.md

---

### 4️⃣ **Genspark** - QA Engineer & Final Validator

**Role**: Test everything and confirm production readiness

**Reads**:
- `Agents.md` - Framework
- `Skills.md` - Past testing patterns
- `Memory.md` - Current state
- `tasks/CURRENT_TASK.md` - Original specification
- `results/codex/RESULT.md` - Codex summary
- `results/gemini/RESULT.md` - Gemini summary
- `results/claude/RESULT.md` - Claude summary
- All technical logs from previous agents
- `order_genspark.md` - Your specific instructions

**Does**:
- Test all code execution
- Test integration
- Test edge cases
- Verify performance
- Confirm production readiness

**Outputs**:
- `results/genspark/RESULT.md` - "Here are test results"
- `results/genspark/TESTING_REPORT.md` - Detailed test results
- `results/genspark/EXECUTION_LOG.md` - Technical log
- `changelog.md` - Updated with test results

**Final**: Task complete, user reviews on GitHub

---

## 📝 Output Files Structure

### RESULT.md (What User Reads) ⭐

**Purpose**: Human-readable summary that takes 1 minute to read

**Format**:
```markdown
# ✅ [Agent Name] Execution Result

**Task**: [Task name]
**Date**: [ISO timestamp]
**Status**: ✅ SUCCESS / ⚠️ PARTIAL / ❌ BLOCKED

## Summary
[1-2 sentences of what was done]

## What Was Accomplished
- ✅ Item 1
- ✅ Item 2
- ⚠️ Issue 1

## Key Metrics
- Quality: [Assessment]
- Compliance: [Percentage]%
- Issues: [Count]

## Next Steps
👉 [Next agent name] will now...

---
**Generated by**: [Agent Name]
**Repository**: https://github.com/garyohosu/virtual-company
```

### EXECUTION_LOG.md (Technical Details)

**Purpose**: Full technical log for debugging

**Contains**:
- Input processing steps
- Execution steps taken
- Issues encountered
- Validation results
- Files created
- Timestamps

### changelog.md (Progress Tracking)

**Format**:
```markdown
## [YYYY-MM-DD] - [Agent Name]

**Task**: [Task ID]
**Changes**: [What was done]
**Status**: COMPLETE / PARTIAL / BLOCKED
**📖 View Result**: `results/[agent]/RESULT.md`
**Next Agent**: [Next agent name]
```

---

## 🔄 Sequential Workflow Example

```
Morning:
  User creates/edits tasks/CURRENT_TASK.md via Claude.ai
  User pushes to GitHub

Afternoon (User kicks agents one by one):

  User: codex "execute order_codex.md"
    ↓
  Codex reads Agents.md → understands framework
  Codex reads Skills.md → learns from past
  Codex reads Memory.md → understands state
  Codex reads order_codex.md → understands specific instructions
  Codex reads tasks/CURRENT_TASK.md → understands specification
  Codex generates code → creates RESULT.md
  Codex pushes to GitHub
    ↓
  User: gemini "execute order_gemini.md"
    ↓
  Gemini reads Agents.md → understands framework
  Gemini reads Skills.md → learns from past
  Gemini reads Memory.md → understands state
  Gemini reads order_gemini.md → understands specific instructions
  Gemini reads results/codex/RESULT.md → sees what Codex created
  Gemini analyzes code → creates RESULT.md
  Gemini pushes to GitHub
    ↓
  User: claude "execute order_claude.md"
    ↓
  Claude reads Agents.md → understands framework
  Claude reads Skills.md → learns from past
  Claude reads Memory.md → understands state
  Claude reads order_claude.md → understands specific instructions
  Claude reads results/codex/RESULT.md + results/gemini/RESULT.md
  Claude validates → creates RESULT.md
  Claude pushes to GitHub
    ↓
  User: genspark (manual browser)
    ↓
  Genspark reads Agents.md → understands framework
  Genspark reads Skills.md → learns from past
  Genspark reads Memory.md → understands state
  Genspark reads order_genspark.md → understands specific instructions
  Genspark reads all previous RESULT.md files
  Genspark tests → creates RESULT.md
  Genspark pushes to GitHub

Evening:
  User opens GitHub
  User reads:
    1. results/codex/RESULT.md
    2. results/gemini/RESULT.md
    3. results/claude/RESULT.md
    4. results/genspark/RESULT.md
  Done! 🎉
```

---

## ✅ Universal Requirements for All Agents

### Before You Start

- [ ] Read Agents.md (this file) - 10 minutes
- [ ] Read Skills.md - 5 minutes (digest only)
- [ ] Read Memory.md - 5 minutes
- [ ] Understand your role above
- [ ] Know what RESULT.md must contain
- [ ] Know you must git push at the end
- [ ] Have SSH access to Sakura server ready

### During Execution

- [ ] Follow your specific order_[agent].md completely
- [ ] Read all previous agents' RESULT.md files
- [ ] Handle all edge cases
- [ ] Implement error handling
- [ ] Document thoroughly
- [ ] Validate before finishing
- [ ] If error occurs and it's in Skills.md, load detailed solution

### After Execution

- [ ] Create RESULT.md (human-readable)
- [ ] Create EXECUTION_LOG.md (technical)
- [ ] Update changelog.md
- [ ] git add / commit / push
- [ ] Verify push was successful

### If Something Goes Wrong

- [ ] Check Skills.md for similar error pattern
- [ ] If found, load detailed solution file
- [ ] If new error, document it
- [ ] Update Skills.md with new pattern
- [ ] Mark status as PARTIAL or BLOCKED
- [ ] Still push (so humans can see what happened)
- [ ] Don't stop the pipeline

---

## 🔐 Security & Git Rules

### Git Configuration

All agents must set:
```bash
git config user.name "[Agent Name]"
git config user.email "[agent]@virtualcompany.local"
```

### Commits

- **Format**: `[Agent]: [Task ID] - [What was done]`
- **Example**: `Codex: TASK-001 - Code generation complete`

### .gitignore Protection

Never commit:
- .env files
- API tokens
- Passwords
- Private keys
- Hardcoded secrets

---

## 📊 Repository Structure

```
virtual-company/
├── Agents.md                    ← This file (framework for all agents)
├── Skills.md                    ← Persistent learning (error patterns)
├── Memory.md                    ← Persistent memory (project state)
├── README.md                    ← Quick reference
├── tasks/
│   └── CURRENT_TASK.md          ← User puts task here
├── results/
│   ├── codex/
│   │   ├── RESULT.md            ← Codex summary (human reads)
│   │   ├── EXECUTION_LOG.md     ← Technical details
│   │   └── [generated files]
│   ├── gemini/
│   │   ├── RESULT.md            ← Gemini summary
│   │   ├── ANALYSIS.md          ← Detailed analysis
│   │   └── EXECUTION_LOG.md
│   ├── claude/
│   │   ├── RESULT.md            ← Claude summary
│   │   ├── INTEGRATION_SUMMARY.md
│   │   └── EXECUTION_LOG.md
│   └── genspark/
│       ├── RESULT.md            ← Genspark summary
│       ├── TESTING_REPORT.md
│       └── EXECUTION_LOG.md
├── skills/
│   └── errors/                  ← Detailed error solutions
│       ├── 001.md
│       ├── 002.md
│       └── ...
├── order_codex.md               ← Codex reads this
├── order_gemini.md              ← Gemini reads this
├── order_claude.md              ← Claude reads this
├── order_genspark.md            ← Genspark reads this
├── changelog.md                 ← All agents update this
└── .gitignore                   ← Security rules
```

---

## 🎯 Success Criteria for a Complete Task

A task is **100% COMPLETE** when:

```
✅ CURRENT_TASK.md is understood
✅ Codex generates code with RESULT.md
✅ Gemini analyzes code with RESULT.md
✅ Claude validates with RESULT.md
✅ Genspark tests with RESULT.md
✅ All RESULT.md files are human-readable
✅ All changes are committed and pushed
✅ changelog.md is updated
✅ User can review results/*/RESULT.md files
✅ No manual copy-paste needed
✅ Learning captured in Skills.md (if error occurred)
✅ Memory.md updated with lessons
```

---

## 🔧 Environment Details

- **Sakura Server**: garyo.sakura.ne.jp
- **Username**: garyo
- **Repository**: https://github.com/garyohosu/virtual-company
- **Local Setup**: Windows 11 (DOS/cmd), optionally WSL2
- **All agents**: Read from GitHub, execute on Sakura, push results

---

## 📞 Communication Between Agents

Agents communicate through:

1. **RESULT.md** (what they accomplished, in plain language)
2. **EXECUTION_LOG.md** (detailed technical info if needed)
3. **changelog.md** (timeline of what happened)

**No direct API calls needed.** Just read GitHub files.

---

## 🚀 The Future: Even More Automation

Currently:
- User kicks each agent manually (4 commands)
- System learns from failures
- Memory tracks progress

Possible future:
- GitHub Actions could kick agents automatically
- Discord bot could notify when tasks are complete
- Scheduled tasks could run at specific times
- Skill patterns could be auto-suggested

But for now: **User kicks → Agents read (Agents.md/Skills.md/Memory.md) → Everything else automatic**

---

## Final Note: You Are Self-Documenting

This Agents.md file IS your documentation. If an agent reads this file, they understand:
- The complete framework
- Their specific role
- How to output files
- How to integrate with other agents
- Where to find persistent learning (Skills.md)
- Where to find persistent memory (Memory.md)
- What success looks like

**Everything flows from this one file + Skills.md + Memory.md.**

---

**Last Updated**: 2025-01-30  
**Version**: 2.1 (Added Skills.md and Memory.md references)  
**Status**: ✅ Ready for Production with Persistent Learning  
**Maintained By**: Claude AI via GitHub MCP
