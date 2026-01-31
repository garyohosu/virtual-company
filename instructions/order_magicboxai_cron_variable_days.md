# Order - MagicBoxAI Cron Variable Days

**Status**: ⏳ Implementation Waiting
**Current Actor**: Gemini CLI
**Goal**: Make the cleanup period in cron_cleanup.php configurable via environment variable.

---

## 🎯 Mission

Modify `src/cron_cleanup.php` to use `MAGICBOXAI_RETENTION_DAYS` environment variable if available, defaulting to 30 days.

## 📋 Implementation

### 1. Modify src/cron_cleanup.php

```php
<?php
/**
 * Auto-delete old files
 * Run via cron: 0 0 * * * /usr/bin/php /path/to/cron_cleanup.php
 */

$uploadsDir = __DIR__ . '/data/uploads';

// Get retention days from ENV or default to 30
$retentionDays = getenv('MAGICBOXAI_RETENTION_DAYS') ? (int)getenv('MAGICBOXAI_RETENTION_DAYS') : 30;
$maxAge = $retentionDays * 24 * 60 * 60;

echo "Starting cleanup (Retention: {$retentionDays} days)...
";

$now = time();
$count = 0;

$files = glob($uploadsDir . '/*.html');
foreach ($files as $file) {
    if ($now - filemtime($file) > $maxAge) {
        unlink($file);
        echo "Deleted: " . basename($file) . "\n";
        $count++;
    }
}

echo "Cleanup complete. Deleted {$count} files.\n";
?>
```

---

## ✅ Success Criteria

- [ ] `src/cron_cleanup.php` reads `MAGICBOXAI_RETENTION_DAYS`.
- [ ] Defaults to 30 if not set.
- [ ] Logging improved (shows retention days and deleted count).
