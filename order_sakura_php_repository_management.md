# Order - Sakura PHP ファイルをリポジトリで一元管理

**Status**: ⏳ ファイル整理待ち
**Current Actor**: Gemini CLI
**Goal**: Sakura の PHP ファイルを garyohosu/magic-box-ai で管理
**Output**: PHP ファイルを garyohosu/magic-box-ai に追加・整理

---

## 🎯 ミッション

### 目標 1: Sakura の PHP ファイルを確認・取得

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

echo "=== Sakura PHP ファイル一覧 ==="
find ~/www/magicboxai -type f | sort

echo ""
echo "=== ファイル詳細 ==="
ls -lah ~/www/magicboxai/

echo ""
echo "=== PHP ファイル内容確認 ==="
echo "--- index.php ---"
head -30 ~/www/magicboxai/index.php

echo ""
echo "--- pages/home.php ---"
head -30 ~/www/magicboxai/pages/home.php

echo ""
echo "--- .htaccess ---"
cat ~/www/magicboxai/.htaccess

EOFSH
```

### 目標 2: 確認内容をレポート出力

```
results/maintenance/SAKURA_PHP_FILES_AUDIT.md に以下を記載：

1. Sakura に現在存在する PHP ファイル一覧
2. 各ファイルの内容・役割
3. 管理状態の確認
4. garyohosu/magic-box-ai との同期状態
```

### 目標 3: リポジトリ整理計画

```
現状：
- virtual-company リポジトリ
  - magicboxai/ (Python/FastAPI)
  - magicboxai/php/ (PHP ファイル？)

目標：
- virtual-company リポジトリ
  - magicboxai/ (Python/FastAPI) ← 削除予定
  
- garyohosu/magic-box-ai リポジトリ（新）
  - magicboxai/
    ├── index.php
    ├── pages/
    ├── data/
    ├── cgi-bin/
    ├── .htaccess
    └── README.md
```

---

## 📋 実行スクリプト

```bash
# Step 1: 確認用スクリプト
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cat > /tmp/sakura_php_audit.md << 'EOF'
# Sakura PHP ファイル監査レポート

**実行日時**: $(date)

---

## 1. PHP ファイル一覧

\`\`\`
$(find ~/www/magicboxai -type f | sort)
\`\`\`

---

## 2. ファイル詳細（ls -la）

\`\`\`
$(ls -lah ~/www/magicboxai/)
\`\`\`

---

## 3. 主要ファイルの内容確認

### index.php

\`\`\`php
$(head -40 ~/www/magicboxai/index.php)
\`\`\`

### pages/home.php

\`\`\`php
$(head -40 ~/www/magicboxai/pages/home.php)
\`\`\`

### .htaccess

\`\`\`
$(cat ~/www/magicboxai/.htaccess)
\`\`\`

---

## 4. 管理状態

現在、これらのファイルは以下の場所にあります：
- 物理ファイル: ~/www/magicboxai/ （Sakura サーバー）
- バージョン管理: ??? （確認が必要）

**推奨**: garyohosu/magic-box-ai リポジトリで一元管理

EOF

cat /tmp/sakura_php_audit.md

EOFSH
```

---

## 🎯 期待される結果

```
このスクリプトで：

1️⃣ Sakura に現在ある PHP ファイルを確認
2️⃣ 各ファイルの内容を把握
3️⃣ 管理されていないファイルを特定
4️⃣ リポジトリ化の計画を立てる

→ 次に、これらを garyohosu/magic-box-ai にアップロード
```

---

## ✅ 成功基準

- ✅ Sakura の PHP ファイルが全て確認できる
- ✅ 各ファイルの役割が明確
- ✅ 管理状態が把握できる
- ✅ garyohosu/magic-box-ai への移行計画が立てられる

---

**Status**: Sakura PHP ファイル監査実施中

次のステップ：
1. このスクリプト実行
2. 結果を確認
3. garyohosu/magic-box-ai リポジトリ構成を決定
4. PHP ファイルを GitHub に追加
5. virtual-company の Python コード削除
