# Paperclip Orchestration Model (summary of upstream concepts)

Summarized from the paperclipai/paperclip README and docs (see SOURCING.md).
This is a faithful summary of the platform's management-layer concepts, not an
invention. Quoted phrases are upstream's.

## Elevator pitch
"If OpenClaw is an employee, Paperclip is the company." A Node.js server +
React UI that orchestrates teams of AI agents as a functioning organization.
Bring-your-own-agent: OpenClaw, Claude Code, Codex, Cursor, Gemini CLI,
OpenCode, Pi, Hermes, Grok Build, Kimi — "if it can receive a heartbeat, it's
hired."

## The four pillars
1. **Agentic Task Manager** — declare intent; agents work; human verifies output.
   Tasks, approvals and review gates, auditable routines.
2. **Org Chart for Agents** — roles, titles, reporting lines, permissions and
   boundaries for humans and agents; delegation and specialization; scoped
   secrets and company boundaries.
3. **Agent Employee Training** — skill studio and shared org-wide skills, evals
   and saved test runs, performance reviews for agents, reusable team templates.
4. **Agentic OS** — cross-provider runtime (any model, any agent), sandboxing,
   MCP integrations, SSO/GRC/RBAC, cost controls, run history and tracing.

## Heartbeats (execution model)
Agents do not wait for chat input. A DB-backed wakeup queue pulses on schedule;
agents wake, check their task queue and shared strategy, execute, log work, and
return to standby. Delegation flows up and down the org chart. This is what
makes 24/7 autonomous operation viable.

## Cost control
Budgets at company, agent, project, goal, and model scope. Spend tracking with
threshold alerts and automatic pauses at configured limits; budget hard-stops
(enforcement uses recorded spend).

## Governance and approvals
Review/approval stages on work; board-style approval workflows for high-risk
actions; agent pause/resume/terminate; config changes revisioned with rollback.
The human sits as the board, not the manager.

## Auditability
Mutating actions, heartbeat state changes, cost events, approvals, comments,
and work products are recorded as durable activity — the full decision history
is replayable.

## Multi-organization
One deployment can host many organizations with separate tasks, agents,
permissions, and histories.

## Relevance to this project
The management layer (org chart, heartbeats, budgets, governance, audit) is
exactly what a live trading operation needs and what a pure research framework
lacks. The trading logic itself is not Paperclip's job — worker agents carry
it. Planned "Clipmart" template marketplace was not live at the fetched commit.
