# Order for Codex CLI - Virtual Company

This file is read and executed by Codex CLI from GitHub.

## Execution Environment

**Server**: garyo.sakura.ne.jp  
**User**: garyo  
**Local**: Windows 11 (DOS/Command Prompt)  

---

## Execution Flow

### Step 1: SSH Login to Sakura Server

```bash
ssh garyo@garyo.sakura.ne.jp
```

### Step 2: Clone and Update Repository

```bash
cd ~

# First time only
git clone https://github.com/garyohosu/virtual-company.git

# Always
cd virtual-company
git pull origin main
```

### Step 3: Configure Git (First Time Only)

```bash
git config user.name "Codex CLI"
git config user.email "codex@virtualcompany.local"
```

### Step 4: Read Current Task

```bash
cat tasks/CURRENT_TASK.md
```

**Implement the complete specification from this file.**

### Step 5: Code Generation Requirements

- [ ] CURRENT_TASK.md fully understood
- [ ] All specifications identified
- [ ] Error handling implemented
- [ ] Input validation added
- [ ] Comments and documentation included
- [ ] Code follows standards (PEP 8 for Python, etc.)
- [ ] No hardcoded values

### Step 6: Create EXECUTION_LOG.md

```bash
mkdir -p results/codex

cat > results/codex/EXECUTION_LOG.md << 'EOF'
# Execution Log - Codex CLI

## Task: [from CURRENT_TASK.md]
**Date**: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Status**: SUCCESS

### Input Processing
- CURRENT_TASK.md read: ✅
- Task ID: [task-id]
- All requirements understood: ✅

### Execution Steps
1. Repository cloned/updated
2. Task specification analyzed
3. Code generated per specifications
4. Error handling implemented
5. Input validation added
6. Comments and documentation included

### Output Generated
- results/codex/[filename]
- results/codex/EXECUTION_LOG.md (this file)

### Validation
- [x] Output matches specifications
- [x] All files in correct location
- [x] Code quality verified
- [x] Ready for next agent

### Issues Encountered
None

### Next Steps
→ Gemini CLI for code review and analysis
EOF
```

### Step 7: Update changelog.md

```bash
cat >> changelog.md << 'EOF'

## [$(date +%Y-%m-%d)] - Codex CLI

**Task**: [from CURRENT_TASK.md]

**Changes**:
- Generated [filename] with full specifications
- Implemented error handling and validation
- Added comprehensive comments
- Code standards verified

**Files Modified**:
- results/codex/[filename] (NEW)
- results/codex/EXECUTION_LOG.md (NEW)

**Status**: COMPLETE

**Next Agent**: Gemini CLI

**Notes**:
- All specifications implemented
- Ready for analysis phase
EOF
```

### Step 8: Git Commit and Push

```bash
cd ~/virtual-company

# Verify status
git status

# Add files
git add results/codex/*
git add changelog.md

# Commit
git commit -m "Codex: [Task ID] - Code generation complete"

# Push
git push origin main
```

---

## Success Criteria

✅ Task specification fully understood  
✅ Code generated per requirements  
✅ Error handling implemented  
✅ Input validation present  
✅ Code standards followed  
✅ EXECUTION_LOG.md created  
✅ changelog.md updated  
✅ Files committed and pushed to GitHub  
✅ Next agent can proceed  

---

## Troubleshooting

### Git push fails
```bash
git pull origin main
git push origin main
```

### SSH connection issues
```bash
ssh -v garyo@garyo.sakura.ne.jp
```

### Git config not set
```bash
git config --global user.name "Codex CLI"
git config --global user.email "codex@virtualcompany.local"
```

---

**Last Updated**: 2025-01-30  
**Version**: 1.0
