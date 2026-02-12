from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from typing import Any
from uuid import uuid4


@dataclass
class ApprovalRequest:
    approval_id: str
    tool_name: str
    tool_input: dict[str, Any]


class ApprovalStore:
    """Approval queue with JSON persistence for risky tool requests."""

    def __init__(self, storage_path: str = "memory/approvals.json") -> None:
        self._requests: dict[str, ApprovalRequest] = {}
        self._lock = Lock()
        self._storage_path = Path(storage_path)
        self._storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._load()

    def _load(self) -> None:
        if not self._storage_path.exists():
            return
        raw = self._storage_path.read_text(encoding="utf-8").strip()
        if not raw:
            return
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return
        for item in data:
            req = ApprovalRequest(
                approval_id=item["approval_id"],
                tool_name=item["tool_name"],
                tool_input=item["tool_input"],
            )
            self._requests[req.approval_id] = req

    def _persist(self) -> None:
        payload = [
            {
                "approval_id": req.approval_id,
                "tool_name": req.tool_name,
                "tool_input": req.tool_input,
            }
            for req in self._requests.values()
        ]
        temp_path = self._storage_path.with_suffix(".tmp")
        temp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        temp_path.replace(self._storage_path)

    def create(self, tool_name: str, tool_input: dict[str, Any]) -> ApprovalRequest:
        req = ApprovalRequest(approval_id=str(uuid4()), tool_name=tool_name, tool_input=tool_input)
        with self._lock:
            self._requests[req.approval_id] = req
            self._persist()
        return req

    def pop(self, approval_id: str) -> ApprovalRequest | None:
        with self._lock:
            req = self._requests.pop(approval_id, None)
            self._persist()
            return req

    def get(self, approval_id: str) -> ApprovalRequest | None:
        with self._lock:
            return self._requests.get(approval_id)
