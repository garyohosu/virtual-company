# Agents.md - Virtual Company Complete Agent Framework

## 🎯 Core Philosophy: Fully Automated GitHub-Driven CI/CD

### The Vision

```
User kick (one command to CLI)
  ↓
Agent reads GitHub md file
  ↓
Agent understands complete workflow from Agents.md
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

## 📋 What Every Agent Must Do (Universal Pattern)

### When You Start (Same for All Agents)

1. **Read Agents.md** (this file)
   - Understand your role
   - Understand the complete workflow
   - Understand output requirements

2. **git pull** the repository
   - Keep local copy up-to-date
   - See what previous agents did

3. **Read tasks/CURRENT_TASK.md**
   - Understand what needs to be done
   - See specifications and requirements

4. **Read results from previous agents** (if any)
   - Understand what was already accomplished
   - Check for issues or notes
   - Plan your work based on their outputs

5. **Execute your specific task**
   - Follow your order_[agent].md file
   - Use RESULT.md output format

6. **Output three files:**
   - `RESULT.md` - Human-readable summary (⭐ this is what user reads)
   - `EXECUTION_LOG.md` - Technical details for debugging
   - `[output files]` - Your actual work

7. **Update changelog.md**
   - Record what you did
   - Note the status
   - Link to RESULT.md

8. **git commit & push**
   - All files to results/[agent-name]/
   - Clear, descriptive commit message
   - Always push to main

---

## 👥 The Four Agents & Their Roles

### 1️⃣ **Codex CLI** - Code Generator

**Role**: Generate code based on specifications

**Reads**:
- `tasks/CURRENT_TASK.md` - What to implement
- `Agents.md` - This file (your framework)
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
- `tasks/CURRENT_TASK.md` - Original specification
- `results/codex/RESULT.md` - What Codex generated
- `results/codex/EXECUTION_LOG.md` - Technical details
- `Agents.md` - This file
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
- `tasks/CURRENT_TASK.md` - Original specification
- `results/codex/RESULT.md` - Codex's output summary
- `results/gemini/RESULT.md` - Gemini's analysis summary
- `results/codex/EXECUTION_LOG.md` - Technical details
- `results/gemini/ANALYSIS.md` - Detailed analysis
- `Agents.md` - This file
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
- `tasks/CURRENT_TASK.md` - Original specification
- `results/codex/RESULT.md` - Codex summary
- `results/gemini/RESULT.md` - Gemini summary
- `results/claude/RESULT.md` - Claude summary
- All technical logs from previous agents
- `Agents.md` - This file
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
  Codex reads order_codex.md → understands specific instructions
  Codex reads tasks/CURRENT_TASK.md → understands specification
  Codex generates code → creates RESULT.md
  Codex pushes to GitHub
    ↓
  User: gemini "execute order_gemini.md"
    ↓
  Gemini reads Agents.md → understands framework
  Gemini reads order_gemini.md → understands specific instructions
  Gemini reads results/codex/RESULT.md → sees what Codex created
  Gemini analyzes code → creates RESULT.md
  Gemini pushes to GitHub
    ↓
  User: claude "execute order_claude.md"
    ↓
  Claude reads Agents.md → understands framework
  Claude reads order_claude.md → understands specific instructions
  Claude reads results/codex/RESULT.md + results/gemini/RESULT.md
  Claude validates → creates RESULT.md
  Claude pushes to GitHub
    ↓
  User: genspark (manual browser)
    ↓
  Genspark reads Agents.md → understands framework
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

- [ ] Read this Agents.md file
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

### After Execution

- [ ] Create RESULT.md (human-readable)
- [ ] Create EXECUTION_LOG.md (technical)
- [ ] Update changelog.md
- [ ] git add / commit / push
- [ ] Verify push was successful

### If Something Goes Wrong

- [ ] Document in EXECUTION_LOG.md
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

Possible future:
- GitHub Actions could kick agents automatically
- Discord bot could notify when tasks are complete
- Scheduled tasks could run at specific times

But for now: **User kicks → Agents read Agents.md → Everything else automatic**

---

## Final Note: You Are Self-Documenting

This Agents.md file IS your documentation. If an agent reads this file, they understand:
- The complete framework
- Their specific role
- How to output files
- How to integrate with other agents
- What success looks like

**Everything flows from this one file.**

---

**Last Updated**: 2025-01-30  
**Version**: 2.0 (Complete Self-Contained Framework)  
**Status**: ✅ Ready for Production  
**Maintained By**: Claude AI via GitHub MCP
