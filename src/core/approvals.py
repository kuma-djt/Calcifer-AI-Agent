from __future__ import annotations

from dataclasses import dataclass
from threading import Lock
from typing import Any
from uuid import uuid4


@dataclass
class ApprovalRequest:
    approval_id: str
    tool_name: str
    tool_input: dict[str, Any]


class ApprovalStore:
    """In-memory approval queue for risky tool requests."""

    def __init__(self) -> None:
        self._requests: dict[str, ApprovalRequest] = {}
        self._lock = Lock()

    def create(self, tool_name: str, tool_input: dict[str, Any]) -> ApprovalRequest:
        req = ApprovalRequest(approval_id=str(uuid4()), tool_name=tool_name, tool_input=tool_input)
        with self._lock:
            self._requests[req.approval_id] = req
        return req

    def pop(self, approval_id: str) -> ApprovalRequest | None:
        with self._lock:
            return self._requests.pop(approval_id, None)

    def get(self, approval_id: str) -> ApprovalRequest | None:
        with self._lock:
            return self._requests.get(approval_id)
