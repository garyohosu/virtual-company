<?php
// 30 日以上前のファイルを削除

$upload_dir = __DIR__ . '/data/uploads';

if (!is_dir($upload_dir)) {
    exit;
}

$files = glob($upload_dir . '/*.json');

foreach ($files as $json_file) {
    $metadata = json_decode(file_get_contents($json_file), true);
    if (!$metadata) continue;
    
    $expires_at = strtotime($metadata['expires_at']);
    
    if (time() > $expires_at) {
        $token = $metadata['token'];
        unlink($json_file);
        $html_file = $upload_dir . '/' . $token . '.html';
        if (file_exists($html_file)) {
            unlink($html_file);
        }
    }
}

echo "Cleanup completed at " . date('c') . "\n";
?>
