import os
from pathlib import Path

from fastapi.testclient import TestClient


def _make_client(tmp_path):
    db_path = tmp_path / "magicboxai_test.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
    from magicboxai.main import app

    return TestClient(app)


def test_check_limit_allows_initial(tmp_path):
    client = _make_client(tmp_path)
    resp = client.get("/api/check-limit")
    assert resp.status_code == 200
    data = resp.json()
    assert data["allowed"] is True
    assert data["count"] == 0
    assert data["limit"] == 5


def test_save_and_view_roundtrip(tmp_path):
    client = _make_client(tmp_path)
    resp = client.post("/api/save", json={"html": "<h1>Hello</h1>"})
    assert resp.status_code == 200
    data = resp.json()
    view_url = data["publicUrl"].replace("http://testserver", "")
    view_resp = client.get(view_url)
    assert view_resp.status_code == 200
    assert "Hello" in view_resp.text


def test_save_rejects_empty_html(tmp_path):
    client = _make_client(tmp_path)
    resp = client.post("/api/save", json={"html": "  "})
    assert resp.status_code == 400


def test_rate_limit_blocks_after_limit(tmp_path):
    client = _make_client(tmp_path)
    for _ in range(5):
        resp = client.post("/api/save", json={"html": "<p>x</p>"})
        assert resp.status_code == 200
    blocked = client.post("/api/save", json={"html": "<p>x</p>"})
    assert blocked.status_code == 429
