from __future__ import annotations


def plan_groceries(text: str) -> str:
    """Generate a deterministic grocery list from common intents."""
    lower = text.lower()
    if "pasta" in lower:
        return "Grocery plan: pasta, tomato sauce, garlic, olive oil, parmesan, spinach."
    if "breakfast" in lower:
        return "Grocery plan: eggs, oats, berries, greek yogurt, whole-grain bread."
    return "Grocery plan: rice, chicken, mixed vegetables, fruit, milk, eggs."
