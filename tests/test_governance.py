from __future__ import annotations

import json
from pathlib import Path

from calcifer.adapters.storage.journal import MemoryJournal
from calcifer.core.approvals import ApprovalStore
from calcifer.core.tool_router import ToolRouter


def test_journal_logging(tmp_path: Path) -> None:
    journal = MemoryJournal(str(tmp_path))
    out = journal.append_turn(
        "plan groceries",
        "Grocery plan generated",
        [{"tool": "groceries_planner"}],
        [{"tool": "groceries_planner", "result": "ok"}],
    )

    content = out.read_text(encoding="utf-8")
    assert "timestamp:" in content
    assert "user: plan groceries" in content
    assert "tool_requests:" in content
    assert "tool_results:" in content


def test_approvals_gate(tmp_path: Path) -> None:
    store = ApprovalStore(storage_path=str(tmp_path / "approvals.json"))
    req = store.create("purchase_request", {"text": "buy a laptop"})
    assert store.get(req.approval_id) is not None
    popped = store.pop(req.approval_id)
    assert popped is not None
    assert popped.tool_name == "purchase_request"
    assert store.get(req.approval_id) is None


def test_approval_persistence_survives_restart(tmp_path: Path) -> None:
    approvals_file = tmp_path / "approvals.json"
    store = ApprovalStore(storage_path=str(approvals_file))
    req = store.create("purchase_request", {"text": "buy diapers"})

    restarted_store = ApprovalStore(storage_path=str(approvals_file))
    loaded = restarted_store.get(req.approval_id)

    assert loaded is not None
    assert loaded.tool_name == "purchase_request"
    assert loaded.tool_input == {"text": "buy diapers"}

    data = json.loads(approvals_file.read_text(encoding="utf-8"))
    assert data and data[0]["approval_id"] == req.approval_id


def test_approval_store_handles_missing_parent_dir(tmp_path: Path) -> None:
    approvals_file = tmp_path / "nested" / "approvals.json"
    store = ApprovalStore(storage_path=str(approvals_file))

    req = store.create("purchase_request", {"text": "buy soap"})
    assert approvals_file.exists()
    assert store.get(req.approval_id) is not None


def test_approval_store_ignores_corrupt_json(tmp_path: Path) -> None:
    approvals_file = tmp_path / "approvals.json"
    approvals_file.write_text("not-json", encoding="utf-8")

    store = ApprovalStore(storage_path=str(approvals_file))
    assert store.get("missing") is None


def test_tool_routing() -> None:
    router = ToolRouter()
    groceries = router.route("make a grocery list for pasta night")
    routine = router.route("build me a morning routine")
    risky = router.route("purchase paper towels")

    assert groceries and groceries.name == "groceries_planner"
    assert routine and routine.name == "routine_builder"
    assert risky and risky.risky is True
