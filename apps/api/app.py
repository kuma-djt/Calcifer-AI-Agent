from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from calcifer.adapters.llm.openai_client import OpenAIClient
from calcifer.adapters.storage.journal import MemoryJournal
from calcifer.core.approvals import ApprovalStore
from calcifer.core.tool_router import ToolCall, ToolRouter

load_dotenv()

REPO_ROOT = Path(__file__).resolve().parents[2]
MEMORY_DIR = REPO_ROOT / "memory"


class ChatRequest(BaseModel):
    session_id: str
    text: str


class ApproveRequest(BaseModel):
    approval_id: str
    approve: bool


class AgentService:
    def __init__(self) -> None:
        self.router = ToolRouter()
        self.approvals = ApprovalStore(storage_path=str(MEMORY_DIR / "approvals.json"))
        self.journal = MemoryJournal(str(MEMORY_DIR))
        self.identity = (REPO_ROOT / "config/IDENTITY.md").read_text(encoding="utf-8")
        self.long_term_memory = (MEMORY_DIR / "MEMORY.md").read_text(encoding="utf-8")
        self.model = os.getenv("OPENAI_MODEL", "gpt-5.2")
        self.llm = OpenAIClient() if os.getenv("OPENAI_API_KEY") else None

    def _fallback_reply(self, text: str) -> str:
        return f"I noted your request: {text}. Ask for groceries or routine planning for deterministic tools."

    def handle_chat(self, text: str) -> dict:
        tool_requests: list[dict] = []
        tool_results: list[dict] = []

        call = self.router.route(text)
        if call and call.risky:
            req = self.approvals.create(call.name, {"text": call.input_text})
            tool_requests.append({"tool": call.name, "input": call.input_text, "risky": True})
            self.journal.append_turn(text, "Approval required before execution.", tool_requests, tool_results)
            return {
                "status": "needs_approval",
                "approval_id": req.approval_id,
                "request": {"tool_name": req.tool_name, "tool_input": req.tool_input},
            }

        if call:
            tool_requests.append({"tool": call.name, "input": call.input_text, "risky": False})
            reply = self.router.execute(call)
            tool_results.append({"tool": call.name, "result": reply})
            self.journal.append_turn(text, reply, tool_requests, tool_results)
            return {"status": "ok", "reply": reply}

        reply = self._fallback_reply(text)
        if self.llm:
            try:
                prompt = (
                    f"{self.identity}\n\nLong-term memory:\n{self.long_term_memory}\n\n"
                    f"User: {text}"
                )
                reply = self.llm.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
            except Exception:
                reply = self._fallback_reply(text)
        self.journal.append_turn(text, reply, tool_requests, tool_results)
        return {"status": "ok", "reply": reply}

    def handle_approve(self, approval_id: str, approve: bool) -> dict:
        req = self.approvals.pop(approval_id)
        if not req:
            raise HTTPException(status_code=404, detail="approval_id not found")

        tool_requests = [{"tool": req.tool_name, "input": req.tool_input, "risky": True, "approval": approve}]
        if not approve:
            reply = "Request denied. No risky action was executed."
            self.journal.append_turn(f"approval:{approval_id}", reply, tool_requests, [])
            return {"status": "ok", "reply": reply}

        call = ToolCall(name=req.tool_name, input_text=req.tool_input.get("text", ""), risky=True)
        result = self.router.execute(call)
        tool_results = [{"tool": req.tool_name, "result": result}]
        self.journal.append_turn(f"approval:{approval_id}", result, tool_requests, tool_results)
        return {"status": "ok", "reply": result}


def get_token(authorization: str | None = Header(default=None)) -> str:
    expected = os.getenv("CALCIFER_API_TOKEN")
    if not expected:
        raise HTTPException(status_code=500, detail="CALCIFER_API_TOKEN not configured")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing bearer token")
    token = authorization.removeprefix("Bearer ").strip()
    if token != expected:
        raise HTTPException(status_code=401, detail="invalid token")
    return token


app = FastAPI(title="Calcifer API")
service = AgentService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health(_: str = Depends(get_token)) -> dict:
    return {"status": "ok"}


@app.post("/chat")
def chat(body: ChatRequest, _: str = Depends(get_token)) -> dict:
    return service.handle_chat(body.text)


@app.post("/approve")
def approve(body: ApproveRequest, _: str = Depends(get_token)) -> dict:
    return service.handle_approve(body.approval_id, body.approve)
