# AGENTS.md — Calcifer Repo Rules (for Codex + contributors)

You are working in the **Calcifer** repository. Follow these rules every time.

## Mission
Build a **local-first household AI agent** with:
- a Python backend (agent runtime + API)
- a separate local UI app
- strong safety controls (approvals + audit logs)
- minimal dependencies and clean structure

## Non-negotiables
- **Never commit secrets** (API keys, tokens, passwords). Use `.env` locally and commit only `.env.example`.
- **Small, reviewable diffs**. Prefer incremental PRs over “big bang” rewrites.
- **Tests required** for memory logging, approvals, and tool routing.
- **Windows-friendly** commands and paths must work.

## Repo structure contract
- `apps/api/` → FastAPI backend (endpoints, auth, CORS)
- `apps/ui/` → Separate UI (React/Vite or Next, decided by repo)
- `src/core/` → orchestration (turn loop, prompt builder, approvals, tool router)
- `src/adapters/` → integrations (LLM client, storage/journal)
- `skills/` → deterministic capabilities (pure functions + schemas + docs)
- `config/` → identity/policy files (Markdown/YAML)
- `memory/` → user-owned logs (daily + curated)
- `tests/` → pytest tests
- `docs/` → architecture + demo instructions

If structure differs, propose changes first; do not silently reorganize everything.

## Security & governance rules
- **Default deny** for risky actions. Examples:
  - sending texts/emails
  - purchases/payments
  - shell execution
  - filesystem writes outside `memory/`
- Implement **approvals** for any risky tool:
  - model may propose → user must approve → then execute
- Maintain an **audit trail**:
  - append every turn to `memory/YYYY-MM-DD.md`
  - log tool requests + results (including blocked attempts)
- Keep services **local by default**:
  - bind to `127.0.0.1`
  - CORS only for local UI origin(s)

## LLM integration rules
- All LLM calls must live under: `src/adapters/llm/`
- The runtime must be provider-agnostic where feasible.
- Never hardcode model keys; use env vars (e.g., `OPENAI_API_KEY`).

## API + UI rules
- API token auth via env var (e.g., `CALCIFER_API_TOKEN`).
- UI must store a `session_id` (localStorage) and handle approvals.
- Keep UI simple; avoid heavy frameworks unless needed.

## Definition of Done (MVP)
- `pytest` passes
- API runs locally and responds:
  - `GET /health`
  - `POST /chat`
  - `POST /approve` (if approvals implemented)
- Memory journaling writes to `memory/YYYY-MM-DD.md`
- At least 2 deterministic skills work end-to-end
- README includes exact run/test commands

## Working style
- If unsure, propose 2–3 options and pick the simplest.
- Prefer standard library + minimal deps.
- Update docs when adding major components.

End.
