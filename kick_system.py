#!/usr/bin/env python
"""
Kick System CLI for Virtual Company.

Usage:
  python kick_system.py --kick order.md
"""

from __future__ import annotations

import argparse
import re
import subprocess
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
            updated.append(f"**Status**: 竢ｳ Waiting for {next_actor}")
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
        subprocess.run(cmd, cwd=repo_root, check=True)

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


def main() -> int:
    parser = argparse.ArgumentParser(description="Kick System CLI")
    parser.add_argument("--kick", required=True, help="Path to order.md")
    parser.add_argument("--no-git", action="store_true", help="Skip git commit/push")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent
    order_path = Path(args.kick)
    if not order_path.is_absolute():
        order_path = (repo_root / order_path).resolve()
    if not order_path.exists():
        raise FileNotFoundError(f"Order file not found: {order_path}")

    order_text = order_path.read_text(encoding="utf-8")
    current_actor = _extract_field(order_text, "Current Actor")
    next_actor = _extract_field(order_text, "Next Actor")
    instructions = _extract_instructions(order_text)

    context = _load_employee_context(repo_root, current_actor)

    print(f"側 {context.name} ({context.role}) is executing...")
    print("搭 Instructions:")
    for line in instructions.splitlines():
        print(f"   {line}")

    print("")
    print("Context:")
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

    if not args.no_git:
        _run_git(repo_root, current_actor)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
