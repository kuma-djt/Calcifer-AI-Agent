from __future__ import annotations

from dataclasses import dataclass

from skills.groceries_planner.skill import plan_groceries
from skills.routine_builder.skill import build_routine


@dataclass
class ToolCall:
    name: str
    input_text: str
    risky: bool = False


class ToolRouter:
    """Simple deterministic router for supported skills and risky actions."""

    def route(self, text: str) -> ToolCall | None:
        lower = text.lower()
        if any(k in lower for k in ["buy", "purchase", "order"]):
            return ToolCall(name="purchase_request", input_text=text, risky=True)
        if "grocery" in lower or "meal" in lower or "pasta" in lower or "breakfast" in lower:
            return ToolCall(name="groceries_planner", input_text=text)
        if "routine" in lower or "morning" in lower or "evening" in lower:
            return ToolCall(name="routine_builder", input_text=text)
        return None

    def execute(self, call: ToolCall) -> str:
        if call.name == "groceries_planner":
            return plan_groceries(call.input_text)
        if call.name == "routine_builder":
            return build_routine(call.input_text)
        if call.name == "purchase_request":
            return "Purchase request executed."
        return "No tool result."
