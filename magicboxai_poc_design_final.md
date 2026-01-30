# MagicBoxAI PoC Design Final

Section 1: Architecture
- Database schema (simple)
  - storage: file-based JSON + HTML (PoC), or SQLite for later
  - record fields:
    - id (base62, 8-10 chars)
    - public_token (same as id)
    - mgmt_token (separate random token)
    - created_at
    - expires_at (created_at + 30 days)
    - status (active | reported | removed)
    - size_bytes
    - ip_hash (optional)
- API endpoints (minimal)
  - POST /api/save
  - GET /p/{public_token}
  - GET /saved/{mgmt_token}
  - DELETE /api/delete/{mgmt_token}
  - POST /api/report/{public_token}
- File storage (strategy)
  - /data/ab/cd/{id}.html for HTML
  - /data/ab/cd/{id}.json for metadata
  - shard by first 2-4 chars of id
  - write with flock/atomic rename
- 30-day auto-delete mechanism
  - scheduled job (cron) deletes expired records + files daily
  - cleanup also runs on read if expires_at < now
- iframe isolation design
  - always render user HTML inside iframe
  - sandbox="allow-scripts allow-forms"
  - do not allow same-origin, top-navigation, or popups

Section 2: Four Core Flows (detailed)
1. Paste flow: HTML input -> validation -> preview
   - validate size <= 200KB
   - reject non-HTML or multi-file submissions
   - show clear error message if invalid
2. Preview flow: render in iframe
   - iframe sandbox enabled
   - fixed height or CSS-based sizing
   - no postMessage bridge
3. Save flow: store -> generate URLs -> return to user
   - generate public_token and mgmt_token
   - write HTML + metadata
   - return public_url and mgmt_url
4. View flow: public URL -> wrapper -> iframe render
   - wrapper page loads HTML via iframe
   - if status=reported/removed: show blocked message

Section 3: Security
- iframe isolation
  - sandbox, no same-origin, no top-navigation
- Direct-access blocking
  - serve HTML only via wrapper endpoints
  - deny direct file path access
- CSP headers
  - default-src 'none'
  - script-src 'unsafe-inline' https: data: blob:
  - style-src 'unsafe-inline' https: data:
  - img-src https: data:
  - font-src https: data:
  - connect-src https:
  - media-src https: data:
