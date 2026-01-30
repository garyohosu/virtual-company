import asyncio
import logging
import uuid
from datetime import datetime, timedelta
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from pydantic import BaseModel

from .db import (
    cleanup_expired,
    connect_db,
    default_expiry,
    ensure_db,
    init_db,
    is_new_day,
    utcnow_str,
)
from .logging_utils import setup_logging

LOG_PATHS = setup_logging()
logger = logging.getLogger("magicboxai")

STORAGE_DIR = Path("magicboxai_storage")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

SAVE_LIMIT = 5

app = FastAPI(title="MagicBoxAI", version="0.1.0")


class SaveRequest(BaseModel):
    html: str


class PromoRequest(BaseModel):
    promoCode: str


def _resolve_identifier(request: Request) -> tuple[str, bool]:
    cookie_id = request.cookies.get("mbx_id")
    if cookie_id:
        return cookie_id, False
    ip = request.client.host if request.client else "unknown"
    identifier = f"ip:{ip}"
    return identifier, True


def _load_tracker(conn, identifier: str):
    init_db(conn)
    row = conn.execute(
        "SELECT identifier, save_count, last_reset, is_premium FROM track_limit_daily WHERE identifier = ?",
        (identifier,),
    ).fetchone()

    if row is None:
        conn.execute(
            "INSERT INTO track_limit_daily (identifier, save_count, last_reset, is_premium) VALUES (?, ?, ?, ?)",
            (identifier, 0, utcnow_str(), 0),
        )
        conn.commit()
        row = conn.execute(
            "SELECT identifier, save_count, last_reset, is_premium FROM track_limit_daily WHERE identifier = ?",
            (identifier,),
        ).fetchone()

    if is_new_day(row["last_reset"]):
        conn.execute(
            "UPDATE track_limit_daily SET save_count = 0, last_reset = ? WHERE identifier = ?",
            (utcnow_str(), identifier),
        )
        conn.commit()
        row = conn.execute(
            "SELECT identifier, save_count, last_reset, is_premium FROM track_limit_daily WHERE identifier = ?",
            (identifier,),
        ).fetchone()

    return row


def _tracker_payload(row) -> dict:
    is_premium = bool(row["is_premium"])
    count = int(row["save_count"])
    allowed = is_premium or count < SAVE_LIMIT
    return {
        "allowed": allowed,
        "count": count,
        "limit": SAVE_LIMIT,
        "isPremium": is_premium,
    }


@app.on_event("startup")
async def on_startup() -> None:
    ensure_db()
    with connect_db() as conn:
        cleanup_expired(conn)
    asyncio.create_task(_cleanup_scheduler())


async def _cleanup_scheduler() -> None:
    while True:
        now = datetime.utcnow()
        next_run = datetime.combine(now.date() + timedelta(days=1), datetime.min.time())
        wait_seconds = max(60, int((next_run - now).total_seconds()))
        await asyncio.sleep(wait_seconds)
        try:
            with connect_db() as conn:
                removed = cleanup_expired(conn)
                logger.info("Cleanup removed %s expired files", removed)
        except Exception:
            logger.exception("Scheduled cleanup failed")


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error for %s %s", request.method, request.url.path)
    return PlainTextResponse("Internal server error", status_code=500)


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    html_path = Path(__file__).parent / "static" / "index.html"
    if not html_path.exists():
        return HTMLResponse("<h1>MagicBoxAI</h1><p>Frontend not found.</p>")
    return HTMLResponse(html_path.read_text(encoding="utf-8"))


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@app.post("/api/save")
def save_code(payload: SaveRequest, request: Request):
    if not payload.html or not payload.html.strip():
        raise HTTPException(status_code=400, detail="HTML content is required")

    identifier, set_cookie = _resolve_identifier(request)
    with connect_db() as conn:
        tracker = _load_tracker(conn, identifier)
        tracker_payload = _tracker_payload(tracker)
        if not tracker_payload["allowed"]:
            raise HTTPException(status_code=429, detail="Daily save limit reached")

        public_id = uuid.uuid4().hex
        mgmt_id = uuid.uuid4().hex
        expires_at = default_expiry()
        conn.execute(
            "INSERT INTO files (public_id, mgmt_id, html_content, expires_at) VALUES (?, ?, ?, ?)",
            (public_id, mgmt_id, payload.html, expires_at),
        )
        conn.execute(
            "UPDATE track_limit_daily SET save_count = save_count + 1 WHERE identifier = ?",
            (identifier,),
        )
        conn.commit()

    file_path = STORAGE_DIR / f"{public_id}.html"
    file_path.write_text(payload.html, encoding="utf-8")

    base_url = str(request.base_url).rstrip("/")
    response = JSONResponse(
        {
            "publicUrl": f"{base_url}/api/view/{public_id}",
            "managementUrl": f"{base_url}/api/delete/{mgmt_id}",
        }
    )
    if set_cookie:
        response.set_cookie("mbx_id", identifier, max_age=60 * 60 * 24 * 365, httponly=True, samesite="Lax")
    return response


@app.get("/api/view/{public_id}")
def view_code(public_id: str):
    with connect_db() as conn:
        row = conn.execute(
            "SELECT id, html_content FROM files WHERE public_id = ?",
            (public_id,),
        ).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Not found")
        conn.execute(
            "UPDATE files SET view_count = view_count + 1 WHERE id = ?",
            (row["id"],),
        )
        conn.commit()
        html = row["html_content"]
    return HTMLResponse(html)


@app.delete("/api/delete/{mgmt_id}")
def delete_code(mgmt_id: str):
    with connect_db() as conn:
        row = conn.execute(
            "SELECT id, public_id FROM files WHERE mgmt_id = ?",
            (mgmt_id,),
        ).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Not found")
        conn.execute("DELETE FROM files WHERE id = ?", (row["id"],))
        conn.commit()
        public_id = row["public_id"]

    file_path = STORAGE_DIR / f"{public_id}.html"
    if file_path.exists():
        file_path.unlink()

    return {"success": True}


@app.post("/api/activate-premium")
def activate_premium(payload: PromoRequest, request: Request):
    code = payload.promoCode.strip()
    if not code:
        raise HTTPException(status_code=400, detail="Promo code required")

    identifier, set_cookie = _resolve_identifier(request)
    with connect_db() as conn:
        promo = conn.execute(
            "SELECT id, used_count, max_uses, is_active FROM promo_codes WHERE code = ?",
            (code,),
        ).fetchone()
        if promo is None or not promo["is_active"]:
            raise HTTPException(status_code=400, detail="Invalid promo code")
        if promo["max_uses"] is not None and promo["used_count"] >= promo["max_uses"]:
            raise HTTPException(status_code=400, detail="Promo code exhausted")

        tracker = _load_tracker(conn, identifier)
        conn.execute(
            "UPDATE track_limit_daily SET is_premium = 1, last_reset = ? WHERE identifier = ?",
            (utcnow_str(), identifier),
        )
        conn.execute(
            "UPDATE promo_codes SET used_count = used_count + 1 WHERE id = ?",
            (promo["id"],),
        )
        conn.commit()

    response = JSONResponse({"success": True})
    if set_cookie:
        response.set_cookie("mbx_id", identifier, max_age=60 * 60 * 24 * 365, httponly=True, samesite="Lax")
    return response


@app.get("/api/check-limit")
def check_limit(request: Request):
    identifier, set_cookie = _resolve_identifier(request)
    with connect_db() as conn:
        tracker = _load_tracker(conn, identifier)
        payload = _tracker_payload(tracker)

    response = JSONResponse(payload)
    if set_cookie:
        response.set_cookie("mbx_id", identifier, max_age=60 * 60 * 24 * 365, httponly=True, samesite="Lax")
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("magicboxai.main:app", host="0.0.0.0", port=8000, reload=False)
    print(f"Execution log: {LOG_PATHS['execution_log']}")
    print(f"Error log: {LOG_PATHS['error_log']}")
