from adapters.llm.openai_client import OpenAIClient
from core.prompt_builder import build_messages

class Runtime:
    def __init__(self, model="gpt-5.2"):
        self.llm = OpenAIClient()
        self.model = model

    def run_turn(self, user_text: str) -> str:
        messages = build_messages(user_text)
        return self.llm.chat(model=self.model, messages=messages)
