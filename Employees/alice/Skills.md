# Alice's Skills - Failure Patterns & Prevention

**Last Updated**: 2025-01-30  
**Total Patterns Learned**: 3

---

## 🔴 Pattern #1: SQL Injection Vulnerability

**Severity**: CRITICAL 🔴

### What Happened
Saw code using string concatenation in SQL queries instead of parameterized queries.

### When It Happens
- During code reviews of other teams
- When integrating with external systems
- In legacy code

### Why It's Dangerous
```sql
-- ❌ WRONG: String concatenation
query = "SELECT * FROM users WHERE id = " + user_id;
query = "SELECT * FROM users WHERE email = '" + email_input + "'";
-- Attacker can pass: 1' OR '1'='1
-- Query becomes: SELECT * FROM users WHERE email = '1' OR '1'='1'
-- Result: Returns ALL users!

-- ✅ CORRECT: Parameterized query
query = "SELECT * FROM users WHERE id = ?";
execute(query, [user_id]);
```

### Prevention Checklist
- [x] Always use parameterized queries
- [x] NEVER concatenate strings in SQL
- [x] Code review must check this
- [x] Use ORM frameworks (they handle it)
- [x] Educate team (already done)

### Reference
- [SQL Injection Prevention (OWASP)](https://owasp.org)
- Internal: Team training completed 2024-12-15

### Last Incident
- **Date**: 2024-12-15
- **Where**: Code review of Bob's migration script
- **Severity**: Medium (not yet deployed)
- **Resolution**: Corrected and re-reviewed
- **Status**: ✅ Resolved

### Team Awareness
✅ Alice: Expert  
✅ Bob: Aware (fixed his code)  
✅ Charlie: Needs training  
✅ Team: General awareness achieved  

---

## 🟡 Pattern #2: Connection Pool Undersizing

**Severity**: HIGH 🟡

### What Happened
System timeout under load because connection pool was too small.

### When It Happens
- Database under heavy concurrent load
- Holiday traffic spikes
- Multiple applications using same pool
- During load tests

### The Problem
```python
# Default pool size: 10 connections
pool = ConnectionPool(max_size=10)

# During peak load: 15+ concurrent queries
# 10 connections used up
# Query #11, #12, #13... waits indefinitely
# After 30 seconds: timeout error
# User impact: "Application is slow" or "Connection error"
```

### Prevention Checklist
- [ ] Calculate peak concurrent load (in progress)
- [ ] Set pool size = peak_load × 1.5
- [ ] Current: 10 → Target: 20 (estimated)
- [ ] Test under 2× peak load
- [ ] Monitor pool utilization in production
- [ ] Set alerts for pool exhaustion

### Calculation Example
```
2024 peak load: 8 concurrent queries (observed)
2025 expected: 12-15 concurrent queries
Buffer: × 1.5 = 15-22
Decision: Pool size = 20
```

### Last Incident
- **Date**: 2025-01-18
- **Symptom**: Timeouts during staging load test
- **Impact**: 3 requests failed
- **Root Cause**: Pool size 10 insufficient
- **Current Status**: 🟡 Fix in progress (awaiting approval)

### Action Plan
1. Get Manager_A1 approval
2. Update config (staging first)
3. Run load test (2× peak)
4. Monitor 1 week
5. Deploy to production
6. Update Pool monitoring

---

## 🆕 Pattern #3: Backup Monitoring Gap

**Severity**: HIGH 🔴 (just discovered)

### What Happened
Automated backup was running but failures went unnoticed.

### When It Happens
- Automated tasks (backups, cron jobs, batch processes)
- "Set it and forget it" operations
- No human monitoring

### The Problem
```
2025-01-20: Backup runs, succeeds
2025-01-21: Backup runs, fails silently
  └─ No one checks logs
  └─ No notification sent
  └─ No email alert
  └─ No Slack message

2025-01-30: Discovered by accident
  └─ 10 days of backup failures!
  └─ System unprotected
  └─ Big risk if disaster happens
```

### Why It's Dangerous
- Silent failures = no backup when needed
- Disaster recovery impossible
- Data loss = business impact
- Regulatory compliance risk

### Prevention Checklist
- [ ] Email notification on completion (success/failure)
- [ ] Slack alert on failure
- [ ] Weekly manual verification
- [ ] Log retention (30+ days)
- [ ] Backup integrity check (test restore)
- [ ] Dashboard showing last successful backup

### Implementation Plan
1. Add email notification to backup script
2. Set up Slack webhook for failures
3. Create weekly validation script
4. Document verification procedure

### First Detection
- **Date**: 2025-01-30 (today!)
- **Detection Method**: Manual log review
- **Time to Fix**: Estimated 3-4 hours
- **Priority**: CRITICAL (implement today)

### Status
🟡 Identified and prioritized  
⏳ Implementation starting today  
📝 Will document in Tech Blog post

---

## 📚 General Principles Learned

### Principle 1: "Secure by Default"
- Never trust user input
- Always assume data is untrusted
- Use parameterized queries by default
- **Application**: Pattern #1

### Principle 2: "Capacity Planning"
- Never use defaults for critical systems
- Calculate actual load
- Add buffer for growth/spikes
- **Application**: Pattern #2

### Principle 3: "Monitor Everything"
- Automated ≠ reliable
- Need visibility into automated tasks
- Failures should make noise
- **Application**: Pattern #3

---

## 🎯 Patterns by Category

### Security Patterns
- Pattern #1: SQL Injection

### Performance Patterns
- Pattern #2: Connection Pool Sizing

### Reliability Patterns
- Pattern #3: Monitoring Gaps

### To Be Discovered
- Pattern #4: (TBD)
- Pattern #5: (TBD)

---

## 📊 Pattern Statistics

| Pattern | Severity | Frequency | Status | Last Update |
|---------|----------|-----------|--------|-------------|
| #1 SQL Injection | CRITICAL | Rare | Resolved | 2024-12-15 |
| #2 Pool Sizing | HIGH | Monthly | In Progress | 2025-01-18 |
| #3 Monitoring | HIGH | New | Starting | 2025-01-30 |

---

## 🔍 How to Use These Patterns

### Before Writing Code
- Read Pattern #1 (SQL Injection)
- Check: Am I using parameterized queries?

### Before Deploying Database
- Read Pattern #2 (Connection Pool)
- Check: Did I calculate pool size correctly?

### Before Setting Up Automated Tasks
- Read Pattern #3 (Monitoring)
- Check: Will I know if this fails?

### When Troubleshooting
- Check relevant pattern
- Prevention checklist
- Last incident details

---

## 💡 Alice's Learning Note

> "I used to think 'good code' meant 'working code'.  
> But after these patterns, I know:  
> Good code = secure + fast + monitored.  
> All three matter."

---

**Repository**: https://github.com/garyohosu/virtual-company/Employees/alice/Skills.md  
**Next Review**: After Pattern #3 implementation (2025-02-01)
