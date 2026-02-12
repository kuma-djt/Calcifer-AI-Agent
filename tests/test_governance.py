from __future__ import annotations

from pathlib import Path

from src.adapters.storage.journal import MemoryJournal
from src.core.approvals import ApprovalStore
from src.core.tool_router import ToolRouter


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


def test_approvals_gate() -> None:
    store = ApprovalStore()
    req = store.create("purchase_request", {"text": "buy a laptop"})
    assert store.get(req.approval_id) is not None
    popped = store.pop(req.approval_id)
    assert popped is not None
    assert popped.tool_name == "purchase_request"
    assert store.get(req.approval_id) is None


def test_tool_routing() -> None:
    router = ToolRouter()
    groceries = router.route("make a grocery list for pasta night")
    routine = router.route("build me a morning routine")
    risky = router.route("purchase paper towels")

    assert groceries and groceries.name == "groceries_planner"
    assert routine and routine.name == "routine_builder"
    assert risky and risky.risky is True
