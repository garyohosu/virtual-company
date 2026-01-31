# 🔒 MagicBoxAI セキュリティ修正指示書

**作成日**: 2026-01-31  
**優先度**: 🔴 **最優先（即座に対応必要）**  
**対象**: magic-box-ai リポジトリ  
**実行方法**: `gemini --yolo instructions/order_magicboxai_security_fixes_20260131.md`

---

## 🚨 修正が必要な重大な脆弱性

コードレビューの結果、以下の重大なセキュリティ脆弱性が発見されました。
これらは即座に修正する必要があります。

---

## 修正1: XSS（クロスサイトスクリプティング）対策

### 📍 対象ファイル
- `magic-box-ai/src/index.php`

### ⚠️ 現在の問題
```php
// Line 26-36: ユーザー入力をそのまま出力
if (isset($_GET['id'])) {
    $id = $_GET['id'];
    $file = 'data/uploads/' . $id . '.html';
    
    if (file_exists($file)) {
        echo file_get_contents($file);  // ⚠️ 危険！
    }
}
```

**脆弱性**: ユーザーが保存した HTML に悪意のあるスクリプト（`<script>alert('XSS')</script>`など）が含まれていた場合、そのまま実行される。

### ✅ 修正内容

```php
// Display HTML（修正版）
if (isset($_GET['id'])) {
    // 1. IDの厳密な検証（英数字のみ）
    $id = $_GET['id'];
    if (!preg_match('/^[a-f0-9]+$/', $id)) {
        http_response_code(400);
        die('Invalid ID format');
    }
    
    // 2. パストラバーサル対策（realpath使用）
    $file = 'data/uploads/' . $id . '.html';
    $realFile = realpath($file);
    $uploadsDir = realpath('data/uploads');
    
    if ($realFile === false || strpos($realFile, $uploadsDir) !== 0) {
        http_response_code(404);
        die('Not found');
    }
    
    // 3. セキュリティヘッダーの追加
    header("Content-Security-Policy: sandbox allow-scripts allow-same-origin;");
    header("X-Content-Type-Options: nosniff");
    header("X-Frame-Options: SAMEORIGIN");
    header("Referrer-Policy: no-referrer");
    
    // 4. ファイル出力
    if (file_exists($realFile)) {
        header('Content-Type: text/html; charset=UTF-8');
        readfile($realFile);
    } else {
        http_response_code(404);
        echo 'Not found';
    }
    exit;
}
```

---

## 修正2: パストラバーサル脆弱性の修正

### ⚠️ 現在の問題
```php
// Line 13-17: ファイル名の検証不足
$file = 'data/uploads/' . $id . '.html';  // ⚠️ ../../../etc/passwd が可能
```

**脆弱性**: `?id=../../../../etc/passwd%00` のような入力で、システムファイルが読み取られる可能性がある。

### ✅ 修正内容

上記の修正1で `realpath()` と `strpos()` を使用することで対策済み。

追加の検証：
```php
// IDの形式を厳密にチェック
if (!preg_match('/^[a-f0-9]{13,16}$/', $id)) {
    http_response_code(400);
    die('Invalid ID format');
}

// uniqid() の形式に準拠（13-16文字の16進数）
```

---

## 修正3: CSRF（クロスサイトリクエストフォージェリ）対策

### ⚠️ 現在の問題
```php
// Line 11-23: CSRF トークンなし
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['html'])) {
    // トークン検証なし ⚠️
    $html = $_POST['html'];
    // ... 保存処理
}
```

### ✅ 修正内容

```php
// ファイルの先頭に追加
session_start();

// CSRFトークン生成（初回のみ）
if (!isset($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}

// Store HTML（修正版）
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['html'])) {
    // 1. CSRF検証
    if (!isset($_POST['csrf_token']) || 
        !hash_equals($_SESSION['csrf_token'], $_POST['csrf_token'])) {
        http_response_code(403);
        header('Content-Type: application/json');
        echo json_encode(['success' => false, 'error' => 'CSRF validation failed']);
        exit;
    }
    
    // 2. HTMLの検証
    $html = $_POST['html'];
    
    // 3. ファイルサイズ制限（1MB）
    if (strlen($html) > 1 * 1024 * 1024) {
        http_response_code(413);
        header('Content-Type: application/json');
        echo json_encode(['success' => false, 'error' => 'File too large (max 1MB)']);
        exit;
    }
    
    // 4. 空チェック
    if (trim($html) === '') {
        http_response_code(400);
        header('Content-Type: application/json');
        echo json_encode(['success' => false, 'error' => 'HTML content required']);
        exit;
    }
    
    // 5. IDの生成
    $id = uniqid();
    
    // 6. ディレクトリの作成（存在チェック）
    $uploadDir = 'data/uploads/';
    if (!is_dir($uploadDir)) {
        mkdir($uploadDir, 0755, true);
    }
    
    // 7. ファイルの保存
    $file = $uploadDir . $id . '.html';
    if (file_put_contents($file, $html) === false) {
        http_response_code(500);
        header('Content-Type: application/json');
        echo json_encode(['success' => false, 'error' => 'Failed to save file']);
        exit;
    }
    
    // 8. 成功レスポンス
    header('Content-Type: application/json');
    echo json_encode(['success' => true, 'id' => $id, 'url' => "?id=$id"]);
    exit;
}
```

### HTMLフォームの修正

```javascript
// JavaScriptでCSRFトークンを含める
function submitHTML() {
    const html = document.getElementById('htmlInput').value.trim();
    
    document.getElementById('confirmModal').classList.add('hidden');
    showLoading();

    // CSRFトークンを追加
    const formData = new URLSearchParams();
    formData.append('html', html);
    formData.append('csrf_token', '<?php echo $_SESSION['csrf_token']; ?>');

    fetch(window.location.href, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formData.toString()
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        
        if (data.success) {
            showResult(data.url);
        } else {
            showError(data.error || 'エラーが発生しました');
        }
    })
    .catch(error => {
        hideLoading();
        showError('ネットワークエラー: ' + error.message);
    });
}
```

---

## 修正4: UTF-8 BOM の削除

### ⚠️ 対象ファイル
- `magic-box-ai/src/cron_cleanup.php`
- `magic-box-ai/.github/workflows/deploy.yml`

### 問題
```
﻿<?php  // ⚠️ BOM (Byte Order Mark) が含まれている
```

**影響**:
- HTTPヘッダーエラー
- セッションエラー
- 予期しない出力

### ✅ 修正方法

#### 方法1: コマンドラインで削除
```bash
cd magic-box-ai/src
sed -i '1s/^\xEF\xBB\xBF//' cron_cleanup.php

cd ../.github/workflows
sed -i '1s/^\xEF\xBB\xBF//' deploy.yml
```

#### 方法2: エディタで修正
1. ファイルを開く
2. 「名前を付けて保存」→「エンコーディング」→「UTF-8（BOMなし）」を選択
3. 保存

---

## 修正5: ファイルサイズ制限の追加

### ⚠️ 現在の問題
無制限にファイルを保存できる → ディスク容量を使い果たす可能性

### ✅ 修正内容

上記の修正3に含まれています：
```php
// ファイルサイズ制限（1MB）
if (strlen($html) > 1 * 1024 * 1024) {
    http_response_code(413);
    header('Content-Type: application/json');
    echo json_encode(['success' => false, 'error' => 'File too large (max 1MB)']);
    exit;
}
```

---

## 修正6: エラーハンドリングの改善

### 📍 対象ファイル
- `magic-box-ai/src/cron_cleanup.php`

### ⚠️ 現在の問題
```php
foreach ($files as $file) {
    if ($now - filemtime($file) > $maxAge) {
        unlink($file);  // ⚠️ 失敗時の処理なし
        echo "Deleted: $file\n";
    }
}
```

### ✅ 修正内容

```php
<?php
/**
 * Auto-delete old files
 * Run via cron: 0 0 * * * /usr/bin/php /path/to/cron_cleanup.php
 */

// エラーログの設定
$logFile = __DIR__ . '/data/cleanup.log';

function logMessage($message, $logFile) {
    $timestamp = date('Y-m-d H:i:s');
    file_put_contents($logFile, "[$timestamp] $message\n", FILE_APPEND);
}

$uploadsDir = __DIR__ . '/data/uploads';
$maxAge = 30 * 24 * 60 * 60; // 30 days
$now = time();

// ディレクトリ存在チェック
if (!is_dir($uploadsDir)) {
    logMessage("ERROR: Uploads directory not found: $uploadsDir", $logFile);
    exit(1);
}

$files = glob($uploadsDir . '/*.html');
$deletedCount = 0;
$errorCount = 0;

foreach ($files as $file) {
    try {
        // ファイル情報の取得
        $mtime = filemtime($file);
        
        if ($mtime === false) {
            logMessage("WARNING: Cannot get file modification time: $file", $logFile);
            $errorCount++;
            continue;
        }
        
        // 有効期限チェック
        if ($now - $mtime > $maxAge) {
            if (unlink($file)) {
                logMessage("INFO: Deleted: $file", $logFile);
                echo "Deleted: $file\n";
                $deletedCount++;
            } else {
                logMessage("ERROR: Failed to delete: $file", $logFile);
                echo "Failed to delete: $file\n";
                $errorCount++;
            }
        }
    } catch (Exception $e) {
        logMessage("ERROR: Exception while processing $file: " . $e->getMessage(), $logFile);
        $errorCount++;
    }
}

logMessage("INFO: Cleanup complete. Deleted: $deletedCount, Errors: $errorCount", $logFile);
echo "Cleanup complete. Deleted: $deletedCount files, Errors: $errorCount\n";

exit($errorCount > 0 ? 1 : 0);
?>
```

---

## 🔧 実装手順

### Step 1: ローカルで修正

```bash
# magic-box-ai リポジトリに移動
cd ~/garyohosu/magic-box-ai

# ブランチ作成
git checkout -b security-fixes-20260131

# ファイルを修正（上記の内容に従って）
# 1. src/index.php を修正
# 2. src/cron_cleanup.php を修正
# 3. BOM を削除

# 修正を確認
git diff

# コミット
git add .
git commit -m "fix: Critical security vulnerabilities

- Fix XSS vulnerability with CSP headers
- Fix path traversal vulnerability with realpath validation
- Add CSRF token validation
- Add file size limit (1MB)
- Improve error handling in cron cleanup
- Remove UTF-8 BOM from PHP files

Security issues identified in CODE_REVIEW_REPORT_20260131.md"

# プッシュ
git push origin security-fixes-20260131
```

### Step 2: PR作成

```bash
# GitHub CLI でPR作成
gh pr create \
  --title "fix: Critical security vulnerabilities" \
  --body "## 🔒 セキュリティ修正

コードレビュー（CODE_REVIEW_REPORT_20260131.md）で発見された重大な脆弱性を修正します。

### 🚨 修正内容

#### 🔴 最優先修正
1. **XSS脆弱性の修正**
   - Content Security Policy ヘッダーを追加
   - sandbox 属性でスクリプト実行を制限

2. **パストラバーサル脆弱性の修正**
   - realpath() で絶対パスを検証
   - IDの形式を厳密にチェック

3. **CSRF対策の実装**
   - セッショントークンの追加
   - hash_equals() で安全な比較

4. **ファイルサイズ制限の追加**
   - 1MB の制限を実装
   - ディスク容量の保護

5. **エラーハンドリングの改善**
   - cron_cleanup.php のエラー処理を追加
   - ログファイルへの記録

6. **UTF-8 BOM の削除**
   - cron_cleanup.php
   - deploy.yml

### ✅ テスト
- [ ] XSS攻撃のテスト
- [ ] パストラバーサル攻撃のテスト
- [ ] CSRF攻撃のテスト
- [ ] ファイルサイズ制限のテスト
- [ ] 自動削除機能のテスト

### 📝 参照
- CODE_REVIEW_REPORT_20260131.md
- OWASP Top 10" \
  --base main \
  --head security-fixes-20260131
```

### Step 3: テスト実施

```bash
# ローカルでテスト
cd ~/garyohosu/magic-box-ai

# PHPUnit テスト
composer install
./vendor/bin/phpunit tests/Unit

# pytest テスト
pip install -r requirements.txt
pytest tests/integration -v

# セキュリティテストの追加（推奨）
# tests/Unit/SecurityTest.php を作成してテスト
```

### Step 4: デプロイ

```bash
# mainブランチにマージ後、自動デプロイが実行される
# GitHub Actions で以下が実行される:
# 1. PHPUnit テスト
# 2. pytest テスト
# 3. Sakura サーバーへのデプロイ
```

---

## ✅ 修正後の確認チェックリスト

### セキュリティチェック
- [ ] XSS攻撃が防止されている
- [ ] パストラバーサル攻撃が防止されている
- [ ] CSRF攻撃が防止されている
- [ ] ファイルサイズ制限が機能している
- [ ] エラーログが記録されている
- [ ] UTF-8 BOMが削除されている

### 機能チェック
- [ ] HTMLの保存が正常に動作する
- [ ] HTMLの表示が正常に動作する
- [ ] 30日後の自動削除が機能する
- [ ] エラーメッセージが適切に表示される

### 性能チェック
- [ ] ページの読み込み速度が許容範囲内
- [ ] ファイルの保存速度が許容範囲内
- [ ] cronジョブが正常に動作する

---

## 📊 修正前後の比較

### 修正前（脆弱）
```php
// ⚠️ 危険なコード
if (isset($_GET['id'])) {
    $id = $_GET['id'];
    $file = 'data/uploads/' . $id . '.html';
    if (file_exists($file)) {
        echo file_get_contents($file);  // XSS可能
    }
}

// ⚠️ CSRF対策なし
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $html = $_POST['html'];
    file_put_contents($file, $html);  // サイズ制限なし
}
```

### 修正後（安全）
```php
// ✅ 安全なコード
if (isset($_GET['id'])) {
    // 厳密な検証
    if (!preg_match('/^[a-f0-9]+$/', $_GET['id'])) {
        http_response_code(400);
        die('Invalid ID');
    }
    
    // パストラバーサル対策
    $realFile = realpath('data/uploads/' . $_GET['id'] . '.html');
    $uploadsDir = realpath('data/uploads');
    
    if ($realFile === false || strpos($realFile, $uploadsDir) !== 0) {
        http_response_code(404);
        die('Not found');
    }
    
    // CSPヘッダー
    header("Content-Security-Policy: sandbox allow-scripts;");
    readfile($realFile);
}

// ✅ CSRF対策あり + サイズ制限
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // CSRF検証
    if (!hash_equals($_SESSION['csrf_token'], $_POST['csrf_token'])) {
        die('CSRF validation failed');
    }
    
    // サイズ制限
    if (strlen($_POST['html']) > 1024 * 1024) {
        die('File too large');
    }
    
    // 保存
    file_put_contents($file, $_POST['html']);
}
```

---

## 🎓 参考資料

### セキュリティベストプラクティス
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [PHP Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/PHP_Configuration_Cheat_Sheet.html)
- [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)

### PHPセキュリティ関数
- `realpath()` - パストラバーサル対策
- `hash_equals()` - タイミング攻撃対策
- `htmlspecialchars()` - XSS対策（HTML出力時）
- `filter_var()` - 入力検証

---

## 📝 注意事項

1. **バックアップ**: 修正前に必ずバックアップを取る
2. **テスト**: ローカル環境で十分にテストする
3. **段階的デプロイ**: 一度に全て修正せず、段階的に実施
4. **監視**: デプロイ後はエラーログを監視する

---

**このファイルを実行**:
```bash
cd ~/garyohosu/virtual-company
git pull origin main
gemini --yolo instructions/order_magicboxai_security_fixes_20260131.md
```

---

**Status**: 準備完了  
**Priority**: 🔴 最優先  
**Current Actor**: Gemini  
**Next Actor**: User（動作確認）  
**Created At**: 2026-01-31
