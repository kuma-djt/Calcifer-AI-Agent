import os
from openai import OpenAI

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def chat(self, model: str, messages: list[dict], temperature: float = 0.2) -> str:
        resp = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        return resp.choices[0].message.content
