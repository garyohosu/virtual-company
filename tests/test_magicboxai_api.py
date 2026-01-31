import os
import pytest
import httpx
from fastapi.testclient import TestClient

# Get Base URL from environment (e.g., "https://garyo.sakura.ne.jp/magicboxai")
REMOTE_BASE_URL = os.environ.get("MAGICBOXAI_BASE_URL")

@pytest.fixture
def client(tmp_path):
    if REMOTE_BASE_URL:
        # Remote Testing
        # verify=False might be needed if certs are an issue, but Sakura has valid certs.
        with httpx.Client(base_url=REMOTE_BASE_URL, timeout=10.0) as c:
            yield c
    else:
        # Local Testing with isolated DB
        db_path = tmp_path / "magicboxai_test.db"
        os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
        # Import app here to ensure env var is set before app startup (if app reads it on import)
        # However, typically app reads on call or module level. 
        # Ideally we reload the module or use a factory, but for this simple app:
        from magicboxai import db
        # Reset DB globals if needed or rely on SQLite path
        
        from magicboxai.main import app
        # Ensure DB is fresh
        with TestClient(app) as c:
            yield c

def test_health_check(client):
    # This might require /index.php/api/health or /api/health depending on deployment
    # The client base_url should handle the prefix if set correctly.
    # We will try standard /api/health. 
    # If using TestClient, it is relative to root.
    
    # Sakura PHP routing: /api/health works if .htaccess is correct.
    resp = client.get("/api/health")
    # If 404, try index.php prefix (fallback logic could be added but let's assume it works)
    if resp.status_code == 404 and REMOTE_BASE_URL:
         resp = client.get("index.php/api/health")

    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"

def test_check_limit_allows_initial(client):
    resp = client.get("/api/check-limit")
    assert resp.status_code == 200
    data = resp.json()
    assert data["allowed"] is True
    # count might not be 0 on remote if shared IP used, but allowed should be true initially (unless exhausted)
    # assert data["count"] == 0 
    assert "limit" in data

def test_save_and_view_roundtrip(client):
    html_content = "<h1>Hello Remote World</h1>"
    resp = client.post("/api/save", json={"html": html_content})
    assert resp.status_code in (200, 201) # PHP uses 201, Python 200 (maybe)
    data = resp.json()
    
    public_url = data["public_url"] if "public_url" in data else data["publicUrl"]
    
    # If local TestClient, publicUrl is http://testserver/api/view/...
    # If remote, it is https://garyo.sakura.ne.jp/magicboxai/view/...
    
    # We need to fetch the view.
    # If public_url is absolute, httpx client.get(public_url) works.
    # TestClient.get(public_url) might treat it weirdly if it has host.
    
    if REMOTE_BASE_URL:
        # public_url is absolute
        view_resp = httpx.get(public_url)
    else:
        # local: http://testserver/api/view/...
        # TestClient handles relative paths best. Extract path.
        from urllib.parse import urlparse
        path = urlparse(public_url).path
        view_resp = client.get(path)
        
    assert view_resp.status_code == 200
    assert "Hello Remote World" in view_resp.text

def test_save_rejects_empty_html(client):
    resp = client.post("/api/save", json={"html": "  "})
    assert resp.status_code == 400

@pytest.mark.skipif(REMOTE_BASE_URL is not None, reason="Avoid consuming rate limits on production")
def test_rate_limit_blocks_after_limit(client):
    # This test is destructive to the rate limit state
    for _ in range(5):
        resp = client.post("/api/save", json={"html": "<p>x</p>"})
        assert resp.status_code in (200, 201)
    blocked = client.post("/api/save", json={"html": "<p>x</p>"})
    assert blocked.status_code == 429
