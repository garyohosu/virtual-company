# Order - MagicBoxAI Development (with Auto Error Capture)

**Status**: ⏳ Waiting for development
**Current Actor**: codex
**Next Actor**: (complete when done)

---

## 🎯 Mission

Implement MagicBoxAI MVP with full error handling and auto-logging.

---

## 🔴 CRITICAL: Automatic Error Capture

**You must capture ALL errors automatically. Do not expect the user to use pipes.**

Implementation:
```python
import sys
import os
from datetime import datetime

# Setup auto error capture
error_log_file = 'results/codex/error.log'
execution_log_file = f'results/codex/execution_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

# Redirect stdout and stderr to both console and file
class DualWriter:
    def __init__(self, *files):
        self.files = files
    
    def write(self, msg):
        for f in self.files:
            f.write(msg)
            f.flush()
    
    def flush(self):
        for f in self.files:
            f.flush()

# Open log files
with open(execution_log_file, 'w', encoding='utf-8') as exec_log, \
     open(error_log_file, 'w', encoding='utf-8') as err_log:
    
    # Redirect both stdout and stderr
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    
    sys.stdout = DualWriter(original_stdout, exec_log, err_log)
    sys.stderr = DualWriter(original_stderr, exec_log, err_log)
    
    try:
        # ALL YOUR CODE HERE
        # Errors will be automatically captured
        pass
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
    finally:
        sys.stdout = original_stdout
        sys.stderr = original_stderr

print(f"✅ Execution log: {execution_log_file}")
print(f"✅ Error log: {error_log_file}")
```

**The user should NEVER use pipes. You handle it.**

---

## 📋 Development Tasks

### Phase 1: Backend API (Python FastAPI)

1. **File Storage System**
   - Store uploaded HTML files
   - Generate unique tokens (public_id, mgmt_id)
   - Auto-delete after 30 days

2. **Database Schema**
   ```sql
   CREATE TABLE files (
       id INTEGER PRIMARY KEY,
       public_id VARCHAR(255) UNIQUE,
       mgmt_id VARCHAR(255) UNIQUE,
       html_content TEXT,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       expires_at TIMESTAMP,
       view_count INTEGER DEFAULT 0
   );
   
   CREATE TABLE track_limit_daily (
       id INTEGER PRIMARY KEY,
       identifier VARCHAR(255) UNIQUE,
       save_count INTEGER DEFAULT 0,
       last_reset TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       is_premium BOOLEAN DEFAULT FALSE
   );
   
   CREATE TABLE promo_codes (
       id INTEGER PRIMARY KEY,
       code VARCHAR(255) UNIQUE,
       used_count INTEGER DEFAULT 0,
       max_uses INTEGER NULLABLE,
       is_active BOOLEAN DEFAULT TRUE
   );
   ```

3. **API Endpoints**
   ```
   POST /api/save
     Input: {html: "..."}
     Output: {publicUrl: "...", managementUrl: "..."}
     Auth: Cookie/IP rate limiting
   
   GET /api/view/{public_id}
     Output: HTML content
     Note: Increment view_count
   
   DELETE /api/delete/{mgmt_id}
     Output: {success: true}
   
   POST /api/activate-premium
     Input: {promoCode: "..."}
     Output: {success: true}
   
   GET /api/check-limit
     Output: {allowed: true/false, count: N, limit: N}
   ```

4. **Cron Job: Auto-Delete**
   ```python
   # Run daily
   DELETE FROM files WHERE expires_at < NOW()
   ```

---

### Phase 2: Frontend (HTML/CSS/JS)

```html
<!DOCTYPE html>
<html>
<head>
    <title>MagicBoxAI - Run Your Code Now</title>
    <style>
        body { font-family: sans-serif; max-width: 900px; margin: 50px auto; }
        textarea { width: 100%; height: 300px; font-family: monospace; }
        button { padding: 10px 20px; font-size: 16px; }
        #preview { border: 1px solid #ccc; margin-top: 20px; min-height: 200px; }
        .status { margin-top: 10px; padding: 10px; background: #f0f0f0; }
        #rateLimit { color: orange; }
    </style>
</head>
<body>
    <h1>🎮 MagicBoxAI - Paste HTML, See It Run</h1>
    
    <!-- Rate limit display -->
    <div id="rateLimit"></div>
    
    <!-- Code input -->
    <textarea id="htmlCode" placeholder="Paste your HTML/JavaScript code here..."></textarea>
    
    <!-- Preview button -->
    <button onclick="updatePreview()">📺 Preview</button>
    
    <!-- Live preview -->
    <div id="preview"></div>
    
    <!-- Save button -->
    <button id="saveBtn" onclick="saveCode()">💾 Save & Share</button>
    
    <!-- Result display -->
    <div id="result" class="status" style="display:none;"></div>
    
    <!-- Premium section -->
    <div id="premiumSection" style="display:none; margin-top: 20px; padding: 10px; background: #ffffcc; border: 2px solid #ffaa00;">
        <p>Hit the daily limit? Get unlimited saves:</p>
        <input type="text" id="promoCode" placeholder="Enter promo code">
        <button onclick="activatePremium()">Unlock Premium</button>
    </div>
    
    <script>
        async function updatePreview() {
            const code = document.getElementById('htmlCode').value;
            const preview = document.getElementById('preview');
            preview.innerHTML = code;
        }
        
        async function saveCode() {
            const code = document.getElementById('htmlCode').value;
            
            try {
                const response = await fetch('/api/save', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({html: code})
                });
                
                if (!response.ok) {
                    if (response.status === 429) {
                        showPremiumSection();
                        showResult('❌ Daily limit reached. Upgrade to Premium!', 'error');
                        return;
                    }
                    throw new Error('Save failed');
                }
                
                const data = await response.json();
                showResult(`
                    ✅ Saved!
                    Public URL: ${data.publicUrl}
                    Management URL: ${data.managementUrl}
                `, 'success');
                
                checkRateLimit();
            } catch (error) {
                showResult(`❌ Error: ${error.message}`, 'error');
            }
        }
        
        async function checkRateLimit() {
            const response = await fetch('/api/check-limit');
            const data = await response.json();
            
            const rateDiv = document.getElementById('rateLimit');
            if (data.isPremium) {
                rateDiv.innerHTML = '⭐ Premium - Unlimited saves';
                document.getElementById('premiumSection').style.display = 'none';
            } else {
                rateDiv.innerHTML = `📊 Saves today: ${data.count}/${data.limit}`;
                if (!data.allowed) {
                    document.getElementById('saveBtn').disabled = true;
                    showPremiumSection();
                }
            }
        }
        
        async function activatePremium() {
            const code = document.getElementById('promoCode').value;
            const response = await fetch('/api/activate-premium', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({promoCode: code})
            });
            
            if (response.ok) {
                showResult('⭐ Premium activated!', 'success');
                checkRateLimit();
            } else {
                showResult('❌ Invalid promo code', 'error');
            }
        }
        
        function showPremiumSection() {
            document.getElementById('premiumSection').style.display = 'block';
        }
        
        function showResult(msg, type) {
            const resultDiv = document.getElementById('result');
            resultDiv.textContent = msg;
            resultDiv.className = `status ${type}`;
            resultDiv.style.display = 'block';
        }
        
        // Check rate limit on load
        window.addEventListener('load', checkRateLimit);
    </script>
</body>
</html>
```

---

### Phase 3: Deployment

1. Deploy to Heroku / Railway / Sakura Internet
2. Set environment variables
3. Initialize database
4. Test with sample HTML

---

## 🔴 Error Handling Rule

**CRITICAL**: 
- All errors must be auto-captured to `results/codex/error.log`
- User should NEVER need to use pipes or manual logging
- If error occurs, it's in the log file automatically
- User just needs to check `results/codex/error.log` to debug

---

## ✅ Success Criteria

- ✅ Backend API running
- ✅ Database initialized
- ✅ Frontend loads
- ✅ Preview works
- ✅ Save works (creates public + mgmt URLs)
- ✅ Rate limiting works (5/day for free)
- ✅ Premium activation works
- ✅ Auto-delete cron scheduled
- ✅ All errors auto-logged to file
- ✅ Code pushed to GitHub

---

## 📝 Next Action

When complete:
```bash
git pull
codex --kick order_deploy_magicboxai.md
```

---

**Status**: Ready for implementation
**Error Logging**: Automatic (no user pipes needed)
