# Order for Gemini CLI - Virtual Company

This file is read and executed by Gemini CLI from GitHub.

## Execution Environment

**Server**: garyo.sakura.ne.jp  
**User**: garyo  

---

## Execution Flow

### Step 1: SSH Login to Sakura Server

```bash
ssh garyo@garyo.sakura.ne.jp
```

### Step 2: Update Repository

```bash
cd ~/virtual-company
git pull origin main
```

### Step 3: Configure Git (First Time Only)

```bash
git config user.name "Gemini CLI"
git config user.email "gemini@virtualcompany.local"
```

### Step 4: Read Current Task

```bash
cat tasks/CURRENT_TASK.md
```

### Step 5: Review Codex's Output

```bash
cat results/codex/EXECUTION_LOG.md
cat results/codex/*.py  # or relevant file
```

### Step 6: Conduct Analysis

Analyze the following:

#### Specification Compliance
- [ ] All requirements from CURRENT_TASK.md implemented
- [ ] No extra features added without specification
- [ ] Edge cases considered
- [ ] Error cases handled

#### Code Quality
- [ ] Follows naming conventions
- [ ] Code is clear and readable
- [ ] Logic is correct
- [ ] Performance is acceptable

#### Risk Assessment
- [ ] Security issues identified
- [ ] Potential bugs logged
- [ ] Edge cases documented
- [ ] Scalability concerns noted

### Step 7: Create ANALYSIS.md

```bash
mkdir -p results/gemini

cat > results/gemini/ANALYSIS.md << 'EOF'
# Analysis Report - Gemini CLI

## Task: [from CURRENT_TASK.md]
**Date**: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Status**: COMPLETE

## Executive Summary
[1-2 sentence overview]

## Implementation Review

### Specification Compliance
**Overall**: 100% / 95% / [percentage]

Implemented Features:
- ✅ Feature 1
- ✅ Feature 2
- ⚠️ Feature 3 (partial)
- ❌ Feature 4 (missing)

### Code Quality Assessment

**Strengths**:
- [Strength 1]
- [Strength 2]

**Areas for Improvement**:
- [Area 1]: [Recommendation]
- [Area 2]: [Recommendation]

### Risk Assessment

**Critical Risks** (Must fix before production):
- [Risk 1]: [Impact and solution]

**Important Risks** (Should fix):
- [Risk 1]: [Recommendation]

**Minor Issues** (Nice to improve):
- [Issue 1]: [Suggestion]

## Security Analysis

- Input validation: ✅ / ⚠️ / ❌
- Error handling: ✅ / ⚠️ / ❌
- No hardcoded secrets: ✅ / ❌

## Recommendations

### Before Production
1. [Critical recommendation]

### Before Next Version
1. [Important recommendation]

### Future Enhancement
1. [Optional improvement]

## Conclusion

**Overall Assessment**: [Summary]

**Ready for Claude integration**: YES / NO
EOF
```

### Step 8: Create EXECUTION_LOG.md

```bash
cat > results/gemini/EXECUTION_LOG.md << 'EOF'
# Execution Log - Gemini CLI

## Task: [from CURRENT_TASK.md]
**Date**: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Status**: SUCCESS

### Input Processing
- CURRENT_TASK.md read: ✅
- Codex outputs reviewed: ✅

### Analysis Summary
- Specifications checked: 100%
- Risks identified: [Number]
- Recommendations provided: [Number]

### Output Files
- results/gemini/ANALYSIS.md (NEW)
- results/gemini/EXECUTION_LOG.md (this file)

### Next Steps
→ Claude Code for integration review
EOF
```

### Step 9: Update changelog.md

```bash
cat >> changelog.md << 'EOF'

## [$(date +%Y-%m-%d)] - Gemini CLI

**Task**: [from CURRENT_TASK.md]

**Changes**:
- Analyzed Codex implementation
- Identified [N] risks
- Provided [N] recommendations

**Files Modified**:
- results/gemini/ANALYSIS.md (NEW)
- results/gemini/EXECUTION_LOG.md (NEW)

**Status**: COMPLETE

**Next Agent**: Claude Code

**Key Findings**:
- [Finding 1]
- [Finding 2]
EOF
```

### Step 10: Git Commit and Push

```bash
cd ~/virtual-company

git add results/gemini/*
git add changelog.md
git commit -m "Gemini: [Task ID] - Analysis and recommendations complete"
git push origin main
```

---

## Success Criteria

✅ Task specification understood  
✅ Codex output thoroughly reviewed  
✅ ANALYSIS.md comprehensive and detailed  
✅ All risks identified and categorized  
✅ Recommendations are actionable  
✅ EXECUTION_LOG.md complete  
✅ changelog.md updated  
✅ Files committed and pushed  
✅ Claude Code can proceed  

---

## Quality Standards

- Evidence-based conclusions
- Specific recommendations (not vague)
- Risk severity clearly marked
- No false positives
- Professional tone

---

**Last Updated**: 2025-01-30  
**Version**: 1.0
