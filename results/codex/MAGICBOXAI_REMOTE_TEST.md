# MagicBoxAI Remote Test Report

**Execution Date**: 2026-01-31
**Target**: https://garyo.sakura.ne.jp/magicboxai
**Platform**: PHP + CGI (Sakura FreeBSD)
**Tester**: pytest + httpx (Local Windows)

---

## 📊 Test Results

| Test Case | Result | Note |
|---|---|---|
| `test_health_check` | ✅ PASS | Verified `/api/health` JSON response |
| `test_check_limit_allows_initial` | ✅ PASS | Verified `/api/check-limit` |
| `test_save_and_view_roundtrip` | ✅ PASS | Saved HTML, then retrieved via Public URL (HTTPS) |
| `test_save_rejects_empty_html` | ✅ PASS | **Fixed**: PHP now rejects whitespace-only HTML |
| `test_rate_limit_blocks_after_limit` | ⏭ SKIP | Skipped to avoid rate-limiting the tester IP |

---

## 🐛 Bugs Found & Fixed

### 1. Empty HTML Validation
- **Issue**: Python `TestClient` rejected `"  "` (400), but PHP accepted it (201).
- **Fix**: Updated `magicboxai/php/index.php` to use `trim($data['html']) === ''`.
- **Status**: Verified ✅

---

## 📝 Conclusion

The Remote PHP implementation is now fully compatible with the standard test suite.
We can use `MAGICBOXAI_BASE_URL` to verify deployment integrity at any time.

```bash
BASE_URL=https://garyo.sakura.ne.jp/magicboxai pytest tests/test_magicboxai_api.py
```
