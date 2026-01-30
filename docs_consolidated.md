# Documentation Consolidation Index

## Purpose
This document consolidates the current documentation set, identifies duplicates, and defines a single source of truth for each topic.

## Single Source of Truth (Use These)
- **Framework & Workflow**: `Agents.md`
- **Project State**: `Memory.md`
- **Learning System**: `Skills.md` (primary)
- **Kick System**: `KickSystem.md` (overview), `kick_system.py` (implementation)
- **Execution Logging Standard**: `STANDARD_execution_logging.md`
- **Organization Structure**: `Organization.md`
- **Scale-free Architecture**: `ScaleFreeNetwork_Implementation.md`
- **MagicBoxAI Core Docs**: `magicboxai_requirements_confirmed.md`, `magicboxai_poc_design_final.md`, `magicboxai_implementation_plan.md`
- **Operational Orders**: `order_*.md` in repository root (current orders)
- **Tasks Queue**: `tasks/CURRENT_TASK.md`

## Duplicates / Derived Files (Reference Only)
- **Skills Digest Split**:
  - `Skills.md` is the official digest for agents.
  - `Skills/DIGEST.md` is a legacy/alternate digest and should be treated as secondary.
- **Generated Order Outputs**:
  - `results/codex/order_sample_001_after.md` and `results/codex/order_sample_002_after.md` are outputs; use `order_sample_001.md` and `order_sample_002.md` as sources.
- **Generated Kick System Copy**:
  - `results/codex/kick_system.py` is a snapshot; use `kick_system.py` as source.
- **Sample Results**:
  - Files under `results/codex/` are generated artifacts and should not replace source docs.

## Documentation Index (By Topic)

### Core Framework
- `Agents.md` ? universal workflow, roles, outputs
- `Skills.md` ? error patterns and fixes (primary digest)
- `Memory.md` ? project state and milestones
- `SYSTEM.md` ? system-level architecture overview

### Execution & Operations
- `KickSystem.md` ? kick system overview
- `kick_system.py` ? kick system implementation
- `CLIStartupGuide.md` ? CLI entry guidance
- `STANDARD_execution_logging.md` ? execution log format

### MagicBoxAI
- `magicboxai_requirements_confirmed.md` ? requirements baseline
- `magicboxai_poc_design_final.md` ? PoC design
- `magicboxai_implementation_plan.md` ? implementation plan
- `order_magicboxai_development.md` ? development order
- `order_magicboxai_sales.md` ? sales order

### Organization & Scale
- `Organization.md` ? org structure and policies
- `ScaleFreeNetwork_Implementation.md` ? scale-free network strategy
- `EmployeeSystem.md` ? employee processes
- `MailReadMarkerSystem.md` ? mail read marker specification

### Orders (Current & Historical)
- `order.md` ? customer integration pipeline (active example)
- `order_multiagent_p2p3.md` ? multi-agent execution order
- Other `order_*.md` ? phase/task-specific orders

### Employees (Per-Role Artifacts)
- `Employees/*/WhoAmI.md` ? role identity
- `Employees/*/Skills.md` ? role-specific skills
- `Employees/*/Memory.md` ? role-specific memory
- `Employees/*/Mail/inbox/*` ? role mail

### Results
- `results/**` ? generated outputs from agents (always treated as artifacts)

## Consolidation Recommendations
1. Treat `Skills.md` as the only primary skills digest; keep `Skills/DIGEST.md` as legacy.
2. Keep source files in repo root; treat `results/` as read-only outputs.
3. For each order, store the canonical file in root and only store outputs in `results/`.
4. Consider adding a short `docs/README.md` in the future to centralize this index.

## Change Log
- 2026-01-30: Created consolidated index and clarified sources of truth.
