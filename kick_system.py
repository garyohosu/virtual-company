#!/usr/bin/env python
"""
Kick System CLI for Virtual Company.

Usage:
  python kick_system.py --kick order.md
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import traceback
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional


META_KEYS = {
    "Status": "**Status**:",
    "Current Actor": "**Current Actor**:",
    "Next Actor": "**Next Actor**:",
    "Previous Actor": "**Previous Actor**:",
    "Completed At": "**Completed At**:",
}

ERROR_LOG_RELATIVE = Path("results") / "codex" / "error.log"
AUDIT_LOG_RELATIVE = Path("results") / "codex" / "audit.log"
RATE_LIMIT_RELATIVE = Path("results") / "codex" / "rate_limit.json"
ALLOWED_ACTOR_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")
ALLOWED_ORDER_EXTENSIONS = {".md"}
MAX_ORDER_SIZE_BYTES = 512 * 1024
RATE_LIMIT_SECONDS = 60


@dataclass
class EmployeeContext:
    name: str
    role: str
    whoami_path: Optional[Path]
    memory_path: Optional[Path]
    skills_path: Optional[Path]
    inbox_dir: Optional[Path]
    inbox_files: list[str]


def _extract_field(text: str, field_name: str) -> str:
    pattern = rf"^\*\*{re.escape(field_name)}\*\*:\s*(.+?)\s*$"
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        raise ValueError(f"Missing field in order.md: {field_name}")
    return match.group(1).strip()


def _extract_instructions(text: str) -> str:
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if any(stripped.startswith(prefix) for prefix in META_KEYS.values()):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def _parse_whoami(text: str) -> tuple[Optional[str], Optional[str]]:
    name_match = re.search(r"^\*\*Name\*\*:\s*(.+?)\s*$", text, flags=re.MULTILINE)
    role_match = re.search(r"^\*\*Role\*\*:\s*(.+?)\s*$", text, flags=re.MULTILINE)
    name = name_match.group(1).strip() if name_match else None
    role = role_match.group(1).strip() if role_match else None
    return name, role


def _configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            continue


def _log_error(repo_root: Path, message: str, exc: BaseException | None = None) -> None:
    log_path = repo_root / ERROR_LOG_RELATIVE
    log_path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] {message}\n")
        if exc:
            handle.write(f"Type: {type(exc).__name__}\n")
            handle.write(f"Error: {exc}\n")
            handle.write("Traceback:\n")
            handle.write("".join(traceback.format_exception(exc)))
            handle.write("\n")


def _write_audit_log(repo_root: Path, event: str, details: dict[str, str]) -> None:
    log_path = repo_root / AUDIT_LOG_RELATIVE
    log_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event": event,
        **details,
    }
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _validate_actor_name(actor: str, field_label: str) -> None:
    if not actor:
        raise ValueError(f"{field_label} cannot be empty.")
    if not ALLOWED_ACTOR_PATTERN.match(actor):
        raise ValueError(
            f"{field_label} '{actor}' must match pattern {ALLOWED_ACTOR_PATTERN.pattern}."
        )


def _validate_order_path(repo_root: Path, order_path: Path) -> Path:
    resolved = order_path.resolve()
    try:
        resolved.relative_to(repo_root)
    except ValueError as exc:
        raise ValueError("Order file must be inside the repository.") from exc
    if resolved.suffix.lower() not in ALLOWED_ORDER_EXTENSIONS:
        raise ValueError(
            f"Order file extension must be one of {sorted(ALLOWED_ORDER_EXTENSIONS)}."
        )
    if not resolved.exists():
        raise FileNotFoundError(f"Order file not found: {resolved}")
    size = resolved.stat().st_size
    if size == 0:
        raise ValueError("Order file is empty.")
    if size > MAX_ORDER_SIZE_BYTES:
        raise ValueError("Order file exceeds maximum size.")
    return resolved


def _enforce_rate_limit(
    repo_root: Path, actor: str, now_ts: float | None = None
) -> None:
    if now_ts is None:
        now_ts = time.time()
    rate_path = repo_root / RATE_LIMIT_RELATIVE
    rate_path.parent.mkdir(parents=True, exist_ok=True)
    data: dict[str, float] = {}
    if rate_path.exists():
        try:
            data = json.loads(rate_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {}
    last_ts = data.get(actor)
    if last_ts and now_ts - last_ts < RATE_LIMIT_SECONDS:
        remaining = int(RATE_LIMIT_SECONDS - (now_ts - last_ts))
        raise RuntimeError(f"Rate limit hit for {actor}. Try again in {remaining}s.")
    data[actor] = now_ts
    rate_path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _load_employee_context(repo_root: Path, actor: str) -> EmployeeContext:
    base_dir = repo_root / "Employees" / actor
    whoami_path = base_dir / "WhoAmI.md"
    memory_path = base_dir / "Memory.md"
    skills_path = base_dir / "Skills.md"
    inbox_dir = base_dir / "Mail" / "inbox"

    name = actor
    role = "Unknown"
    if whoami_path.exists():
        whoami_text = whoami_path.read_text(encoding="utf-8")
        parsed_name, parsed_role = _parse_whoami(whoami_text)
        if parsed_name:
            name = parsed_name
        if parsed_role:
            role = parsed_role

    inbox_files = []
    if inbox_dir.exists() and inbox_dir.is_dir():
        inbox_files = sorted(p.name for p in inbox_dir.iterdir() if p.is_file())

    return EmployeeContext(
        name=name,
        role=role,
        whoami_path=whoami_path if whoami_path.exists() else None,
        memory_path=memory_path if memory_path.exists() else None,
        skills_path=skills_path if skills_path.exists() else None,
        inbox_dir=inbox_dir if inbox_dir.exists() else None,
        inbox_files=inbox_files,
    )


def _update_order_content(
    text: str, current_actor: str, next_actor: str, timestamp: str
) -> str:
    lines = text.splitlines()
    updated = []
    found = {key: False for key in META_KEYS}

    for line in lines:
        stripped = line.strip()
        if stripped.startswith(META_KEYS["Status"]):
            updated.append(f"**Status**: Waiting for {next_actor}")
            found["Status"] = True
            continue
        if stripped.startswith(META_KEYS["Current Actor"]):
            updated.append(f"**Current Actor**: {next_actor}")
            found["Current Actor"] = True
            continue
        if stripped.startswith(META_KEYS["Previous Actor"]):
            updated.append(f"**Previous Actor**: {current_actor}")
            found["Previous Actor"] = True
            continue
        if stripped.startswith(META_KEYS["Completed At"]):
            updated.append(f"**Completed At**: {timestamp}")
            found["Completed At"] = True
            continue
        updated.append(line)

    if not found["Previous Actor"]:
        updated = _insert_after(
            updated,
            lambda l: l.strip().startswith(META_KEYS["Current Actor"]),
            [f"**Previous Actor**: {current_actor}"],
        )
    if not found["Completed At"]:
        updated = _insert_after(
            updated,
            lambda l: l.strip().startswith(META_KEYS["Previous Actor"]),
            [f"**Completed At**: {timestamp}"],
        )
    return "\n".join(updated) + ("\n" if text.endswith("\n") else "")


def _insert_after(lines: list[str], predicate, new_lines: Iterable[str]) -> list[str]:
    for i, line in enumerate(lines):
        if predicate(line):
            return lines[: i + 1] + list(new_lines) + lines[i + 1 :]
    return lines + list(new_lines)


def _run_git(repo_root: Path, current_actor: str) -> None:
    def run(cmd: list[str]) -> None:
        subprocess.run(cmd, cwd=repo_root, check=True, capture_output=True, text=True)

    try:
        run(["git", "add", "."])

        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
        if not status.stdout.strip():
            print("No changes detected; skipping commit/push.")
            return

        commit_message = f"chore: Kick - {current_actor} executed"
        run(["git", "commit", "-m", commit_message])
        run(["git", "push"])
    except subprocess.CalledProcessError as exc:
        details = (exc.stderr or exc.stdout or "").strip()
        if details:
            raise RuntimeError(f"Git command failed: {details}") from exc
        raise RuntimeError("Git command failed with no output.") from exc


def main() -> int:
    _configure_stdio()
    parser = argparse.ArgumentParser(description="Kick System CLI")
    parser.add_argument("--kick", required=True, help="Path to order.md")
    parser.add_argument("--no-git", action="store_true", help="Skip git commit/push")
    parser.add_argument(
        "--no-rate-limit", action="store_true", help="Skip rate limiting checks"
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent
    try:
        order_path = Path(args.kick)
        if not order_path.is_absolute():
            order_path = repo_root / order_path
        order_path = _validate_order_path(repo_root, order_path)

        order_text = order_path.read_text(encoding="utf-8")
        current_actor = _extract_field(order_text, "Current Actor")
        next_actor = _extract_field(order_text, "Next Actor")
        _validate_actor_name(current_actor, "Current Actor")
        _validate_actor_name(next_actor, "Next Actor")

        if not args.no_rate_limit:
            _enforce_rate_limit(repo_root, current_actor)

        _write_audit_log(
            repo_root,
            "KICK_STARTED",
            {"current_actor": current_actor, "next_actor": next_actor, "order": str(order_path)},
        )
        instructions = _extract_instructions(order_text)

        context = _load_employee_context(repo_root, current_actor)

        print(f"INFO: {context.name} ({context.role}) is executing...")
        print("INFO: Instructions:")
        for line in instructions.splitlines():
            print(f"  {line}")

        print("")
        print("INFO: Context:")
        print(f"  WhoAmI: {'OK' if context.whoami_path else 'MISSING'}")
        print(f"  Memory: {'OK' if context.memory_path else 'MISSING'}")
        print(f"  Skills: {'OK' if context.skills_path else 'MISSING'}")
        if context.inbox_dir:
            print(f"  Inbox: {len(context.inbox_files)} message(s)")
            for name in context.inbox_files:
                print(f"    - {name}")
        else:
            print("  Inbox: MISSING")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        updated = _update_order_content(order_text, current_actor, next_actor, timestamp)
        order_path.write_text(updated, encoding="utf-8")
        _write_audit_log(
            repo_root,
            "ORDER_UPDATED",
            {"current_actor": current_actor, "next_actor": next_actor, "order": str(order_path)},
        )

        if not args.no_git:
            _run_git(repo_root, current_actor)
            _write_audit_log(
                repo_root,
                "GIT_PUSHED",
                {"current_actor": current_actor},
            )
        else:
            _write_audit_log(
                repo_root,
                "GIT_SKIPPED",
                {"current_actor": current_actor},
            )

        return 0
    except Exception as exc:
        _write_audit_log(
            repo_root,
            "KICK_FAILED",
            {"error": str(exc)},
        )
        _log_error(repo_root, "Kick system failed.", exc)
        print(
            "ERROR: Kick system failed. See results/codex/error.log for details.",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
