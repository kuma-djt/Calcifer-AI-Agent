from __future__ import annotations


def build_routine(text: str) -> str:
    """Generate a deterministic household routine from user intent."""
    lower = text.lower()
    if "morning" in lower:
        return "Routine: wake up, hydrate, 10-min stretch, review tasks, breakfast."
    if "evening" in lower:
        return "Routine: tidy kitchen, prepare next-day plan, read 20 minutes, sleep prep."
    return "Routine: prioritize top 3 tasks, block focus time, reset workspace."
