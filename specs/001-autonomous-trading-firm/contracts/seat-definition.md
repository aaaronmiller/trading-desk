---
date: 2026-10-22 08:37:18 UTC
ver: 1.0.0
author: Claude Code session (system-derived)
model: Claude (Claude Code session)
tags: [contract, seat-definition, canonical-firm, harness-neutral]
layer: derived
---
# Contract: canonical seat definition

Clauses: SPEC-001, SPEC-002, SPEC-005, SPEC-013 to SPEC-017, SPEC-161. Source of truth: `firm/seats/<id>.md`. Generated harness files never feed back into this file.

## File shape

YAML frontmatter followed by a Markdown body with exactly these H2 sections, in order: `Mission`, `Responsibilities`, `Inputs`, `Outputs`, `Authority`, `Handoffs`, `Cadence`, `Boundaries`, `Procedure`, `Output template`. The loader rejects a file missing any section (SPEC-001). `Cadence` in the body only names the runtime manifest key; numeric cadence, budget and escalation values are forbidden in prose (SPEC-017).

## Frontmatter (Zod schema in `packages/registry/src/seat.ts`)

```ts
type SeatDefinition = {
  schema: "seats/v1";
  id: string;                 // ^[a-z0-9-]{1,64}$
  title: string;
  reports_to: string | "owners";        // seat id; internal-audit reports to "owners"
  group: "office" | "investment" | "challenge" | "risk" | "compliance" | "operations" | "education" | "audit";
  instances?: "single" | "per-persona" | "per-strategy" | "pool";
  authority_classes: Array<"read" | "write_paths" | "network" | "order_release" | "booking" | "publish_nav" | "spawn" | "owner_reply">;
  write_paths?: string[];     // glob allowlist when write_paths is granted
  may_spawn?: string[];       // seat ids this seat may delegate to
  tools: string[];            // tool ids from contracts/tool-catalog.md; checked against authority classes
  skills: string[];           // skill folder names under firm/skills
  rules: string[];            // rule file names under firm/rules
  outputs: Array<{ name: string; contract: string }>;  // contract = schema id in packages/agents/src/contracts
  route: "bulk" | "typed" | "review" | "advocate-a" | "advocate-b" | "judge" | "deep-dive";
  family_constraint?: "differs-from-proposer";
  manifest_key: string;       // key in firm/manifest/runtime.yaml (cadence, budget share, escalation)
  must_not: string[];         // human-readable prohibitions, compiled into every harness
  provenance?: Array<{ repo: string; commit: string; file: string; license: string }>;  // upstream text sources
};
```

Validation: `reports_to` must resolve (no cycles, at most 6 hops to the chief executive); `tools` must be grantable under `authority_classes` (for example `order.submit` requires `order_release`); only the execution trader seat type may hold `order_release`; only fund accounting may hold `booking`; only the controller may hold `publish_nav`.

## Example (abridged)

```markdown
---
schema: seats/v1
id: chief-risk-officer
title: Chief Risk Officer
reports_to: chief-executive
group: risk
authority_classes: [read, write_paths]
write_paths: ["records/risk/**"]
tools: [market.snapshot, book.state, risk.limits, risk.exposure, prediction.graph, record.write]
skills: [limit-check, drawdown-ladder, stress-scenarios]
rules: [no-simulation-language, numeric-grounding, untrusted-content]
outputs: [{ name: risk_verdict, contract: risk-verdict/v1 }]
route: review
family_constraint: differs-from-proposer
manifest_key: chief-risk-officer
must_not: ["place, cancel or size orders", "change limits or ceilings", "approve your own analysis"]
---
## Mission
Keep every book inside its limits and the firm inside the owners' envelope.
## Responsibilities
...
## Output template
...
```

## Generated targets (see `harness-capability-matrix.md`)

Each generated file carries `source_hash: <sha256 of the canonical file and its skills and rules>` in a comment or field; `bun run firm:check` regenerates in memory and fails on any byte difference (SPEC-013).
