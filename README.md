# Calcifer — Local-First Governance-First AI Agent

Calcifer is an MVP agent with a local FastAPI backend and separate React UI. It uses deterministic skills, explicit approval gating for risky actions, and markdown-based memory journaling.

## Repository layout

- `apps/api` — FastAPI app (`/health`, `/chat`, `/approve`)
- `apps/ui` — React + Vite chat UI
- `src/core` — approvals + tool routing
- `src/adapters` — storage + LLM adapter
- `skills` — deterministic skill implementations
- `memory` — long-term memory + daily journals
- `tests` — governance and routing tests

## Setup

### 1) Create and populate env

```powershell
Copy-Item .env.example .env
```

Set at least:

- `CALCIFER_API_TOKEN`
- `VITE_API_TOKEN` (same value)
- Optional: `OPENAI_API_KEY`

### 2) Install backend dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Install UI dependencies

```powershell
cd apps/ui
npm install
cd ../..
```

## Run API

```powershell
$env:CALCIFER_API_TOKEN="change-me"
python -m uvicorn apps.api.app:app --host 127.0.0.1 --port 8000 --reload
```

## Run UI

```powershell
cd apps/ui
$env:VITE_API_BASE_URL="http://127.0.0.1:8000"
$env:VITE_API_TOKEN="change-me"
npm run dev -- --host 127.0.0.1 --port 5173
```

## Run tests

```powershell
pytest -q
```

## Approvals system

- Risky intents (e.g., purchase/order) are deny-by-default.
- `/chat` returns `needs_approval` with an `approval_id` for risky requests.
- UI displays approval controls and calls `/approve`.
- Journal entries are appended to `memory/YYYY-MM-DD.md` for each turn.

## Demo flow

1. Send: `make me a grocery plan for pasta night`.
2. Observe deterministic groceries response.
3. Send: `purchase paper towels`.
4. Observe approval prompt.
5. Approve or deny and observe audited result.
