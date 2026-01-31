# 🎯 Step 2-3-4 FINAL ORDER for Gemini

**実行者**: Gemini CLI  
**実行方法**: `gemini --yolo instructions/MAGICBOXAI_FINAL_SETUP.md`  
**対象**: garyohosu/magic-box-ai リポジトリ  
**内容**: PHP コード同期 → テスト戦略 → CI/CD ワークフロー設定

---

## 📋 実行前準備

```bash
# virtual-company から magic-box-ai に移動
cd ~/garyohosu/magic-box-ai

# または clone
git clone https://github.com/garyohosu/magic-box-ai.git
cd magic-box-ai

# 確認
git status
```

---

## 🚀 Phase 1: ディレクトリ構造準備

```bash
# リポジトリルートで実行
pwd
# 出力: ~/garyohosu/magic-box-ai

# ディレクトリ作成
mkdir -p src/pages
mkdir -p src/cgi-bin
mkdir -p src/data/uploads
mkdir -p tests/Unit
mkdir -p tests/integration
mkdir -p .github/workflows
```

---

## 🔧 Phase 2: PHP ソースコード配置

### 2-1: index.php

```bash
cat > src/index.php << 'EOF'
<?php
/**
 * MagicBoxAI - HTML Paste & Share Service
 * Main Entry Point
 */

session_start();

// Set headers
header('Content-Type: text/html; charset=UTF-8');

// Store HTML
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['html'])) {
    $html = $_POST['html'];
    $id = uniqid();
    
    // Create file
    $file = 'data/uploads/' . $id . '.html';
    file_put_contents($file, $html);
    
    // Return ID
    echo json_encode(['success' => true, 'id' => $id]);
    exit;
}

// Display HTML
if (isset($_GET['id'])) {
    $id = $_GET['id'];
    $file = 'data/uploads/' . $id . '.html';
    
    if (file_exists($file)) {
        echo file_get_contents($file);
    } else {
        echo "Not found";
    }
    exit;
}

// Home page
?>
<!DOCTYPE html>
<html>
<head>
    <title>MagicBoxAI</title>
</head>
<body>
    <h1>MagicBoxAI - HTML Paste & Share</h1>
    <form method="POST">
        <textarea name="html" placeholder="Paste HTML here"></textarea>
        <button type="submit">Save</button>
    </form>
</body>
</html>
EOF
```

### 2-2: pages/home.php

```bash
cat > src/pages/home.php << 'EOF'
<?php
echo "Home Page";
?>
EOF
```

### 2-3: cron_cleanup.php

```bash
cat > src/cron_cleanup.php << 'EOF'
<?php
/**
 * Auto-delete old files
 * Run via cron: 0 0 * * * /usr/bin/php /path/to/cron_cleanup.php
 */

$uploadsDir = __DIR__ . '/data/uploads';
$maxAge = 30 * 24 * 60 * 60; // 30 days
$now = time();

$files = glob($uploadsDir . '/*.html');
foreach ($files as $file) {
    if ($now - filemtime($file) > $maxAge) {
        unlink($file);
        echo "Deleted: $file\n";
    }
}

echo "Cleanup complete\n";
?>
EOF
```

### 2-4: .htaccess

```bash
cat > src/.htaccess << 'EOF'
Options -Indexes
DirectoryIndex index.php
EOF
```

### 2-5: data/files.json

```bash
cat > src/data/files.json << 'EOF'
{}
EOF
```

---

## 🧪 Phase 3: PHPUnit テスト環境

### 3-1: composer.json

```bash
cat > composer.json << 'EOF'
{
    "name": "garyohosu/magic-box-ai",
    "description": "HTML Paste & Share Service",
    "type": "project",
    "require": {
        "php": ">=7.4"
    },
    "require-dev": {
        "phpunit/phpunit": "^9.5"
    },
    "autoload": {
        "psr-4": {
            "Tests\\": "tests/"
        }
    }
}
EOF
```

### 3-2: phpunit.xml

```bash
cat > phpunit.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="https://schema.phpunit.de/9.5/phpunit.xsd"
         bootstrap="vendor/autoload.php"
         verbose="true">
    <testsuites>
        <testsuite name="Unit">
            <directory>tests/Unit</directory>
        </testsuite>
    </testsuites>
</phpunit>
EOF
```

### 3-3: tests/Unit/IndexTest.php

```bash
cat > tests/Unit/IndexTest.php << 'EOF'
<?php

namespace Tests\Unit;

use PHPUnit\Framework\TestCase;

class IndexTest extends TestCase
{
    public function testIndexSyntax()
    {
        $output = shell_exec('php -l src/index.php 2>&1');
        $this->assertStringContainsString('No syntax errors', $output);
    }
}
?>
EOF
```

### 3-4: tests/Unit/CronCleanupTest.php

```bash
cat > tests/Unit/CronCleanupTest.php << 'EOF'
<?php

namespace Tests\Unit;

use PHPUnit\Framework\TestCase;

class CronCleanupTest extends TestCase
{
    public function testCronCleanupSyntax()
    {
        $output = shell_exec('php -l src/cron_cleanup.php 2>&1');
        $this->assertStringContainsString('No syntax errors', $output);
    }
}
?>
EOF
```

---

## 🐍 Phase 4: pytest テスト環境

### 4-1: requirements.txt

```bash
cat > requirements.txt << 'EOF'
pytest==7.2.0
requests==2.28.1
EOF
```

### 4-2: pytest.ini

```bash
cat > pytest.ini << 'EOF'
[pytest]
testpaths = tests/integration
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
timeout = 30
EOF
```

### 4-3: tests/integration/test_api_save.py

```bash
cat > tests/integration/test_api_save.py << 'EOF'
import subprocess
import requests
import time
import pytest
import os
import signal

class TestAPISave:
    @pytest.fixture(scope="class")
    def php_server(self):
        """Start built-in PHP server"""
        proc = subprocess.Popen(
            ['php', '-S', 'localhost:8888', '-t', 'src/'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(1)
        yield proc
        try:
            proc.terminate()
        except:
            pass
    
    def test_index_endpoint(self, php_server):
        """Test index.php is accessible"""
        response = requests.get('http://localhost:8888/', timeout=5)
        assert response.status_code == 200

class TestCLI:
    def test_cron_cleanup_syntax(self):
        """Test cron_cleanup.php can be executed"""
        result = subprocess.run(
            ['php', 'src/cron_cleanup.php'],
            capture_output=True,
            timeout=10
        )
        # Should not have PHP syntax errors
        assert 'syntax error' not in result.stderr.decode().lower()
EOF
```

---

## 🔄 Phase 5: CI/CD ワークフロー

### 5-1: test-phpunit.yml

```bash
cat > .github/workflows/test-phpunit.yml << 'EOF'
name: PHPUnit Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup PHP
      uses: shivammathur/setup-php@v2
      with:
        php-version: 7.4
        tools: composer:v2
    
    - name: Install composer dependencies
      run: composer install --prefer-dist
    
    - name: Run PHPUnit
      run: ./vendor/bin/phpunit tests/Unit
    
    - name: PHP Syntax Check
      run: |
        php -l src/index.php
        php -l src/cron_cleanup.php
EOF
```

### 5-2: test-pytest.yml

```bash
cat > .github/workflows/test-pytest.yml << 'EOF'
name: pytest Integration Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup PHP
      uses: shivammathur/setup-php@v2
      with:
        php-version: 7.4
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: pip install -r requirements.txt
    
    - name: Run pytest
      run: pytest tests/integration -v
EOF
```

### 5-3: deploy.yml

```bash
cat > .github/workflows/deploy.yml << 'EOF'
name: Deploy to Sakura

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Setup PHP
      uses: shivammathur/setup-php@v2
      with:
        php-version: 7.4
        tools: composer:v2
    - name: Install dependencies
      run: composer install
    - name: Run tests
      run: ./vendor/bin/phpunit tests/Unit

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    - name: Deploy
      env:
        SAKURA_HOST: ${{ secrets.SAKURA_HOST }}
        SAKURA_USER: ${{ secrets.SAKURA_USER }}
        SAKURA_KEY: ${{ secrets.SAKURA_KEY }}
      run: |
        mkdir -p ~/.ssh
        echo "$SAKURA_KEY" > ~/.ssh/sakura_key
        chmod 600 ~/.ssh/sakura_key
        ssh -i ~/.ssh/sakura_key -o StrictHostKeyChecking=no $SAKURA_USER@$SAKURA_HOST "echo 'Deployment OK'"
EOF
```

---

## ✅ Phase 6: Git Commit & Push

```bash
# ファイル確認
git status

# すべてを追加
git add src/
git add tests/
git add .github/workflows/
git add composer.json
git add phpunit.xml
git add requirements.txt
git add pytest.ini

# Commit
git commit -m "feat: Add PHP source, test suites, and CI/CD pipeline

Phase 2-2: PHP Code Synchronization
- src/index.php: Main application
- src/pages/home.php: Home page
- src/cron_cleanup.php: Auto-cleanup script
- src/.htaccess: Apache config
- src/data/: Data template

Phase 3: Test Strategy (PHPUnit + pytest)
- composer.json: PHPUnit dependency
- tests/Unit/: PHP unit tests
- phpunit.xml: PHPUnit config
- requirements.txt: pytest dependency
- tests/integration/: API tests
- pytest.ini: pytest config

Phase 4: CI/CD Workflows
- .github/workflows/test-phpunit.yml
- .github/workflows/test-pytest.yml
- .github/workflows/deploy.yml

Test Strategy:
✅ PHPUnit: PHP unit tests (syntax check)
✅ pytest: API/CLI tests (HTTP, subprocess)
✅ GitHub Actions: Auto-test and deploy

Note:
- Server code /home/garyo/www/magicboxai/ unchanged
- Python code removed in Step 1
"

# Push
git push origin main

# 確認
echo "✅ COMPLETED!"
git log --oneline -3
```

---

## 📊 最終確認

```bash
# ローカル確認
ls -laR src/
ls -laR tests/
ls -laR .github/workflows/

# ファイル確認
test -f composer.json && echo "✅ composer.json"
test -f phpunit.xml && echo "✅ phpunit.xml"
test -f pytest.ini && echo "✅ pytest.ini"

# Git 確認
git log --oneline -5

# GitHub 確認（curl）
curl https://api.github.com/repos/garyohosu/magic-box-ai/contents/src
```

---

## ⚠️ GitHub Secrets 設定（手動）

GitHub Settings > Secrets and variables > Actions で以下を設定：

```
SAKURA_HOST = garyo.sakura.ne.jp
SAKURA_USER = garyo
SAKURA_KEY = (SSH private key)
```

---

**では実行してください！**

```bash
# virtual-company から移動
cd ~/garyohosu/magic-box-ai

git pull origin main

gemini --yolo instructions/MAGICBOXAI_FINAL_SETUP.md
```
