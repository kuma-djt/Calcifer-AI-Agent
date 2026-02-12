# Calcifer MVP Architecture

## API layer (`apps/api/app.py`)

- Token-authenticated endpoints.
- CORS scoped to local Vite origins.
- Agent service coordinates routing, approvals, and journaling.

## Runtime primitives (`src/core`)

- `ToolRouter`: deterministic classification and execution.
- `ApprovalStore`: in-memory pending approvals with lock-protected access.

## Adapters (`src/adapters`)

- `MemoryJournal`: appends markdown entries to daily files.
- `OpenAIClient`: optional fallback response generation when key exists.

## Skills (`skills/*`)

- `groceries_planner` and `routine_builder` deterministic functions.

## UI (`apps/ui`)

- Transcript + composer.
- Approval card for risky actions.
- Session persistence via `localStorage`.
