import pytest

import kick_system


def test_extract_field():
    text = """
**Current Actor**: alice
**Next Actor**: engineering_bob
"""
    assert kick_system._extract_field(text, "Current Actor") == "alice"
    assert kick_system._extract_field(text, "Next Actor") == "engineering_bob"


def test_extract_instructions_omits_meta():
    text = """
**Status**: Waiting for alice
**Current Actor**: alice
**Next Actor**: engineering_bob

## Instructions
- Do the thing
"""
    instructions = kick_system._extract_instructions(text)
    assert "Status" not in instructions
    assert "Current Actor" not in instructions
    assert "Next Actor" not in instructions
    assert "Do the thing" in instructions


def test_load_employee_context(tmp_path):
    repo_root = tmp_path
    base_dir = repo_root / "Employees" / "alice"
    base_dir.mkdir(parents=True)
    whoami_path = base_dir / "WhoAmI.md"
    whoami_path.write_text("""
**Name**: Alice
**Role**: Database Administrator
""", encoding="utf-8")
    (base_dir / "Memory.md").write_text("memory", encoding="utf-8")
    (base_dir / "Skills.md").write_text("skills", encoding="utf-8")
    inbox_dir = base_dir / "Mail" / "inbox"
    inbox_dir.mkdir(parents=True)
    (inbox_dir / "msg1.md").write_text("hello", encoding="utf-8")

    context = kick_system._load_employee_context(repo_root, "alice")

    assert context.name == "Alice"
    assert context.role == "Database Administrator"
    assert context.whoami_path is not None
    assert context.memory_path is not None
    assert context.skills_path is not None
    assert context.inbox_dir is not None
    assert context.inbox_files == ["msg1.md"]


def test_update_order_content():
    original = """
# Order
**Status**: Waiting for alice
**Current Actor**: alice
**Next Actor**: engineering_bob
"""
    updated = kick_system._update_order_content(
        original, "alice", "engineering_bob", "2026-01-30 10:00"
    )
    assert "**Status**: Waiting for engineering_bob" in updated
    assert "**Current Actor**: engineering_bob" in updated
    assert "**Previous Actor**: alice" in updated
    assert "**Completed At**: 2026-01-30 10:00" in updated


def test_validate_actor_name():
    kick_system._validate_actor_name("engineering_bob", "Current Actor")
    with pytest.raises(ValueError):
        kick_system._validate_actor_name("bad name", "Current Actor")


def test_validate_order_path(tmp_path):
    repo_root = tmp_path
    order_path = repo_root / "order.md"
    order_path.write_text("**Current Actor**: alice\n**Next Actor**: bob\n", encoding="utf-8")

    resolved = kick_system._validate_order_path(repo_root, order_path)
    assert resolved == order_path

    bad_path = repo_root / "order.txt"
    bad_path.write_text("content", encoding="utf-8")
    with pytest.raises(ValueError):
        kick_system._validate_order_path(repo_root, bad_path)


def test_enforce_rate_limit(tmp_path):
    repo_root = tmp_path
    kick_system._enforce_rate_limit(repo_root, "alice", now_ts=1000.0)
    with pytest.raises(RuntimeError):
        kick_system._enforce_rate_limit(repo_root, "alice", now_ts=1000.0 + 10)
