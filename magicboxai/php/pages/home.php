<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MagicBoxAI - PHP + CGI 版</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: #f0f2f5;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 40px 20px; 
            border-radius: 8px; 
            margin-bottom: 30px; 
            text-align: center;
        }
        header h1 { font-size: 2em; margin-bottom: 10px; }
        header p { opacity: 0.9; }
        .content { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .panel { 
            background: white; 
            padding: 20px; 
            border-radius: 8px; 
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        textarea { 
            width: 100%; 
            height: 400px; 
            padding: 15px; 
            border: 1px solid #ccc; 
            border-radius: 4px; 
            font-family: monospace; 
            font-size: 12px; 
            resize: vertical;
        }
        button { 
            background: #667eea; 
            color: white; 
            padding: 12px 24px; 
            border: none; 
            border-radius: 4px; 
            cursor: pointer; 
            font-size: 14px; 
            margin-top: 10px;
            margin-right: 10px;
        }
        button:hover { background: #764ba2; }
        #preview { 
            width: 100%; 
            height: 400px; 
            border: 1px solid #ccc; 
            border-radius: 4px; 
            background: white; 
            overflow: auto;
        }
        .url-section { 
            margin-top: 20px; 
            padding: 15px; 
            background: #f0f2f5;
            border-radius: 4px; 
            border: 1px solid #ddd; 
            display: none;
        }
        .url-section input { 
            width: 100%; 
            padding: 10px; 
            border: 1px solid #ccc; 
            border-radius: 4px; 
            margin-top: 10px; 
            font-size: 12px;
        }
        .status { 
            margin-top: 10px; 
            padding: 10px; 
            border-radius: 4px; 
            display: none;
        }
        .status.success { 
            background: #d4edda; 
            color: #155724; 
            border: 1px solid #c3e6cb;
        }
        .status.error { 
            background: #f8d7da; 
            color: #721c24; 
            border: 1px solid #f5c6cb;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            color: #666;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎮 MagicBoxAI</h1>
            <p>HTML コードを貼り付けたら、すぐに動作確認</p>
            <p style="font-size: 12px; margin-top: 10px;">Powered by PHP + CGI（Sakura 最適化版）</p>
        </header>
        
        <div class="content">
            <div class="panel">
                <h2>📝 HTML を貼り付け</h2>
                <textarea id="htmlInput" placeholder="<!DOCTYPE html>
<html>
<head>
    <title>My Game</title>
</head>
<body>
    <h1>Hello!</h1>
    <script>alert('Hello World!');</script>
</body>
</html>"></textarea>
                <button onclick="preview()">📺 プレビュー</button>
                <button onclick="saveHtml()">💾 保存</button>
                
                <div id="status" class="status"></div>
            </div>
            
            <div class="panel">
                <h2>🖼️ プレビュー</h2>
                <iframe id="preview" sandbox="allow-scripts" style="width: 100%; height: 400px; border: 1px solid #ccc; border-radius: 4px;"></iframe>
                
                <div class="url-section" id="urlSection">
                    <h3>✅ 保存完了！</h3>
                    <p>このURL を共有してください：</p>
                    <input type="text" id="publicUrl" readonly>
                    <p style="margin-top: 10px; font-size: 12px; color: #666;">
                        30日後に自動削除されます
                    </p>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>MagicBoxAI - HTML ファイルを即座に公開できるサービス</p>
            <p>Sakura レンタルサーバー上で PHP + CGI で実行中</p>
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
                showStatus('❌ HTML を入力してください', 'error');
                return;
            }

            fetch('./index.php/api/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ html: html })
            })
            .then(r => r.json())
            .then(data => {
                if (data.status === 'saved') {
                    showStatus('✅ 保存しました！', 'success');
                    document.getElementById('publicUrl').value = data.public_url;
                    document.getElementById('urlSection').style.display = 'block';
                } else {
                    showStatus('❌ エラー: ' + (data.error || '不明なエラー'), 'error');
                }
            })
            .catch(e => {
                showStatus('❌ ' + e.message, 'error');
            });
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
