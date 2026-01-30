# Standard: Execution Logging Setup

**Important**: All Codex executions must capture BOTH stdout and stderr.

---

## 📋 For User

When executing any order, use this pattern:

```bash
# Standard Unix pipeline: capture everything
codex --kick order_*.md 2>&1 | tee results/codex/execution_$(date +%Y%m%d_%H%M%S).log

# Or shorter (overwrites):
codex --kick order_*.md 2>&1 | tee results/codex/execution.log
```

This ensures:
- ✅ stdout captured
- ✅ stderr captured  
- ✅ Displayed to terminal (tee)
- ✅ Saved to file for audit trail

---

## 📝 For Order Files

Every order should include this in "Post-Execution":

```
## Post-Execution

After Codex completes (success or error):

1. Check results/codex/execution.log
2. Review for warnings/errors
3. If NEEDS_FIX: address issues and re-run
4. If SUCCESS: proceed to next order

Command pattern:
$ codex --kick order_name.md 2>&1 | tee results/codex/execution.log
```

---

## 🔧 For Codex CLI

Codex should log all operations:

```
results/codex/
├── execution.log           ← All output (tee)
├── execution_20260130_001.log  ← Timestamped backup
├── RESULT.md              ← Summary
├── EXECUTION_LOG.md       ← Detailed log
└── errors/                ← Separate error archive
    ├── error_001.txt
    └── error_002.txt
```

---

## ✨ Why This Matters

```
Without logging:
  ❌ Error happens
  ❌ User sees it, forgets
  ❌ Can't reproduce

With logging:
  ✅ Error happens
  ✅ Captured in file
  ✅ Can review later
  ✅ Can debug with context
  ✅ Audit trail exists
```

---

## 🎯 Universal Rule

**All Codex executions = logged to file**

No exceptions.

This is the Unix philosophy: "pipe everything, save everything"

---

**Status**: Standard Practice (not an order, just a rule)
