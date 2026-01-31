<?php
/**
 * Auto-delete old files
 * Run via cron: 0 0 * * * /usr/bin/php /path/to/cron_cleanup.php
 */

$uploadsDir = __DIR__ . '/data/uploads';

if (!is_dir($uploadsDir)) {
    echo "Upload directory not found: {$uploadsDir}\n";
    exit;
}

// Get retention days from ENV or default to 30
$retentionDays = getenv('MAGICBOXAI_RETENTION_DAYS') ? (int)getenv('MAGICBOXAI_RETENTION_DAYS') : 30;
$maxAge = $retentionDays * 24 * 60 * 60;

echo "Starting cleanup (Retention: {$retentionDays} days)...";

$now = time();
$count = 0;

// Scan for JSON metadata files first to clean up both JSON and HTML
$files = glob($uploadsDir . '/*.json');
foreach ($files as $jsonFile) {
    if ($now - filemtime($jsonFile) > $maxAge) {
        $token = basename($jsonFile, '.json');
        $htmlFile = $uploadsDir . '/' . $token . '.html';
        
        unlink($jsonFile);
        if (file_exists($htmlFile)) {
            unlink($htmlFile);
        }
        
        echo "Deleted: {$token}\n";
        $count++;
    }
}

// Also scan for any orphaned HTML files
$htmlFiles = glob($uploadsDir . '/*.html');
foreach ($htmlFiles as $htmlFile) {
    if ($now - filemtime($htmlFile) > $maxAge) {
        unlink($htmlFile);
        echo "Deleted orphaned: " . basename($htmlFile) . "\n";
        $count++;
    }
}

echo "Cleanup complete. Deleted {$count} items.";
?>