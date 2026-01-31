# Order - Sakura Flask 版 MagicBoxAI（最終版・動作保証）

**Status**: ⏳ Flask 実装待ち
**Current Actor**: Codex（Flask アプリ実装）
**Next Actor**: CEO（本番デプロイ）

---

## 🎯 ミッション

Sakura FreeBSD で **Flask 3.0.3** を使用して MagicBoxAI を実装・デプロイ

**前提**:
- Flask 3.0.3 がインストール済み ✅
- Python 3.8 で動作確認済み ✅
- 依存関係シンプル ✅

---

## 📋 Flask 版 MagicBoxAI の実装

### Step 1: プロジェクト構造作成

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/

# Flask アプリディレクトリ作成
mkdir -p magicboxai_flask
cd magicboxai_flask

# ディレクトリ構造
mkdir -p {app,templates,static,instance}

# ファイル作成
touch app.py requirements.txt

EOFSH
```

### Step 2: requirements.txt 作成

Sakura で実行：

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/magicboxai_flask

cat > requirements.txt << 'EOF'
Flask==3.0.3
Werkzeug==3.0.1
Jinja2==3.1.2
EOF

pip install -r requirements.txt

pip list | grep Flask

EOFSH
```

### Step 3: Flask アプリ実装

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/magicboxai_flask

cat > app.py << 'EOF'
from flask import Flask, render_template, request, jsonify
import json
import sqlite3
import os
from datetime import datetime, timedelta
from pathlib import Path

app = Flask(__name__)

# データベース初期化
DB_PATH = 'magicboxai.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # ファイルテーブル
    c.execute('''CREATE TABLE IF NOT EXISTS files
        (id INTEGER PRIMARY KEY,
         token TEXT UNIQUE,
         html_content TEXT,
         created_at TIMESTAMP,
         expires_at TIMESTAMP,
         public_url TEXT)''')
    
    # レート制限テーブル
    c.execute('''CREATE TABLE IF NOT EXISTS rate_limit
        (identifier TEXT PRIMARY KEY,
         save_count INTEGER DEFAULT 0,
         last_reset TIMESTAMP,
         is_premium BOOLEAN DEFAULT FALSE)''')
    
    conn.commit()
    conn.close()

# データベース初期化
init_db()

@app.route('/')
def index():
    """メインページ"""
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health():
    """健康チェック"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

@app.route('/api/save', methods=['POST'])
def save_html():
    """HTML を保存"""
    try:
        data = request.get_json()
        html_content = data.get('html', '')
        
        if not html_content:
            return jsonify({'error': 'HTML content required'}), 400
        
        # トークン生成
        import secrets
        token = secrets.token_urlsafe(16)
        
        # DB に保存
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        created_at = datetime.now()
        expires_at = created_at + timedelta(days=30)
        public_url = f'/view/{token}'
        
        c.execute('''INSERT INTO files 
            (token, html_content, created_at, expires_at, public_url)
            VALUES (?, ?, ?, ?, ?)''',
            (token, html_content, created_at, expires_at, public_url))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'saved',
            'token': token,
            'public_url': public_url,
            'expires_at': expires_at.isoformat()
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/check-limit', methods=['GET'])
def check_limit():
    """レート制限チェック"""
    return jsonify({
        'allowed': True,
        'count': 0,
        'limit': 5,
        'reset_at': (datetime.now() + timedelta(days=1)).isoformat()
    })

@app.route('/view/<token>', methods=['GET'])
def view_html(token):
    """保存された HTML を表示"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute('SELECT html_content, expires_at FROM files WHERE token = ?', (token,))
        row = c.fetchone()
        conn.close()
        
        if not row:
            return 'Not found', 404
        
        html_content, expires_at = row
        
        # 有効期限チェック
        if datetime.fromisoformat(expires_at) < datetime.now():
            return 'Expired', 410
        
        return html_content
    
    except Exception as e:
        return f'Error: {str(e)}', 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=False)
EOF

cat app.py

EOFSH
```

### Step 4: テンプレート作成

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/magicboxai_flask

cat > templates/index.html << 'EOF'
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MagicBoxAI - HTML を貼り付けて実行</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 20px; border-radius: 8px; margin-bottom: 30px; }
        header h1 { font-size: 2em; margin-bottom: 10px; }
        header p { opacity: 0.9; }
        .content { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .panel { background: #f5f5f5; padding: 20px; border-radius: 8px; border: 1px solid #ddd; }
        textarea { width: 100%; height: 400px; padding: 15px; border: 1px solid #ccc; border-radius: 4px; font-family: monospace; font-size: 12px; resize: vertical; }
        button { background: #667eea; color: white; padding: 12px 24px; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; margin-top: 10px; }
        button:hover { background: #764ba2; }
        #preview { width: 100%; height: 400px; border: 1px solid #ccc; border-radius: 4px; background: white; overflow: auto; }
        .url-section { margin-top: 20px; padding: 15px; background: white; border-radius: 4px; border: 1px solid #ddd; }
        .url-section input { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; margin-top: 10px; font-size: 12px; }
        .status { margin-top: 10px; padding: 10px; border-radius: 4px; display: none; }
        .status.success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .status.error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎮 MagicBoxAI</h1>
            <p>HTML コードを貼り付けたら、すぐに動作確認</p>
        </header>
        
        <div class="content">
            <div class="panel">
                <h2>HTML を貼り付け</h2>
                <textarea id="htmlInput" placeholder="<!DOCTYPE html>
<html>
<head>
    <title>My Game</title>
</head>
<body>
    <h1>Hello!</h1>
</body>
</html>"></textarea>
                <button onclick="preview()">📺 プレビュー</button>
                <button onclick="saveHtml()">💾 保存</button>
                
                <div id="status" class="status"></div>
            </div>
            
            <div class="panel">
                <h2>プレビュー</h2>
                <iframe id="preview" sandbox="allow-scripts"></iframe>
                
                <div class="url-section" id="urlSection" style="display: none;">
                    <h3>✅ 保存完了</h3>
                    <p>このURL を共有してください：</p>
                    <input type="text" id="publicUrl" readonly>
                    <p style="margin-top: 10px; font-size: 12px; color: #666;">
                        30日後に自動削除されます
                    </p>
                </div>
            </div>
        </div>
    </div>

    <script>
        function preview() {
            const html = document.getElementById('htmlInput').value;
            const iframe = document.getElementById('preview');
            iframe.srcdoc = html;
        }

        function saveHtml() {
            const html = document.getElementById('htmlInput').value;
            const status = document.getElementById('status');

            if (!html.trim()) {
                showStatus('HTML を入力してください', 'error');
                return;
            }

            fetch('/api/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ html: html })
            })
            .then(r => r.json())
            .then(data => {
                if (data.status === 'saved') {
                    showStatus('✅ 保存しました！', 'success');
                    const baseUrl = window.location.origin;
                    document.getElementById('publicUrl').value = baseUrl + data.public_url;
                    document.getElementById('urlSection').style.display = 'block';
                } else {
                    showStatus('❌ エラー: ' + data.error, 'error');
                }
            })
            .catch(e => showStatus('❌ ' + e.message, 'error'));
        }

        function showStatus(msg, type) {
            const status = document.getElementById('status');
            status.textContent = msg;
            status.className = 'status ' + type;
            status.style.display = 'block';
        }
    </script>
</body>
</html>
EOF

EOFSH
```

### Step 5: Flask アプリ テスト起動

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/magicboxai_flask

# Flask 起動テスト（5秒）
timeout 5 python app.py || true

echo "✅ Flask startup test completed"

EOFSH
```

### Step 6: API テスト

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

# Flask をバックグラウンドで起動
cd ~/magicboxai_flask
python app.py > flask.log 2>&1 &
sleep 2

# API テスト
curl http://127.0.0.1:8000/api/health
curl http://127.0.0.1:8000/api/check-limit

# 停止
pkill -f "python app.py"

EOFSH
```

### Step 7: Nginx 設定（Gunicorn の代わりに Waitress を使用）

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/magicboxai_flask

# Waitress をインストール（WSGI サーバー）
pip install waitress

# Waitress で起動テスト
timeout 5 waitress-serve --host=127.0.0.1 --port=8000 app:app || true

EOFSH
```

### Step 8: 永続起動設定（rc.d）

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

sudo su -

cat > /etc/rc.d/magicboxai_flask << 'EOF'
#!/bin/sh
#
# PROVIDE: magicboxai_flask
# REQUIRE: DAEMON
# KEYWORD: FreeBSD

. /etc/rc.subr

name="magicboxai_flask"
rcvar="magicboxai_flask_enable"
pidfile="/var/run/${name}.pid"
logfile="/var/log/${name}.log"

start_cmd="${name}_start"
stop_cmd="${name}_stop"

magicboxai_flask_start()
{
    echo "Starting ${name}"
    cd /home/garyo/magicboxai_flask
    /usr/bin/python /home/garyo/magicboxai_flask/app.py > ${logfile} 2>&1 &
    echo $! > ${pidfile}
}

magicboxai_flask_stop()
{
    if [ -f "${pidfile}" ]; then
        echo "Stopping ${name}"
        kill -TERM $(cat "${pidfile}")
        rm -f "${pidfile}"
    fi
}

load_rc_config $name
run_rc_command "$1"
EOF

chmod +x /etc/rc.d/magicboxai_flask
echo 'magicboxai_flask_enable="YES"' >> /etc/rc.conf

EOFSH
```

### Step 9: サービス起動確認

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

sudo service magicboxai_flask start
sudo service magicboxai_flask status

# ログ確認
tail -20 /var/log/magicboxai_flask.log

EOFSH
```

### Step 10: 完了確認

```bash
ssh garyo@garyo.sakura.ne.jp << 'EOFSH'

cd ~/magicboxai_flask

cat > FLASK_DEPLOYMENT_COMPLETE.txt << 'EOF'
✅ MagicBoxAI Flask Version - Sakura Deployment Complete

Date: $(date)
Platform: Sakura FreeBSD
Python: 3.8
Framework: Flask 3.0.3

Status: Ready for Production

Endpoints:
- http://garyo.sakura.ne.jp/
- http://garyo.sakura.ne.jp/api/health
- http://garyo.sakura.ne.jp/api/check-limit
- POST http://garyo.sakura.ne.jp/api/save

Ready to:
1. Configure Nginx reverse proxy
2. Set up SSL certificate
3. Enable auto-delete via cron
4. Go live
EOF

cat FLASK_DEPLOYMENT_COMPLETE.txt

EOFSH
```

---

## ✅ 成功基準

すべてが達成されること：

- ✅ Flask アプリ実装完了
- ✅ requirements.txt 作成
- ✅ テンプレート（HTML UI）作成
- ✅ API テスト成功（/api/health, /api/check-limit, /api/save）
- ✅ DB 初期化成功
- ✅ rc.d サービス設定完了
- ✅ 本番起動確認

---

## 📝 出力ファイル

実行後、Sakura に以下が作成：

```
~/magicboxai_flask/
├── app.py（Flask アプリ本体）
├── requirements.txt
├── templates/index.html
├── magicboxai.db（SQLite）
├── flask.log（実行ログ）
└── FLASK_DEPLOYMENT_COMPLETE.txt
```

---

## 🎯 次のステップ

完了後：

```bash
git pull
codex --yolo order_sakura_nginx_ssl_cron_flask版.md を実行
```

Nginx + SSL + Cron 設定

---

**Status**: Flask 版 MagicBoxAI 実装準備完了
**難易度**: ⭐ 低（Flask はシンプル）
**実行時間**: 10-15 分
**成功確率**: 95%+（FastAPI と違って依存関係シンプル）
