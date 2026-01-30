# Security Checklist

## Input Validation
- [x] Order file must be inside repository
- [x] Order file extension restricted to `.md`
- [x] File size limits enforced
- [x] Actor name validated against allowed pattern
- [x] Missing required fields raise errors

## Rate Limiting
- [x] Per-actor rate limit enforced (default 60s)
- [x] Rate limit state stored in `results/codex/rate_limit.json`
- [x] Manual override available via `--no-rate-limit`
- [ ] Premium bypass (not applicable to CLI)

## Audit Logging
- [x] Kick start logged
- [x] Order update logged
- [x] Git push or skip logged
- [x] Failures logged
- [x] Logs append-only (`results/codex/audit.log`)

## Access Control
- [x] Order file path constrained to repo
- [x] Actor names constrained to safe pattern
- [ ] Management URL separation (not applicable to CLI)
- [ ] User auth/permissions (not applicable to CLI)

## Data Protection
- [ ] Encryption at rest (out of scope for CLI)
- [x] Error logs avoid secrets
- [ ] Immutable storage (future)

## Notes
- Focused on CLI safety controls; web/API-specific items are marked as N/A.
- Recommended next step: centralize audit log rotation and retention policy.
