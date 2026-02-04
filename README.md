# Calcifer-AI-Agent
Calcifer is a secure-by-design home operations agent demonstrating AI governance patterns: tool gating, approvals, memory hygiene, auditability, and human-in-the-loop control.

# Calcifer – Home Operations Agent

Calcifer is a **secure-by-design personal AI agent** demonstrating governance patterns relevant to DoD and enterprise agent deployments:

- Tool gating with human approval  
- Memory hygiene (daily vs long-term)  
- Auditable action logs  
- Policy-driven execution  
- Provider-agnostic LLM runtime (GPT-5.2)

## Capabilities (MVP)

- Meal & grocery planning  
- Routine checklists  
- Draft communications (confirm-before-send)  
- Budget awareness  
- Local memory with privacy boundaries

## Architecture

- FastAPI Gateway  
- Agent runtime with tool registry  
- SQLite + file memory  
- Human-in-the-loop approvals

## Security Principles

- No external actions without confirmation  
- Secrets excluded via .gitignore  
- Local-first memory  
- Explicit PII boundaries
