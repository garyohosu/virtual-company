<?php
/**
 * Auto-delete old files
 * Run via cron: 0 0 * * * /usr/bin/php /path/to/cron_cleanup.php
 */

// エラーログの設定
$logDir = __DIR__ . '/data';
if (!is_dir($logDir)) {
    mkdir($logDir, 0755, true);
}
$logFile = $logDir . '/cleanup.log';

function logMessage($message, $logFile) {
    $timestamp = date('Y-m-d H:i:s');
    file_put_contents($logFile, "[$timestamp] $message\n", FILE_APPEND);
}

$uploadsDir = __DIR__ . '/data/uploads';

// Get retention days from ENV or default to 30
$retentionDays = getenv('MAGICBOXAI_RETENTION_DAYS') ? (int)getenv('MAGICBOXAI_RETENTION_DAYS') : 30;
$maxAge = $retentionDays * 24 * 60 * 60;
$now = time();

// ディレクトリ存在チェック
if (!is_dir($uploadsDir)) {
    logMessage("ERROR: Uploads directory not found: $uploadsDir", $logFile);
    echo "Upload directory not found: {$uploadsDir}\n";
    exit(1);
}

logMessage("INFO: Starting cleanup (Retention: {$retentionDays} days)...", $logFile);
echo "Starting cleanup (Retention: {$retentionDays} days)...
";

$deletedCount = 0;
$errorCount = 0;

// Scan for JSON metadata files first to clean up both JSON and HTML
$files = glob($uploadsDir . '/*.json');
foreach ($files as $jsonFile) {
    try {
        $mtime = filemtime($jsonFile);
        if ($mtime === false) {
            logMessage("WARNING: Cannot get file modification time: $jsonFile", $logFile);
            $errorCount++;
            continue;
        }

        if ($now - $mtime > $maxAge) {
            $token = basename($jsonFile, '.json');
            $htmlFile = $uploadsDir . '/' . $token . '.html';
            
            $success = true;
            if (!unlink($jsonFile)) {
                logMessage("ERROR: Failed to delete: $jsonFile", $logFile);
                $success = false;
            }
            
            if (file_exists($htmlFile)) {
                if (!unlink($htmlFile)) {
                    logMessage("ERROR: Failed to delete: $htmlFile", $logFile);
                    $success = false;
                }
            }
            
            if ($success) {
                logMessage("INFO: Deleted: $token", $logFile);
                echo "Deleted: $token\n";
                $deletedCount++;
            } else {
                $errorCount++;
            }
        }
    } catch (Exception $e) {
        logMessage("ERROR: Exception while processing $jsonFile: " . $e->getMessage(), $logFile);
        $errorCount++;
    }
}

// Also scan for any orphaned HTML files
$htmlFiles = glob($uploadsDir . '/*.html');
foreach ($htmlFiles as $htmlFile) {
    try {
        $mtime = filemtime($htmlFile);
        if ($mtime === false) continue;

        if ($now - $mtime > $maxAge) {
            if (unlink($htmlFile)) {
                logMessage("INFO: Deleted orphaned: " . basename($htmlFile), $logFile);
                echo "Deleted orphaned: " . basename($htmlFile) . "\n";
                $deletedCount++;
            } else {
                logMessage("ERROR: Failed to delete orphaned: $htmlFile", $logFile);
                $errorCount++;
            }
        }
    } catch (Exception $e) {
        logMessage("ERROR: Exception while processing $htmlFile: " . $e->getMessage(), $logFile);
        $errorCount++;
    }
}

logMessage("INFO: Cleanup complete. Deleted: $deletedCount, Errors: $errorCount", $logFile);
echo "Cleanup complete. Deleted: $deletedCount items, Errors: $errorCount\n";

exit($errorCount > 0 ? 1 : 0);
?>
