# Order for Claude Code - Virtual Company

This file is read and executed by Claude Code.

## Your Role: VP of Engineering & Orchestrator

You are responsible for:
1. Validating all agent outputs
2. Making integration decisions
3. Orchestrating via MCP if needed
4. Approving or requesting revisions

---

## Execution Flow

### Step 1: SSH Login to Sakura Server

```bash
ssh garyo@garyo.sakura.ne.jp
cd ~/virtual-company
git pull origin main
```

### Step 2: Read Task and Review Outputs

```bash
cat tasks/CURRENT_TASK.md
cat results/codex/EXECUTION_LOG.md
cat results/gemini/ANALYSIS.md
cat results/codex/*.py  # or relevant file
```

### Step 3: Validate Codex Output

Code Quality Checklist:
- [ ] Syntax is correct
- [ ] Follows naming conventions
- [ ] Has proper error handling
- [ ] Is well-documented
- [ ] No security issues
- [ ] Performance is acceptable
- [ ] Meets all specifications

### Step 4: Validate Gemini Output

Analysis Quality Checklist:
- [ ] Conclusions are evidence-based
- [ ] Risks are accurately identified
- [ ] Recommendations are actionable
- [ ] Nothing is overlooked
- [ ] Professional tone

### Step 5: Create INTEGRATION_SUMMARY.md

```bash
mkdir -p results/claude

cat > results/claude/INTEGRATION_SUMMARY.md << 'EOF'
# Integration Summary - Claude Code

## Overall Assessment

### Executive Summary
[1-2 sentences on what was accomplished]

### Quality Metrics
- Code Quality: Excellent / Good / Acceptable / Poor
- Analysis Quality: Excellent / Good / Acceptable / Poor
- Specification Compliance: 100% / 95% / [percentage]

## Codex Code Review

### Assessment
[Your evaluation]

### Strengths
- [Strength 1]
- [Strength 2]

### Issues Found
- [Issue 1] → Recommendation
- [Issue 2] → Recommendation

## Gemini Analysis Review

### Assessment
[Your evaluation]

### Validation
- Risk identification: Accurate / Partial / Missed items
- Recommendations: Actionable / Needs refinement

## Final Decision

**Status**: APPROVED / APPROVED WITH NOTES / NEEDS REVISION

**Confidence Level**: High / Medium / Low

**Date**: $(date -u +"%Y-%m-%dT%H:%M:%SZ")

### Before Genspark QA
- [ ] Issue 1 must be resolved
- [ ] Issue 2 should be addressed
- [ ] All critical items cleared

EOF
```

### Step 6: Create EXECUTION_LOG.md

```bash
cat > results/claude/EXECUTION_LOG.md << 'EOF'
# Execution Log - Claude Code

## Task: [from CURRENT_TASK.md]
**Date**: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Status**: VALIDATION_COMPLETE

### Validation Results
- Codex output: ✅ Reviewed
- Gemini output: ✅ Reviewed
- Specification compliance: [Percentage]

### Decision
APPROVED / NEEDS_REVISION

### Next Steps
→ Genspark for final QA and testing
EOF
```

### Step 7: Update changelog.md

```bash
cat >> changelog.md << 'EOF'

## [$(date +%Y-%m-%d)] - Claude Code

**Task**: [from CURRENT_TASK.md]

**Validation Results**:
- Code quality: [Assessment]
- Analysis quality: [Assessment]
- Compliance: [Percentage]

**Decision**: APPROVED / NEEDS_REVISION

**Next Agent**: Genspark

**Notes**:
- [Key decision point]
EOF
```

### Step 8: Git Commit and Push

```bash
cd ~/virtual-company

git add results/claude/*
git add changelog.md
git commit -m "Claude: [Task ID] - Integration and validation complete"
git push origin main
```

---

## Success Criteria

✅ All outputs reviewed and validated  
✅ Quality standards verified  
✅ INTEGRATION_SUMMARY.md created  
✅ Clear approval or revision decision  
✅ EXECUTION_LOG.md complete  
✅ changelog.md updated  
✅ Files committed and pushed  
✅ Genspark can proceed  

---

## Decision Framework

**APPROVED**: All requirements met, quality excellent, no issues

**APPROVED WITH NOTES**: Requirements met, minor issues noted, proceed to Genspark

**NEEDS REVISION**: Issues found that must be fixed before Genspark, send back to Codex/Gemini

---

**Last Updated**: 2025-01-30  
**Version**: 1.0
