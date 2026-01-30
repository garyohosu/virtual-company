# MagicBoxAI - Test Results After Fix

**Date**: 2026-01-31T05:42:05.7342989+09:00
**Command**: python -m pytest tests/test_magicboxai_api.py -v

## Summary
- Total: 4
- Passed: 1
- Failed: 3

## Failed Tests
- 	est_check_limit_allows_initial -> sqlite3.OperationalError: no such table: track_limit_daily
- 	est_save_and_view_roundtrip -> sqlite3.OperationalError: no such table: track_limit_daily
- 	est_rate_limit_blocks_after_limit -> sqlite3.OperationalError: no such table: track_limit_daily

## Notes
- Startup event that calls ensure_db() is not triggered when using TestClient(app) without lifespan context.
