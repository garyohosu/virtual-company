<?php
// MagicBoxAI - PHP + CGI 版 (Fixed Routing & HTTPS)

session_start();

// CSRFトークン生成（初回のみ）
if (!isset($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}

header('Content-Type: text/html; charset=UTF-8');
$db_file = __DIR__ . '/data/magicboxai.db';

function init_db() {
    global $db_file;
    if (!file_exists($db_file)) {
        $db_dir = dirname($db_file);
        if (!is_dir($db_dir)) mkdir($db_dir, 0755, true);
        touch($db_file);
        file_put_contents($db_dir . '/files.json', json_encode([]));
    }
}
init_db();

// ルーティング
$request_uri = $_SERVER['REQUEST_URI'];
$script_name = $_SERVER['SCRIPT_NAME']; // 例: /magicboxai/index.php

$base_path = dirname($script_name); // /magicboxai
$request_path = str_replace($base_path, '', $request_uri); 

// index.php を除去
$request_path = str_replace('/index.php', '', $request_path); 
if ($request_path === '') $request_path = '/';

if ($request_path === '/') {
    include __DIR__ . '/pages/home.php';
} elseif (strpos($request_path, '/api/health') === 0) {
    header('Content-Type: application/json');
    echo json_encode(['status' => 'ok', 'timestamp' => date('c'), 'engine' => 'php']);
} elseif (strpos($request_path, '/api/check-limit') === 0) {
    header('Content-Type: application/json');
    echo json_encode(['allowed' => true, 'count' => 0, 'limit' => 5]);
} elseif (strpos($request_path, '/api/save') === 0) {
    handle_save();
} elseif (strpos($request_path, '/view/') === 0) {
    $token = basename($request_path);
    handle_view($token);
} else {
    http_response_code(404);
    echo 'Not found: ' . htmlspecialchars($request_path);
}

function handle_save() {
    header('Content-Type: application/json');
    
    // 1. CSRF検証
    $csrf_token = null;
    $html = null;

    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        if (strpos($_SERVER['CONTENT_TYPE'], 'application/json') !== false) {
            $input = file_get_contents('php://input');
            $data = json_decode($input, true);
            $csrf_token = $data['csrf_token'] ?? null;
            $html = $data['html'] ?? null;
        } else {
            $csrf_token = $_POST['csrf_token'] ?? null;
            $html = $_POST['html'] ?? null;
        }
    }

    if (!$csrf_token || !isset($_SESSION['csrf_token']) || !hash_equals($_SESSION['csrf_token'], $csrf_token)) {
        http_response_code(403);
        echo json_encode(['success' => false, 'error' => 'CSRF validation failed']);
        exit;
    }

    // 2. HTMLの検証
    if (!$html || trim($html) === '') {
        http_response_code(400);
        echo json_encode(['success' => false, 'error' => 'HTML content required']);
        exit;
    }
    
    // 3. ファイルサイズ制限（1MB）
    if (strlen($html) > 1 * 1024 * 1024) {
        http_response_code(413);
        echo json_encode(['success' => false, 'error' => 'File too large (max 1MB)']);
        exit;
    }

    $token = bin2hex(random_bytes(8));
    $save_dir = __DIR__ . '/data/uploads';
    if (!is_dir($save_dir)) mkdir($save_dir, 0755, true);
    
    $file_path = $save_dir . '/' . $token . '.html';
    if (file_put_contents($file_path, $html) === false) {
        http_response_code(500);
        echo json_encode(['success' => false, 'error' => 'Failed to save file']);
        exit;
    }

    $retentionDays = getenv('MAGICBOXAI_RETENTION_DAYS') ? (int)getenv('MAGICBOXAI_RETENTION_DAYS') : 30;
    $metadata = [
        'token' => $token, 
        'created_at' => date('c'), 
        'expires_at' => date('c', strtotime("+{$retentionDays} days"))
    ];
    file_put_contents($save_dir . '/' . $token . '.json', json_encode($metadata));
    
    // HTTPS 対応
    $protocol = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http';
    $base_url = $protocol . '://' . $_SERVER['HTTP_HOST'] . dirname($_SERVER['SCRIPT_NAME']);
    
    http_response_code(201);
    echo json_encode([
        'status' => 'saved', 
        'success' => true,
        'token' => $token, 
        'public_url' => rtrim($base_url, '/') . '/view/' . $token,
        'expires_at' => $metadata['expires_at']
    ]);
}

function handle_view($token) {
    // 1. IDの厳密な検証（英数字のみ、8バイトのbin2hexは16文字）
    if (!preg_match('/^[a-f0-9]{16}$/', $token)) {
        http_response_code(400);
        die('Invalid ID format');
    }

    $save_dir = __DIR__ . '/data/uploads';
    $file_path = $save_dir . '/' . $token . '.html';
    
    // 2. パストラバーサル対策（realpath使用）
    $realFile = realpath($file_path);
    $uploadsDir = realpath($save_dir);
    
    if ($realFile === false || strpos($realFile, $uploadsDir) !== 0) {
        http_response_code(404);
        die('Not found');
    }

    if (!file_exists($realFile)) {
        http_response_code(404); echo 'Not found'; return;
    }

    // 3. セキュリティヘッダーの追加
    header("Content-Security-Policy: sandbox allow-scripts allow-same-origin;");
    header("X-Content-Type-Options: nosniff");
    header("X-Frame-Options: SAMEORIGIN");
    header("Referrer-Policy: no-referrer");
    header('Content-Type: text/html; charset=UTF-8');
    
    readfile($realFile);
}
?>
