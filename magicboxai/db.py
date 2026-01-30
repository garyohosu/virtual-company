import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DATE_FMT = "%Y-%m-%d %H:%M:%S"


def utcnow_str() -> str:
    return datetime.utcnow().strftime(DATE_FMT)


def get_db_path() -> Path:
    url = os.getenv("DATABASE_URL", "sqlite:///./magicboxai.db")
    if not url.startswith("sqlite:///"):
        raise ValueError("Only sqlite is supported in this MVP")
    raw_path = url.replace("sqlite:///", "", 1)
    path = Path(raw_path)
    if not path.is_absolute():
        path = Path.cwd() / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def connect_db() -> sqlite3.Connection:
    conn = sqlite3.connect(get_db_path(), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,
            public_id VARCHAR(255) UNIQUE,
            mgmt_id VARCHAR(255) UNIQUE,
            html_content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            view_count INTEGER DEFAULT 0
        );
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS track_limit_daily (
            id INTEGER PRIMARY KEY,
            identifier VARCHAR(255) UNIQUE,
            save_count INTEGER DEFAULT 0,
            last_reset TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_premium BOOLEAN DEFAULT FALSE
        );
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS promo_codes (
            id INTEGER PRIMARY KEY,
            code VARCHAR(255) UNIQUE,
            used_count INTEGER DEFAULT 0,
            max_uses INTEGER NULL,
            is_active BOOLEAN DEFAULT TRUE
        );
        """
    )
    conn.commit()


def ensure_db() -> None:
    with connect_db() as conn:
        init_db(conn)


def is_new_day(last_reset: str | None) -> bool:
    if not last_reset:
        return True
    try:
        last_dt = datetime.strptime(last_reset, DATE_FMT)
    except ValueError:
        return True
    return last_dt.date() != datetime.utcnow().date()


def cleanup_expired(conn: sqlite3.Connection) -> int:
    now = utcnow_str()
    cur = conn.execute("SELECT id, public_id FROM files WHERE expires_at < ?", (now,))
    rows = cur.fetchall()
    ids = [row["id"] for row in rows]
    if not ids:
        return 0
    conn.execute(
        f"DELETE FROM files WHERE id IN ({','.join(['?'] * len(ids))})",
        ids,
    )
    conn.commit()
    return len(ids)


def default_expiry() -> str:
    return (datetime.utcnow() + timedelta(days=30)).strftime(DATE_FMT)
