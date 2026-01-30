# Order - Sakura FreeBSD 本番デプロイ（修正版）

**Status**: ⏳ デプロイ待ち
**Current Actor**: Ops 部門
**Next Actor**: CEO（note 記事執筆）

---

## 🎯 ミッション

MagicBoxAI を **Sakura FreeBSD** サーバーに本番デプロイします。

**注意**: Sakura は FreeBSD です。Linux とは異なります。

---

## 📋 FreeBSD デプロイ手順

### Step 1: SSH 接続（完了）✅

```bash
ssh garyo@garyo.sakura.ne.jp
```

### Step 2: FreeBSD 環境確認

```bash
uname -a
# FreeBSD 13.0-RELEASE-p14

python3 --version
# Python 3.x.x が必要（3.9 以上）

pip3 --version
```

### Step 3: プロジェクトをクローン

```bash
cd ~
git clone https://github.com/garyohosu/magic-box-ai.git
cd magic-box-ai
```

### Step 4: Python 仮想環境作成

```bash
python3 -m venv venv
source venv/bin/activate

# 仮想環境有効化確認
which python
# /home/garyo/magic-box-ai/venv/bin/python と表示される
```

### Step 5: 依存関係インストール

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

期待結果：
```
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 ...
```

### Step 6: データベース初期化

```bash
python -m scripts.init_db
```

期待結果：
```
✅ Database initialized
✅ Tables created
```

### Step 7: Gunicorn インストール

```bash
pip install gunicorn
```

### Step 8: Gunicorn + Uvicorn テスト起動

```bash
gunicorn \
  --workers 2 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 127.0.0.1:8000 \
  magicboxai.main:app
```

別ターミナルで：
```bash
ssh garyo@garyo.sakura.ne.jp

# ローカルホストでテスト
curl http://127.0.0.1:8000/api/health
# 期待: {"status":"ok",...}

# 元のターミナルで Ctrl+C で停止
```

---

## 🔧 FreeBSD での永続起動（rc.d サービス）

### Step 9: rc.d スクリプト作成

Sakura では `systemd` ではなく `rc.d` を使います。

```bash
# スーパーユーザーで実行（またはsudo を使用）
sudo su -

# スクリプト作成
cat > /etc/rc.d/magicboxai << 'EOF'
#!/bin/sh
#
# PROVIDE: magicboxai
# REQUIRE: DAEMON
# KEYWORD: FreeBSD

. /etc/rc.subr

name="magicboxai"
rcvar="magicboxai_enable"
pidfile="/var/run/${name}.pid"
logfile="/var/log/${name}.log"

start_cmd="${name}_start"
stop_cmd="${name}_stop"
status_cmd="${name}_status"

magicboxai_start()
{
    echo "Starting ${name}"
    cd /home/garyo/magic-box-ai
    /home/garyo/magic-box-ai/venv/bin/gunicorn \
        --workers 2 \
        --worker-class uvicorn.workers.UvicornWorker \
        --bind unix:/tmp/magicboxai.sock \
        --user garyo \
        --group wheel \
        --pid ${pidfile} \
        --error-logfile ${logfile} \
        --access-logfile - \
        magicboxai.main:app &
}

magicboxai_stop()
{
    if [ -f "${pidfile}" ]; then
        echo "Stopping ${name}"
        kill -TERM $(cat "${pidfile}")
        rm -f "${pidfile}"
    fi
}

magicboxai_status()
{
    if [ -f "${pidfile}" ]; then
        echo "${name} is running with PID $(cat ${pidfile})"
    else
        echo "${name} is not running"
    fi
}

load_rc_config $name
run_rc_command "$1"
EOF

chmod +x /etc/rc.d/magicboxai
```

### Step 10: /etc/rc.conf に追加

```bash
echo 'magicboxai_enable="YES"' >> /etc/rc.conf
```

### Step 11: サービス起動テスト

```bash
service magicboxai start
# Starting magicboxai

service magicboxai status
# magicboxai is running with PID [number]

# ログ確認
tail -f /var/log/magicboxai.log
```

---

## 🌐 Nginx リバースプロキシ設定

### Step 12: Nginx 設定ファイル作成

```bash
sudo su -

cat > /usr/local/etc/nginx/sites-available/magicboxai.conf << 'EOF'
server {
    listen 80;
    server_name garyo.sakura.ne.jp;

    location / {
        proxy_pass http://unix:/tmp/magicboxai.sock;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
        proxy_connect_timeout 120s;
    }

    # 健康チェックエンドポイント
    location /api/health {
        access_log off;
        proxy_pass http://unix:/tmp/magicboxai.sock;
    }
}
EOF

# シンボリックリンク作成
mkdir -p /usr/local/etc/nginx/sites-enabled
ln -s /usr/local/etc/nginx/sites-available/magicboxai.conf \
      /usr/local/etc/nginx/sites-enabled/magicboxai.conf
```

### Step 13: Nginx テスト・起動

```bash
# 設定ファイルテスト
nginx -t
# nginx: the configuration file /usr/local/etc/nginx/nginx.conf syntax is ok

# Nginx 起動
service nginx start

# または既に起動している場合
service nginx restart
```

---

## 🔐 SSL 設定（Let's Encrypt）

### Step 14: Certbot のインストール（FreeBSD）

```bash
sudo su -

# pkg で certbot をインストール
pkg install certbot

# Nginx プラグインもインストール
pkg install py39-certbot-nginx
```

### Step 15: SSL 証明書取得

```bash
certbot certonly --nginx -d garyo.sakura.ne.jp
```

プロンプトに従って：
- メールアドレス入力
- 利用規約に同意
- 証明書取得

期待結果：
```
Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/garyo.sakura.ne.jp/fullchain.pem
```

### Step 16: Nginx 設定を HTTPS 対応に更新

```bash
cat > /usr/local/etc/nginx/sites-available/magicboxai.conf << 'EOF'
# HTTP → HTTPS リダイレクト
server {
    listen 80;
    server_name garyo.sakura.ne.jp;
    return 301 https://$server_name$request_uri;
}

# HTTPS サーバー
server {
    listen 443 ssl http2;
    server_name garyo.sakura.ne.jp;

    ssl_certificate /etc/letsencrypt/live/garyo.sakura.ne.jp/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/garyo.sakura.ne.jp/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://unix:/tmp/magicboxai.sock;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_read_timeout 120s;
        proxy_connect_timeout 120s;
    }
}
EOF

nginx -t
service nginx restart
```

---

## 📊 デプロイ完了確認

### Step 17: エンドポイント テスト

```bash
# ローカルテスト
curl http://127.0.0.1:8000/api/health
curl http://127.0.0.1:8000/api/check-limit

# HTTPS でテスト
curl https://garyo.sakura.ne.jp/api/health
curl https://garyo.sakura.ne.jp/api/check-limit
```

期待結果：
```
{"status":"ok",...}
{"allowed":true,...}
```

### Step 18: ログ確認

```bash
# Gunicorn ログ
tail -f /var/log/magicboxai.log

# Nginx ログ
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

---

## 🔄 定期タスク（ファイル自動削除）

### Step 19: Cron ジョブ設定

FreeBSD では `crontab` を使用：

```bash
# crontab -e で編集
crontab -e

# 以下を追加（毎日午前 2 時に実行）
0 2 * * * cd /home/garyo/magic-box-ai && /home/garyo/magic-box-ai/venv/bin/python -c "from scripts.cleanup_expired import cleanup; cleanup()" >> /var/log/magicboxai-cleanup.log 2>&1
```

---

## 📝 デプロイレポート作成

`results/ops/SAKURA_FREEBSD_DEPLOYMENT_REPORT.md` を生成：

```markdown
# Sakura FreeBSD デプロイ完了レポート

## デプロイ日時
[実行日時]

## サーバー情報
- OS: FreeBSD 13.0-RELEASE-p14
- ホスト: garyo.sakura.ne.jp
- Python: 3.x
- Web: Nginx
- App: Gunicorn + FastAPI

## 本番 URL
```
https://garyo.sakura.ne.jp
```

## API エンドポイント
- /api/health: https://garyo.sakura.ne.jp/api/health
- /api/check-limit: https://garyo.sakura.ne.jp/api/check-limit
- /api/save: https://garyo.sakura.ne.jp/api/save

## デプロイ検証結果
- [x] SSH 接続確認
- [x] Python 仮想環境作成
- [x] 依存関係インストール完了
- [x] DB 初期化完了
- [x] Gunicorn テスト起動成功
- [x] rc.d サービス設定完了
- [x] Nginx リバースプロキシ設定完了
- [x] SSL 証明書取得完了
- [x] /api/health テスト: 200 OK
- [x] /api/check-limit テスト: 200 OK
- [x] Cron で自動削除ジョブ設定完了

## 本番状態

✅ **MagicBoxAI は本番環境で稼働中です。**

公開 URL: https://garyo.sakura.ne.jp
ステータス: 正常稼働

## 次のステップ
1. ブログで宣伝開始
2. Twitter で告知
3. note で有料記事に本番 URL を記載
4. 販売開始
```

---

## ✅ 成功基準

- ✅ SSH 接続確認
- ✅ git clone 完了
- ✅ Python 仮想環境作成
- ✅ 依存関係インストール
- ✅ DB 初期化
- ✅ Gunicorn テスト起動
- ✅ rc.d サービス起動
- ✅ Nginx 設定完了
- ✅ SSL 証明書取得
- ✅ https://garyo.sakura.ne.jp で稼働確認
- ✅ デプロイレポート作成・GitHub push

---

**Status**: FreeBSD デプロイ準備完了
**ユーザーアクション**: Sakura サーバーで上記コマンドを実行
