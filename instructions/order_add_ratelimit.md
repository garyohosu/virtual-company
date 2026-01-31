# Order - Add Rate Limiting to MagicBoxAI

**Status**: ⏳ Waiting for implementation
**Current Actor**: codex
**Next Actor**: (complete when done)

---

## 🎯 Mission

Add rate limiting to MagicBoxAI to prevent abuse.

Free users: Limited to N saves per day (Cookie/IP-based).
Premium users (with promo code): Unlimited.

---

## 📋 Requirements

### 1. Rate Limiting Strategy

**Method**: Combination of Cookie + IP Address
- Cookie: Persistent client-side tracking
- IP: Server-side fallback tracking

**Purpose**: Stop abuse without authentication

### 2. Implementation

#### 2.1: Database Schema Addition

Add to metadata table:
```sql
-- track_limit_daily table
CREATE TABLE track_limit_daily (
    id INTEGER PRIMARY KEY,
    identifier VARCHAR(255) UNIQUE,  -- hash of (IP + Cookie)
    save_count INTEGER DEFAULT 0,
    last_reset TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_premium BOOLEAN DEFAULT FALSE,
    promo_code VARCHAR(255) NULLABLE
);

-- Indexes
CREATE INDEX idx_identifier ON track_limit_daily(identifier);
CREATE INDEX idx_last_reset ON track_limit_daily(last_reset);
```

#### 2.2: Frontend Changes

**Add to HTML form**:
```html
<!-- Show rate limit status -->
<div id="rateLimit">
  <p id="savedToday">Saves today: <span id="count">0</span>/5</p>
  <p id="premiumUpgrade" style="display:none;">
    Go premium to save unlimited.
    <input type="text" id="promoCode" placeholder="Enter promo code">
    <button onclick="applyPromoCode()">Unlock Premium</button>
  </p>
</div>

<!-- Premium promo code input (always available) -->
<div id="premiumSection" style="display:none;">
  <input type="text" id="premiumPromoInput" placeholder="Promo code">
  <button onclick="applyPromoCode()">Activate Premium</button>
</div>

<!-- Save button -->
<button id="saveBtn" onclick="saveHTML()">Save</button>
```

**JavaScript**:
```javascript
async function checkRateLimit() {
  const response = await fetch('/api/check-limit');
  const data = await response.json();
  
  // data.allowed: boolean
  // data.count: number of saves today
  // data.limit: daily limit (5 or unlimited)
  // data.isPremium: boolean
  
  document.getElementById('count').textContent = data.count;
  
  if (data.isPremium) {
    document.getElementById('rateLimit').style.display = 'none';
    document.getElementById('saveBtn').disabled = false;
  } else if (data.allowed) {
    document.getElementById('saveBtn').disabled = false;
    document.getElementById('premiumUpgrade').style.display = 'block';
  } else {
    document.getElementById('saveBtn').disabled = true;
    document.getElementById('saveBtn').textContent = 'Daily limit reached';
    document.getElementById('premiumUpgrade').style.display = 'block';
  }
}

async function applyPromoCode() {
  const code = document.getElementById('promoCode').value;
  const response = await fetch('/api/activate-premium', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({promoCode: code})
  });
  
  if (response.ok) {
    alert('Premium unlocked!');
    checkRateLimit();
  } else {
    alert('Invalid promo code');
  }
}

// Check limit on page load
window.addEventListener('load', checkRateLimit);
```

#### 2.3: Backend API Changes

**New endpoints**:

```
GET /api/check-limit
  Returns:
  {
    "allowed": true/false,
    "count": 3,
    "limit": 5 or unlimited,
    "isPremium": false
  }

POST /api/save (existing)
  Add: Increment counter if not premium
  
POST /api/activate-premium
  Input: {promoCode: "CODE123"}
  Action: Mark user as premium
  Return: {success: true, expiresAt: null}
```

#### 2.4: Backend Logic

```python
# In backend (FastAPI/Express)

def get_user_identifier(request):
  """Generate unique identifier from IP + Cookie"""
  ip = request.client.host
  cookie = request.cookies.get('session_id')
  
  if not cookie:
    # Generate new session cookie
    cookie = generate_uuid()
    response.set_cookie('session_id', cookie, max_age=86400*365)
  
  # Hash IP + Cookie together
  identifier = hash(f"{ip}:{cookie}")
  return identifier

def check_rate_limit(identifier):
  """Check if user can save"""
  record = db.query('track_limit_daily').filter(
    identifier=identifier
  ).first()
  
  if not record:
    # New user
    db.insert('track_limit_daily', {
      identifier: identifier,
      save_count: 0,
      is_premium: False
    })
    return {'allowed': True, 'count': 0, 'limit': 5}
  
  # Check if 24 hours passed
  if time.now() - record.last_reset > 86400:
    # Reset counter
    db.update('track_limit_daily', 
      {save_count: 0, last_reset: time.now()},
      identifier=identifier
    )
    return {'allowed': True, 'count': 0, 'limit': 5}
  
  # Premium users: unlimited
  if record.is_premium:
    return {'allowed': True, 'count': record.save_count, 'limit': 'unlimited', 'isPremium': True}
  
  # Free users: 5 per day
  if record.save_count >= 5:
    return {'allowed': False, 'count': record.save_count, 'limit': 5}
  
  return {'allowed': True, 'count': record.save_count, 'limit': 5}

def increment_save_count(identifier):
  """Increment after successful save"""
  record = db.query('track_limit_daily').filter(identifier=identifier).first()
  
  if record:
    db.update('track_limit_daily', 
      {save_count: record.save_count + 1},
      identifier=identifier
    )

@app.post('/api/save')
def save_html(request):
  identifier = get_user_identifier(request)
  limit_check = check_rate_limit(identifier)
  
  if not limit_check['allowed']:
    return {'error': 'Rate limit exceeded'}, 429
  
  # Save HTML...
  save_file(request.body['html'])
  
  # Increment counter
  increment_save_count(identifier)
  
  return {'publicUrl': url, 'managementUrl': mgmt_url}

@app.get('/api/check-limit')
def check_limit(request):
  identifier = get_user_identifier(request)
  return check_rate_limit(identifier)

@app.post('/api/activate-premium')
def activate_premium(request):
  promo_code = request.body['promoCode']
  
  # Validate promo code
  if not is_valid_promo_code(promo_code):
    return {'error': 'Invalid code'}, 400
  
  identifier = get_user_identifier(request)
  
  db.update('track_limit_daily',
    {is_premium: True, promo_code: promo_code},
    identifier=identifier
  )
  
  return {'success': True, 'unlimited': True}
```

---

### 3. Promo Code Management

**Backend**:
```python
# Promo codes table
CREATE TABLE promo_codes (
    id INTEGER PRIMARY KEY,
    code VARCHAR(255) UNIQUE,
    created_at TIMESTAMP,
    used_count INTEGER DEFAULT 0,
    max_uses INTEGER (NULL = unlimited),
    is_active BOOLEAN DEFAULT TRUE
);

def is_valid_promo_code(code):
  record = db.query('promo_codes').filter(code=code).first()
  
  if not record:
    return False
  
  if not record.is_active:
    return False
  
  if record.max_uses and record.used_count >= record.max_uses:
    return False
  
  return True

def use_promo_code(code):
  db.update('promo_codes',
    {used_count: used_count + 1},
    code=code
  )
```

**Generate promo codes**:
```python
import secrets

def generate_promo_codes(count=10, max_uses_per_code=None):
  """Generate promo codes for distribution"""
  codes = []
  for i in range(count):
    code = f"MAGIC{secrets.token_hex(8).upper()}"
    db.insert('promo_codes', {
      code: code,
      max_uses: max_uses_per_code,
      is_active: True
    })
    codes.append(code)
  
  return codes

# Usage: 
# codes = generate_promo_codes(count=50, max_uses_per_code=None)
# Share codes with early adopters
```

---

### 4. Configuration

Add to config:
```python
# Rate limiting
FREE_TIER_DAILY_LIMIT = 5  # Can be changed
RATE_LIMIT_WINDOW = 86400  # 24 hours in seconds
RATE_LIMIT_METHOD = "cookie_ip"  # or "cookie_only" or "ip_only"
```

---

## 📋 Tasks

1. ✅ Add `track_limit_daily` table to database
2. ✅ Add `promo_codes` table to database
3. ✅ Update frontend HTML with rate limit display
4. ✅ Add JavaScript rate limit checking
5. ✅ Implement `/api/check-limit` endpoint
6. ✅ Implement `/api/activate-premium` endpoint
7. ✅ Update `/api/save` to check and increment limit
8. ✅ Test with multiple users/IPs
9. ✅ Create promo code generation script
10. ✅ Document for deployment

---

## ✅ Success Criteria

- ✅ Free user can save max 5 times per day
- ✅ 6th attempt shows "limit reached"
- ✅ Premium user (with promo code) can save unlimited
- ✅ Cookie-based tracking works across sessions
- ✅ IP-based tracking as fallback
- ✅ Promo codes can be generated and validated
- ✅ Promo codes are one-time (can be used multiple times but tracked)
- ✅ Daily counter resets at UTC midnight
- ✅ UI shows remaining saves

---

## 🎯 Outcome

**Free users**: 5 saves/day = Prevents spam/abuse
**Premium users**: Unlimited saves = Incentive to purchase promo code

**Cost to implement**: ~400 lines of code
**Implementation time**: 2-3 hours

---

## 📝 Next Action

When this is complete:
```bash
git pull
codex --kick order_magicboxai_development.md
```

And start actual development with rate limiting already designed.

---

**Status**: Ready for implementation
**Executor**: codex
**Output**: All code changes pushed to GitHub
