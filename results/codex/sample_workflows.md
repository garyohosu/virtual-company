# Sample Workflows - Phase 1 Verification

## Sample 001: Simple Handoff

**Input File**: order_sample_001.md
**Run Command**: python kick_system.py --kick order_sample_001.md --no-git

### Expected Output
- Status updated to "Waiting for engineering_bob"
- Current Actor updated to "engineering_bob"
- Previous Actor inserted as "alice"
- Completed At inserted with current timestamp
- Order file preserved with instructions and deliverables

### Result Snapshot
- results/codex/order_sample_001_after.md

## Sample 002: Multi-Actor Workflow

**Input File**: order_sample_002.md
**Run Command**: python kick_system.py --kick order_sample_002.md --no-git

### Expected Output
- Status updated to "Waiting for engineering_bob"
- Current Actor updated to "engineering_bob"
- Previous Actor inserted as "sales_alice"
- Completed At inserted with current timestamp
- Pipeline section preserved

### Result Snapshot
- results/codex/order_sample_002_after.md

---

## Verification Checklist
- [x] Kick command updates Status and Current Actor
- [x] Previous Actor and Completed At fields added
- [x] Order body preserved after update
- [x] Context lookup prints WhoAmI/Memory/Skills/Inbox status
- [x] Error logging path available at results/codex/error.log
