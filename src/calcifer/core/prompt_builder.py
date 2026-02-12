from pathlib import Path

def load_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")

def build_messages(user_text: str) -> list[dict]:
    identity = load_text("config/IDENTITY.md")
    memory = load_text("memory/MEMORY.md")

    system = f"{identity}\n\nLong-term memory:\n{memory}"
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user_text},
    ]
