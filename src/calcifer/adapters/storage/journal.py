from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any


class MemoryJournal:
    def __init__(self, memory_dir: str = "memory") -> None:
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)

    def append_turn(
        self,
        user_text: str,
        assistant_reply: str,
        tool_requests: list[dict[str, Any]],
        tool_results: list[dict[str, Any]],
    ) -> Path:
        now = datetime.now()
        file_path = self.memory_dir / f"{now:%Y-%m-%d}.md"
        timestamp = now.isoformat(timespec="seconds")

        lines = [
            "\n---\n",
            f"timestamp: {timestamp}\n",
            f"user: {user_text}\n",
            f"assistant: {assistant_reply}\n",
            "tool_requests:\n",
        ]
        if tool_requests:
            lines.extend(f"- {request}\n" for request in tool_requests)
        else:
            lines.append("- none\n")

        lines.append("tool_results:\n")
        if tool_results:
            lines.extend(f"- {result}\n" for result in tool_results)
        else:
            lines.append("- none\n")

        with file_path.open("a", encoding="utf-8") as handle:
            handle.writelines(lines)

        return file_path
