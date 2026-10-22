---
date: 2026-10-22 08:37:18 UTC
ver: 1.0.0
author: Claude Code session (system-derived)
model: Claude (Claude Code session)
tags: [contract, harness, capability-matrix, compilers, claude-code, roo-code]
layer: derived
---
# Contract: harness capability matrix and generated workspaces

Clauses: SPEC-013 to SPEC-016, SPEC-020. Source: R04 sections 8.2 and 8.3 (field formats read from pinned source; verify field names against current documentation at build). Generators live in `packages/compilers/src/<harness>.ts`; output goes to `harness/workspaces/<harness>/`, each a ready workspace with an MCP configuration pointing at `apps/mcp`.

| Canonical field | Claude Code | Roo Code | OpenCode | Codex | oh-my-pi | Agent Companies (Paperclip) |
|---|---|---|---|---|---|---|
| id | `name` | `slug` | agent key or file name | role key and name | `name` | `agents/<slug>/` |
| title | prose | `name` | prose | prose | prose | `title` |
| mission | `description` plus body | `roleDefinition` | `description` | `description` | `description` | `description` |
| body sections | system prompt body | `customInstructions` plus `.roo/rules-<slug>/` | prompt body | `developer_instructions` | body | `AGENTS.md` body |
| tools and authority | `tools`, `disallowedTools`; write paths via a PreToolUse hook | `groups` with edit `fileRegex`; built-in delegation tools cannot be removed (prohibition written into instructions; reported gap) | permission map | role config keys (verify) | `tools`, `spawns` | sidecar adapter and permissions (verify) |
| route (model tier) | `model` | not expressible (reported gap) | `model` | `model` | model role alias | `adapter.config.model` |
| skills | skill folders and `skills` | rules directories (gap: no native skills) | skills folders | skills folders | skills folders | skills listed in `AGENTS.md` |
| outputs contract | prose (gap) | prose (gap) | prose (gap) | prose (gap) | `output` schema | prose (gap) |
| cadence, budget, escalation | not in file (runtime manifest; gap) | gap | `steps` as iteration cap only | gap | gap (verify) | heartbeat, budgets, routines in `.paperclip.yaml` |
| handoffs | Agent tool | `new_task` | Task tool | spawn by role (verify) | task `agent` | `reportsTo`, task assignee |

Generated layout:

```
harness/workspaces/
├── claude-code/.claude/agents/<id>.md, .claude/skills/<skill>/SKILL.md, .claude/settings.json (write-path hooks), .mcp.json, CLAUDE.md
├── roo-code/.roomodes, .roo/rules-<id>/*.md, .roo/mcp.json
├── opencode/.opencode/agent/<id>.md, opencode.json
├── codex/.codex/agents/<id>.toml, AGENTS.md, config.toml fragment
├── oh-my-pi/.omp/agents/<id>.md
└── agent-companies/COMPANY.md, teams/*/TEAM.md, agents/<id>/AGENTS.md, skills/*/SKILL.md, .paperclip.yaml
```

The generation report (`harness/workspaces/CAPABILITIES.md`) lists, per harness and seat, every declared feature the harness cannot express (SPEC-015). Generated workspaces never live under the repository's own `.claude/` so the build session's harness does not load firm seats by accident.
