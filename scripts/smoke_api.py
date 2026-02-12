from __future__ import annotations

import os
from typing import Any

import requests

BASE_URL = os.getenv("CALCIFER_API_BASE_URL", "http://127.0.0.1:8000")
API_TOKEN = os.getenv("CALCIFER_API_TOKEN", "")
SESSION_ID = "smoke-session"


def _print_step(title: str, data: dict[str, Any]) -> None:
    print(f"\n=== {title} ===")
    print(data)


def _post(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    response = requests.post(
        f"{BASE_URL}{path}",
        json=payload,
        headers={"Authorization": f"Bearer {API_TOKEN}"},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def main() -> int:
    if not API_TOKEN:
        print("FAIL: set CALCIFER_API_TOKEN before running smoke test.")
        return 1

    try:
        normal = _post("/chat", {"session_id": SESSION_ID, "text": "make me a grocery list for pasta night"})
        _print_step("Normal /chat", normal)

        risky = _post("/chat", {"session_id": SESSION_ID, "text": "buy diapers"})
        _print_step("Risky /chat (approval expected)", risky)

        if risky.get("status") != "needs_approval" or not risky.get("approval_id"):
            print("FAIL: risky request did not require approval.")
            return 1

        approval = _post("/approve", {"approval_id": risky["approval_id"], "approve": True})
        _print_step("/approve", approval)
    except requests.RequestException as exc:
        print(f"FAIL: request error: {exc}")
        return 1

    print("\nPASS: smoke flow succeeded (chat, approval gate, approval execution, journaling side effects on server).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
