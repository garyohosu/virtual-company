# Order - Implement Kick System

**Status**: ⏳ Waiting for implementation
**Current Actor**: codex
**Next Actor**: (complete when done)

---

## 🎯 Mission

Implement the Kick System CLI for Virtual Company.

This will enable: `codex --kick order.md`

---

## 📋 Core Requirements

### 1. Parse order.md
Read and extract:
- `**Current Actor**:` (who runs now)
- `**Next Actor**:` (who runs after)
- Instructions (everything else)

### 2. Load Employee Context
From `Employees/{current_actor}/` directory:
```
- WhoAmI.md           (who they are)
- Memory.md           (what they remember)
- Skills.md           (what they learned)
- Mail/inbox/         (any messages)
```

### 3. Display Summary
```
👤 {Name} ({Role}) is executing...
📋 Instructions:
   [show order.md instructions]
```

### 4. Update order.md
After execution:
```
**Status**: ⏳ Waiting for {next_actor}
**Current Actor**: {next_actor}
**Previous Actor**: {current_actor}
**Completed At**: {timestamp}
```

### 5. Git Operations
```bash
git add .
git commit -m "chore: Kick - {current_actor} executed"
git push
```

---

## 💾 Implementation Details

### Language
- Python / Go / Rust (your choice)

### File
Create: `kick_system.py` (or equivalent)

### CLI Usage
```bash
python kick_system.py --kick order.md
```

Or integrated with codex:
```bash
codex --kick order.md
```

### Test Case

Before:
```
order.md:
  Current Actor: sales_alice
  Next Actor: engineering_bob
```

After `codex --kick order.md`:
```
order.md:
  Current Actor: engineering_bob
  Next Actor: manufacturing_eve
  Completed: sales_alice at 2025-01-30 15:00
```

---

## 🧪 Success Criteria

✅ Reads order.md from GitHub  
✅ Finds current_actor: sales_alice  
✅ Loads Employees/sales_alice/ context  
✅ Shows employee summary  
✅ Updates order.md: Current → Next  
✅ Commits and pushes to GitHub  
✅ Command works: `codex --kick order.md`

---

## Timeline

Complete by: Today

---

## Notes

This is the core system for Virtual Company.
Once working, all workflows run via: `codex --kick order.md`

No other commands needed.
