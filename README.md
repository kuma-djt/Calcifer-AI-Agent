# Calcifer — Local-First Governance-First AI Agent

Calcifer is an MVP agent with a local FastAPI backend and separate React UI. It uses deterministic skills, explicit approval gating for risky actions, and markdown-based memory journaling.

## Repository layout

- `apps/api` — FastAPI app (`/health`, `/chat`, `/approve`)
- `apps/ui` — React + Vite chat UI
- `src/calcifer` — packaged runtime code (core + adapters + deterministic skills)
- `memory` — long-term memory + daily journals
- `tests` — governance and routing tests

## Windows PowerShell (fresh-clone reliable)

```powershell
py -m venv .venv
Set-ExecutionPolicy -Scope Process Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip setuptools wheel
python -m pip install -e ".[dev]"
python -m pytest -q
```

If your environment blocks build-isolation downloads, retry install with:

```powershell
python -m pip install -e ".[dev]" --no-build-isolation
```

## Environment file

```powershell
Copy-Item .env.example .env
```

Set at least:

- `CALCIFER_API_TOKEN`
- Optional: `OPENAI_API_KEY`

## Run API

```powershell
$env:CALCIFER_API_TOKEN="change-me"
python -m uvicorn apps.api.app:app --host 127.0.0.1 --port 8000 --reload
```

## Run API smoke demo (no UI required)

```powershell
$env:CALCIFER_API_TOKEN="change-me"
python scripts/smoke_api.py
```

The smoke script demonstrates normal chat, approval gating, and approval execution using `/chat` and `/approve`.

## Optional UI install/run

```powershell
cd apps/ui
npm install
$env:VITE_API_BASE_URL="http://127.0.0.1:8000"
$env:VITE_API_TOKEN="change-me"
npm run dev -- --host 127.0.0.1 --port 5173
```

If `npm install` is blocked in your environment, you can still demo the backend with `scripts/smoke_api.py`.
