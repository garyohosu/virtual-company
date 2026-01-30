# Order - Implement MagicBoxAI Service

**Status**: ⏳ Waiting for implementation
**Current Actor**: codex
**Next Actor**: (complete when done)

---

## 🎯 Mission

Implement the MagicBoxAI service end-to-end.

MagicBoxAI is "a working note" for beginners: paste HTML → instant preview → auto-generates public URL + management URL → auto-deletes after 30 days.

---

## 📋 Tasks

### Phase 1: Requirements Confirmation

**Source**: https://github.com/garyohosu/magic-box-ai/blob/main/docs_public/requirements.md

**Task**:
1. Read magic-box-ai/docs_public/requirements.md
2. Confirm it is final v1.0 (no changes needed)
3. Create: magicboxai_requirements_confirmed.md
   - Confirm all MUST requirements are clear
   - Note any ambiguities
   - List the 4 core flows

**Output**: magicboxai_requirements_confirmed.md

---

### Phase 2: PoC Design

**Source**: https://github.com/garyohosu/magic-box-ai/blob/main/docs_public/poc_design.md

**Task**:
1. Read magic-box-ai/docs_public/poc_design.md
2. Align it with requirements.md
3. Create: magicboxai_poc_design_final.md
   - Database schema
   - API endpoints (minimal)
   - File storage strategy
   - 30-day auto-delete mechanism
   - iframe isolation design
   - 4 flows: paste → preview → save → view

**Output**: magicboxai_poc_design_final.md

---

### Phase 3: Implementation Plan

**Task**:
1. Break down into phases:
   - Phase 1: Backend (HTML storage, URL generation, auto-delete)
   - Phase 2: Frontend (paste UI, preview, save button)
   - Phase 3: Security (CSP, iframe, direct-access block)
   - Phase 4: Operations (reporting, moderation UI)

2. Create: magicboxai_implementation_plan.md
   - Estimate: lines of code per phase
   - Tech stack: (PHP? Python? Node?)
   - Database: (SQLite? PostgreSQL?)
   - Storage: (File system? Cloud?)
   - Testing strategy

3. Recommend starting with Phase 1+2 for MVP

**Output**: magicboxai_implementation_plan.md

---

### Phase 4: Create Virtual Company Integration

**Task**:
1. Design the business process for MagicBoxAI:
   - Sales: Customer support (email/chat)
   - Backend: Implementation + testing
   - QA: Security testing + moderation
   - Operations: Server management

2. Create: order_magicboxai_customer_support.md
   - Template for handling customer inquiries
   - Escalation flow
   - Response templates

3. Create: order_magicboxai_development.md
   - Template for implementing features
   - Testing checklist
   - Deploy process

**Output**: 
- order_magicboxai_customer_support.md
- order_magicboxai_development.md

---

## 🎯 Success Criteria

✅ magicboxai_requirements_confirmed.md created  
✅ magicboxai_poc_design_final.md created  
✅ magicboxai_implementation_plan.md created  
✅ order_magicboxai_customer_support.md created  
✅ order_magicboxai_development.md created  
✅ All files pushed to virtual-company repo  
✅ Cross-linked to garyohosu/magic-box-ai  

---

## 📂 Deliverables Location

All files in: https://github.com/garyohosu/virtual-company/

```
virtual-company/
├── magicboxai_requirements_confirmed.md
├── magicboxai_poc_design_final.md
├── magicboxai_implementation_plan.md
├── order_magicboxai_customer_support.md
├── order_magicboxai_development.md
└── ...
```

---

## 📝 Context

- MagicBoxAI repo: https://github.com/garyohosu/magic-box-ai
- Requirements: https://github.com/garyohosu/magic-box-ai/blob/main/docs_public/requirements.md
- PoC Design: https://github.com/garyohosu/magic-box-ai/blob/main/docs_public/poc_design.md

---

## ⏰ Timeline

Complete all by: Today

---

## 🔄 After Completion

Once done, you will:
1. `git pull` in virtual-company
2. `codex --kick order_magicboxai_development.md` to start development
3. Every feature/bug → new order.md → automated execution

This is the magic: one `codex --kick` runs everything.

---

**This is your experiment**: Can Codex actually build MagicBoxAI end-to-end?
