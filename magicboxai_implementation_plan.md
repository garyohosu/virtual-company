## Phases

Phase 1: Backend MVP (must have)
- File storage system (file system or cloud)
- API: POST /api/save (save HTML) -> return public_url + mgmt_url
- API: DELETE /api/delete/{token} (delete with mgmt_url)
- Database: store metadata (created_at, expires_at, public_token, mgmt_token)
- Auto-delete cron job (delete files older than 30 days)
- Estimate: 300-500 lines of code (Python FastAPI or Node.js Express)

Phase 2: Frontend MVP (must have)
- Simple HTML form: textarea for code
- Preview iframe (shows live HTML)
- Save button -> calls API
- Display public_url + mgmt_url
- Copy-to-clipboard button
- Estimate: 200-300 lines of HTML/CSS/JS

Phase 3: Security Hardening (should have)
- CSP headers
- Input validation
- Rate limiting
- Reporting form
- Moderation UI (admin can delete reported items)
- Estimate: 200 lines

Phase 4: Operational Tasks (should have)
- Logging system
- Monitoring (PV, storage usage)
- Admin dashboard
- Estimate: 150 lines

## Tech Stack Recommendation
- Backend: Python (Flask/FastAPI) or Node.js (Express)
- Frontend: Plain HTML/CSS/JS (no framework needed)
- Database: SQLite (for MVP) or PostgreSQL (for scale)
- Storage: Local file system (for MVP) or S3 (for scale)
- Deployment: Heroku / Railway / VPS (Sakura Internet)

## Timeline
- Phase 1+2 MVP: 1-2 weeks
- Phase 3 Security: 1 week
- Phase 4 Operations: 1 week
- Total: 3-4 weeks for production ready

## Effort Estimate (One Developer)
- Phase 1: 3-4 days
- Phase 2: 2-3 days
- Phase 3: 2 days
- Phase 4: 1-2 days
