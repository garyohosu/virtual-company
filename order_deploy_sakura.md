# Order - Sakura レンタルサーバーへの本番デプロイ

**Status**: ⏳ デプロイ待ち
**Current Actor**: Ops 部門（デプロイ担当）
**Next Actor**: CEO（あなた・note 記事執筆）

---

## 🎯 ミッション

MagicBoxAI を Sakura レンタルサーバーに本番デプロイし、
公開 URL を取得して、note 有料記事での宣伝に備えます。

---

## 📋 デプロイ手順

### Step 1: Sakura サーバー情報確認

デプロイ前に以下を確認：

```
- ホスト名: [あなたの Sakura ホスト名]
- ログイン ID: [あなたの ID]
- パスワード: [あなたのパスワード]
- Python バージョン: 3.9 以上
- FastAPI 対応: Yes
```

### Step 2: リモートサーバーへのデプロイ

#### 2.1: リモートサーバーに SSH で接続

```bash
ssh user@sakura-host.com
```

#### 2.2: プロジェクトをクローン

```bash
cd /home/user/
git clone https://github.com/garyohosu/magic-box-ai.git
cd magic-box-ai
```

#### 2.3: 依存関係をインストール

```bash
python3.9 -m pip install -r requirements.txt
```

または：

```bash
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 2.4: データベース初期化

```bash
python3.9 -m scripts.init_db
```

期待結果：
```
✅ magicboxai.db created
✅ tables initialized
```

#### 2.5: アプリを Gunicorn で実行（Sakura 推奨）

Sakura での推奨起動方法：

```bash
python3.9 -m pip install gunicorn

# ポート 8000 で起動
python3.9 -m gunicorn \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  magicboxai.main:app
```

または、systemd service として登録（推奨・自動起動）：

```bash
sudo tee /etc/systemd/system/magicboxai.service > /dev/null <<EOF
[Unit]
Description=MagicBoxAI FastAPI Service
After=network.target

[Service]
Type=notify
User=user
WorkingDirectory=/home/user/magic-box-ai
ExecStart=/home/user/magic-box-ai/venv/bin/gunicorn \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind unix:/tmp/magicboxai.sock \
  --timeout 120 \
  magicboxai.main:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable magicboxai
sudo systemctl start magicboxai
```

#### 2.6: Nginx リバースプロキシ設定（Sakura 推奨）

```bash
sudo tee /etc/nginx/sites-available/magicboxai > /dev/null <<EOF
server {
    listen 80;
    server_name magicboxai.example.com;

    location / {
        proxy_pass http://unix:/tmp/magicboxai.sock;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/magicboxai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 2.7: SSL 証明書設定（Let's Encrypt）

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d magicboxai.example.com
```

#### 2.8: ファイアウォール設定（必要に応じて）

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

### Step 3: デプロイ検証

#### 3.1: サーバーで HTTP テスト

```bash
# ローカルでテスト
curl http://localhost:8000/api/health
# 期待: {"status": "ok", ...}

curl http://localhost:8000/api/check-limit
# 期待: {"allowed": true, ...}
```

#### 3.2: リモートから HTTP テスト

```bash
# 別マシンから
curl http://magicboxai.example.com/api/health
curl http://magicboxai.example.com/api/check-limit
```

#### 3.3: ログ確認

```bash
# systemd ログ
sudo journalctl -u magicboxai -f

# Nginx ログ
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log
```

---

### Step 4: 本番設定

#### 4.1: 環境変数設定

```bash
# /home/user/magic-box-ai/.env を作成
cat > /home/user/magic-box-ai/.env <<EOF
DATABASE_URL=sqlite:///./magicboxai.db
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')
ENVIRONMENT=production
DEBUG=False
EOF

chmod 600 /home/user/magic-box-ai/.env
```

#### 4.2: バックアップ戦略

```bash
# 日次バックアップスクリプト
cat > /home/user/backup_magicboxai.sh <<'EOF'
#!/bin/bash
BACKUP_DIR="/home/user/backups"
mkdir -p $BACKUP_DIR
tar czf $BACKUP_DIR/magicboxai-$(date +%Y%m%d).tar.gz \
  /home/user/magic-box-ai/magicboxai.db
# 30 日以上前のバックアップを削除
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
EOF

chmod +x /home/user/backup_magicboxai.sh

# Crontab で日次実行
(crontab -l 2>/dev/null; echo "0 2 * * * /home/user/backup_magicboxai.sh") | crontab -
```

#### 4.3: モニタリング設定

```bash
# ログローテーション設定（logrotate）
sudo tee /etc/logrotate.d/magicboxai > /dev/null <<EOF
/var/log/magicboxai/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
EOF
```

---

## 📊 デプロイレポート作成

### `results/ops/SAKURA_DEPLOYMENT_REPORT.md` を生成

```markdown
# Sakura レンタルサーバー デプロイレポート

## デプロイ日時
[実行日時]

## デプロイ情報

### サーバー
- ホスト: [sakura-host.com]
- OS: [Linux版]
- Python: 3.9+
- Web サーバー: Nginx
- アプリケーション: Gunicorn + FastAPI

### 本番 URL
```
https://magicboxai.example.com
```

### API エンドポイント
- /api/health: https://magicboxai.example.com/api/health
- /api/check-limit: https://magicboxai.example.com/api/check-limit
- /api/save: https://magicboxai.example.com/api/save

## デプロイ検証結果

- [x] SSH 接続確認
- [x] Python 環境確認
- [x] 依存関係インストール完了
- [x] DB 初期化完了
- [x] Gunicorn 起動確認
- [x] Nginx リバースプロキシ設定完了
- [x] SSL 証明書設定完了
- [x] /api/health テスト: 200 OK
- [x] /api/check-limit テスト: 200 OK
- [x] ファイアウォール設定完了
- [x] バックアップスクリプト設定完了
- [x] モニタリング設定完了

## 本番状態

✅ **MagicBoxAI は本番環境で稼働中です。**

公開 URL: https://magicboxai.example.com
ステータス: 正常稼働

## 次のステップ

1. ブログで宣伝開始
2. Twitter で告知
3. note で有料記事に本番 URL を記載
4. 販売開始

---

## トラブルシューティング

### エラー: "Connection refused"
→ systemd で magicboxai サービスが起動しているか確認
```bash
sudo systemctl status magicboxai
sudo systemctl restart magicboxai
```

### エラー: "502 Bad Gateway"
→ Gunicorn ログを確認
```bash
sudo journalctl -u magicboxai -f
```

### エラー: SSL 証明書エラー
→ Let's Encrypt 更新
```bash
sudo certbot renew --dry-run
sudo certbot renew
```
```

---

## ✅ 成功基準

すべてが達成されること：

- ✅ Sakura サーバーに SSH 接続
- ✅ magic-box-ai リポジトリをクローン
- ✅ 依存関係をインストール
- ✅ DB 初期化完了
- ✅ Gunicorn + Nginx で起動
- ✅ SSL 証明書設定完了
- ✅ 本番 URL で /api/health が 200 OK
- ✅ 本番 URL で /api/check-limit が 200 OK
- ✅ systemd サービスで自動起動確認
- ✅ デプロイレポート作成・GitHub push

---

## 🎯 本番 URL 例

```
https://magicboxai.example.com
```

この URL を以下で使用：
- ブログ宣伝ページ（garyohosu.github.io）
- note 有料記事
- Twitter ツイート

---

## 🚀 デプロイ完了後

次のステップ：

```bash
git pull
codex --yolo order_note記事執筆.md を実行
```

note 有料記事に本番 URL を記載して、販売開始！

---

**Status**: Sakura デプロイ準備完了
**ユーザーアクション**: Sakura サーバー情報を確認して実行
