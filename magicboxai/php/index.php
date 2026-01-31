<?php
// MagicBoxAI - PHP + CGI 版 (Fixed Routing & HTTPS)

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
    $input = file_get_contents('php://input');
    $data = json_decode($input, true);
    if (!isset($data['html']) || trim($data['html']) === '') {
        http_response_code(400); echo json_encode(['error' => 'HTML content required']); return;
    }
    $token = bin2hex(random_bytes(8));
    $save_dir = __DIR__ . '/data/uploads';
    if (!is_dir($save_dir)) mkdir($save_dir, 0755, true);
    file_put_contents($save_dir . '/' . $token . '.html', $data['html']);
    $metadata = ['token' => $token, 'created_at' => date('c'), 'expires_at' => date('c', strtotime('+30 days'))];
    file_put_contents($save_dir . '/' . $token . '.json', json_encode($metadata));
    
    // HTTPS 対応
    $protocol = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http';
    $base_url = $protocol . '://' . $_SERVER['HTTP_HOST'] . dirname($_SERVER['SCRIPT_NAME']);
    
    http_response_code(201);
    echo json_encode([
        'status' => 'saved', 
        'token' => $token, 
        'public_url' => rtrim($base_url, '/') . '/view/' . $token,
        'expires_at' => $metadata['expires_at']
    ]);
}

function handle_view($token) {
    $save_dir = __DIR__ . '/data/uploads';
    $file_path = $save_dir . '/' . $token . '.html';
    if (!file_exists($file_path)) {
        http_response_code(404); echo 'Not found'; return;
    }
    header('Content-Type: text/html; charset=UTF-8');
    readfile($file_path);
}
?>
