# 🔧 MagicBoxAI CRON削除日数を可変化

**作成日**: 2026-01-31  
**優先度**: 🟡 中（UI改善に追加）  
**対象**: magic-box-ai リポジトリ  
**実行方法**: `gemini --yolo instructions/order_magicboxai_cron_variable_days_20260131.md`

---

## 📋 改善内容

### 現在の問題
```php
// cron_cleanup.php Line 8
$maxAge = 30 * 24 * 60 * 60; // 30 days ← 固定値
```

**問題点**:
- 削除日数が30日に固定されている
- 動作確認用に1日で消したい時に対応できない
- 環境ごとに異なる設定ができない

### 改善内容
削除日数を以下の方法で可変化：
1. **環境変数** での指定（推奨）
2. **設定ファイル** での指定
3. **コマンドライン引数** での指定

---

## 🔧 実装方法

### 方法1: 環境変数（推奨）

#### cron_cleanup.php の修正

```php
<?php
/**
 * Auto-delete old files
 * Run via cron: 0 0 * * * /usr/bin/php /path/to/cron_cleanup.php
 * 
 * Environment Variables:
 *   MAGICBOXAI_MAX_AGE_DAYS - Maximum age in days (default: 30)
 * 
 * Example:
 *   MAGICBOXAI_MAX_AGE_DAYS=1 php cron_cleanup.php   # 1日で削除（動作確認用）
 *   MAGICBOXAI_MAX_AGE_DAYS=7 php cron_cleanup.php   # 7日で削除
 *   php cron_cleanup.php                             # 30日で削除（デフォルト）
 */

// エラーログの設定
$logFile = __DIR__ . '/data/cleanup.log';

function logMessage($message, $logFile) {
    $timestamp = date('Y-m-d H:i:s');
    file_put_contents($logFile, "[$timestamp] $message\n", FILE_APPEND);
}

// 設定：削除日数を環境変数から取得（デフォルト30日）
$maxAgeDays = (int)getenv('MAGICBOXAI_MAX_AGE_DAYS');
if ($maxAgeDays <= 0) {
    $maxAgeDays = 30; // デフォルト値
}

$uploadsDir = __DIR__ . '/data/uploads';
$maxAge = $maxAgeDays * 24 * 60 * 60; // 日数を秒に変換
$now = time();

logMessage("INFO: Starting cleanup. Max age: $maxAgeDays days", $logFile);

// ディレクトリ存在チェック
if (!is_dir($uploadsDir)) {
    logMessage("ERROR: Uploads directory not found: $uploadsDir", $logFile);
    echo "ERROR: Uploads directory not found\n";
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
        
        $ageInSeconds = $now - $mtime;
        $ageInDays = round($ageInSeconds / (24 * 60 * 60), 1);
        
        // 有効期限チェック
        if ($ageInSeconds > $maxAge) {
            if (unlink($file)) {
                logMessage("INFO: Deleted: $file (age: $ageInDays days)", $logFile);
                echo "Deleted: $file (age: $ageInDays days)\n";
                $deletedCount++;
            } else {
                logMessage("ERROR: Failed to delete: $file", $logFile);
                echo "ERROR: Failed to delete: $file\n";
                $errorCount++;
            }
        } else {
            // デバッグ用：残り日数を表示
            $remainingDays = round(($maxAge - $ageInSeconds) / (24 * 60 * 60), 1);
            echo "Skipped: $file (age: $ageInDays days, remaining: $remainingDays days)\n";
        }
    } catch (Exception $e) {
        logMessage("ERROR: Exception while processing $file: " . $e->getMessage(), $logFile);
        echo "ERROR: Exception for $file: " . $e->getMessage() . "\n";
        $errorCount++;
    }
}

logMessage("INFO: Cleanup complete. Max age: $maxAgeDays days, Deleted: $deletedCount, Errors: $errorCount", $logFile);
echo "\nCleanup complete.\n";
echo "Max age: $maxAgeDays days\n";
echo "Deleted: $deletedCount files\n";
echo "Errors: $errorCount\n";

exit($errorCount > 0 ? 1 : 0);
?>
```

#### 使用方法

```bash
# デフォルト（30日）
php cron_cleanup.php

# 動作確認用（1日）
MAGICBOXAI_MAX_AGE_DAYS=1 php cron_cleanup.php

# 7日で削除
MAGICBOXAI_MAX_AGE_DAYS=7 php cron_cleanup.php

# Cronに設定（環境変数付き）
# crontab -e
0 0 * * * MAGICBOXAI_MAX_AGE_DAYS=1 /usr/bin/php /path/to/cron_cleanup.php
```

---

### 方法2: 設定ファイル

#### config.php の作成

```php
<?php
/**
 * MagicBoxAI Configuration
 */

return [
    // 削除日数設定
    'max_age_days' => 30,  // デフォルト30日
    
    // 環境別設定
    'development' => [
        'max_age_days' => 1,  // 開発環境は1日
    ],
    'production' => [
        'max_age_days' => 30, // 本番環境は30日
    ],
];
?>
```

#### cron_cleanup.php で読み込み

```php
<?php
// 設定ファイルの読み込み
$config = include __DIR__ . '/config.php';

// 環境の判定（環境変数 APP_ENV で切り替え）
$env = getenv('APP_ENV') ?: 'production';

// 削除日数の取得
if (isset($config[$env]['max_age_days'])) {
    $maxAgeDays = $config[$env]['max_age_days'];
} else {
    $maxAgeDays = $config['max_age_days'];
}

echo "Environment: $env\n";
echo "Max age: $maxAgeDays days\n";

$maxAge = $maxAgeDays * 24 * 60 * 60;
// ... 以下同じ
?>
```

#### 使用方法

```bash
# 本番環境（30日）
APP_ENV=production php cron_cleanup.php

# 開発環境（1日）
APP_ENV=development php cron_cleanup.php
```

---

### 方法3: コマンドライン引数

#### cron_cleanup.php の修正

```php
<?php
/**
 * Auto-delete old files
 * 
 * Usage:
 *   php cron_cleanup.php          # デフォルト30日
 *   php cron_cleanup.php 1        # 1日で削除
 *   php cron_cleanup.php 7        # 7日で削除
 *   php cron_cleanup.php --days=1 # オプション形式
 */

// コマンドライン引数の解析
$maxAgeDays = 30; // デフォルト

if (isset($argv[1])) {
    if (strpos($argv[1], '--days=') === 0) {
        // --days=1 形式
        $maxAgeDays = (int)substr($argv[1], 7);
    } else {
        // 数値のみ
        $maxAgeDays = (int)$argv[1];
    }
}

// 検証
if ($maxAgeDays <= 0) {
    echo "ERROR: Invalid days: $maxAgeDays\n";
    exit(1);
}

echo "Max age: $maxAgeDays days\n";

$maxAge = $maxAgeDays * 24 * 60 * 60;
// ... 以下同じ
?>
```

#### 使用方法

```bash
# デフォルト（30日）
php cron_cleanup.php

# 1日で削除
php cron_cleanup.php 1

# 7日で削除
php cron_cleanup.php --days=7
```

---

## 🎯 推奨実装：方法1（環境変数）

**理由**:
1. ✅ シンプルで分かりやすい
2. ✅ Cronで簡単に設定可能
3. ✅ 設定ファイルの管理不要
4. ✅ 環境ごとに柔軟に変更可能

---

## 📝 UI側の表示も更新

### index.php の修正

現在の表示：
```html
<p class="text-gray-500 text-sm mb-4">
    ※ 30日後に自動で削除されます
</p>
```

修正後（動的表示）：
```php
<?php
// 削除日数を取得（環境変数またはデフォルト）
$maxAgeDays = (int)getenv('MAGICBOXAI_MAX_AGE_DAYS');
if ($maxAgeDays <= 0) {
    $maxAgeDays = 30; // デフォルト
}
?>

<!-- HTML表示 -->
<p class="text-gray-500 text-sm mb-4">
    ※ <?php echo $maxAgeDays; ?>日後に自動で削除されます
</p>
```

または、JavaScriptで動的に表示：
```javascript
// APIエンドポイントで設定を取得
fetch('./index.php/api/config')
    .then(r => r.json())
    .then(data => {
        const days = data.max_age_days || 30;
        document.getElementById('deleteWarning').textContent = 
            `※ ${days}日後に自動で削除されます`;
    });
```

---

## 🔧 実装手順

### Step 1: cron_cleanup.php を更新

```bash
cd ~/garyohosu/magic-box-ai
git checkout -b cron-variable-days

# ファイルを編集（上記の方法1を実装）
nano src/cron_cleanup.php

# UTF-8 BOM も同時に削除
sed -i '1s/^\xEF\xBB\xBF//' src/cron_cleanup.php
```

### Step 2: テスト実行

```bash
# デフォルト（30日）
cd src
php cron_cleanup.php

# 1日で削除（動作確認用）
MAGICBOXAI_MAX_AGE_DAYS=1 php cron_cleanup.php

# 7日で削除
MAGICBOXAI_MAX_AGE_DAYS=7 php cron_cleanup.php
```

### Step 3: index.php を更新

```bash
# index.php を編集
nano src/index.php

# 削除日数の動的表示を追加
```

### Step 4: Cron設定を更新

```bash
# Sakuraサーバーでcrontab編集
crontab -e

# 本番環境（30日）
0 0 * * * /usr/bin/php /path/to/magicboxai/src/cron_cleanup.php >> /path/to/magicboxai/src/data/cron.log 2>&1

# 動作確認環境（1日）
0 0 * * * MAGICBOXAI_MAX_AGE_DAYS=1 /usr/bin/php /path/to/magicboxai/src/cron_cleanup.php >> /path/to/magicboxai/src/data/cron.log 2>&1
```

### Step 5: コミット＆プッシュ

```bash
git add src/cron_cleanup.php src/index.php
git commit -m "feat: Make CRON deletion days variable

- Add MAGICBOXAI_MAX_AGE_DAYS environment variable
- Default: 30 days
- Configurable for testing (e.g., 1 day)
- Improve error handling and logging
- Display deletion days dynamically in UI
- Remove UTF-8 BOM"

git push origin cron-variable-days

# PR作成
gh pr create \
  --title "feat: Make CRON deletion days variable" \
  --body "## 🔧 削除日数の可変化

### 改善内容
- 環境変数 \`MAGICBOXAI_MAX_AGE_DAYS\` で削除日数を指定可能
- デフォルト: 30日
- 動作確認用に1日で削除可能

### 使用方法
\`\`\`bash
# デフォルト（30日）
php cron_cleanup.php

# 1日で削除
MAGICBOXAI_MAX_AGE_DAYS=1 php cron_cleanup.php

# 7日で削除
MAGICBOXAI_MAX_AGE_DAYS=7 php cron_cleanup.php
\`\`\`

### UI側の改善
- 削除日数を動的に表示
- 環境に応じて自動で切り替わる" \
  --base main \
  --head cron-variable-days
```

---

## ✅ テストケース

### テスト1: デフォルト動作（30日）
```bash
# 実行
php cron_cleanup.php

# 期待結果
Max age: 30 days
Deleted: 0 files (新規ファイルは削除されない)
```

### テスト2: 1日で削除（動作確認用）
```bash
# 31日前のテストファイルを作成
touch -t 202412010000 test_old.html

# 実行
MAGICBOXAI_MAX_AGE_DAYS=1 php cron_cleanup.php

# 期待結果
Max age: 1 days
Deleted: 1 file (test_old.html)
```

### テスト3: エラーハンドリング
```bash
# 不正な値
MAGICBOXAI_MAX_AGE_DAYS=0 php cron_cleanup.php
# → デフォルト30日にフォールバック

MAGICBOXAI_MAX_AGE_DAYS=-1 php cron_cleanup.php
# → デフォルト30日にフォールバック
```

---

## 📊 実装後の動作

### 本番環境
```bash
# Cron設定
0 0 * * * /usr/bin/php /path/to/cron_cleanup.php
# → 30日で自動削除
```

### 動作確認環境
```bash
# Cron設定
0 */6 * * * MAGICBOXAI_MAX_AGE_DAYS=1 /usr/bin/php /path/to/cron_cleanup.php
# → 6時間ごとに実行、1日で削除
```

### ローカル開発環境
```bash
# 手動実行
MAGICBOXAI_MAX_AGE_DAYS=1 php cron_cleanup.php
# → すぐにテスト可能
```

---

## 🎨 UI表示例

### 本番環境（30日）
```
✅ 保存完了！
このURLを共有してください：
https://garyo.sakura.ne.jp/magicboxai/view/xxxxx
[コピー] [開く] [ZIPで渡す]

⚠️ 30日後に自動削除されます
```

### 動作確認環境（1日）
```
✅ 保存完了！
このURLを共有してください：
https://garyo.sakura.ne.jp/magicboxai/view/xxxxx
[コピー] [開く] [ZIPで渡す]

⚠️ 1日後に自動削除されます（動作確認モード）
```

---

## 📝 ドキュメント更新

### README.md に追加

```markdown
## 環境変数

| 変数名 | 説明 | デフォルト値 | 例 |
|--------|------|--------------|-----|
| `MAGICBOXAI_MAX_AGE_DAYS` | ファイルの自動削除日数 | 30 | `1`, `7`, `30` |

## 自動削除の設定

### 本番環境（30日）
```bash
# Cron設定
0 0 * * * /usr/bin/php /path/to/cron_cleanup.php
```

### 動作確認環境（1日）
```bash
# Cron設定
0 0 * * * MAGICBOXAI_MAX_AGE_DAYS=1 /usr/bin/php /path/to/cron_cleanup.php
```

### 手動実行
```bash
# 1日で削除
MAGICBOXAI_MAX_AGE_DAYS=1 php cron_cleanup.php

# 7日で削除
MAGICBOXAI_MAX_AGE_DAYS=7 php cron_cleanup.php
```
```

---

## 🎯 まとめ

### 改善点
- ✅ 削除日数が可変になった
- ✅ 動作確認が容易になった
- ✅ 環境ごとに設定を変更可能
- ✅ UI側も動的に表示される
- ✅ エラーハンドリングが改善された
- ✅ ログが充実した

### 使い分け

| 環境 | 設定日数 | 用途 |
|------|----------|------|
| 本番環境 | 30日 | 通常運用 |
| ステージング | 7日 | 中期テスト |
| 開発環境 | 1日 | 動作確認 |
| ローカル | 1時間 | デバッグ（将来の拡張） |

---

**このファイルを実行**:
```bash
cd ~/garyohosu/virtual-company
git pull origin main
gemini --yolo instructions/order_magicboxai_cron_variable_days_20260131.md
```

---

**Status**: 準備完了  
**Priority**: 🟡 中  
**Current Actor**: Gemini  
**Next Actor**: User（動作確認）  
**Created At**: 2026-01-31
