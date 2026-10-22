---
date: 2026-10-22 08:37:18 UTC
ver: 1.0.0
author: Claude Code session (system-derived)
model: Claude (Claude Code session)
tags: [contract, model-routes, configuration, budget]
layer: derived
---
# Contract: model routes and budget configuration

Clauses: SPEC-087, SPEC-089, SPEC-092, SPEC-136 to SPEC-139, SPEC-143, SPEC-144. File: `firm/routes/models.yaml`. Code reads routes only through `packages/agents/src/routing.ts`; no model identifier appears elsewhere (SPEC-139, checked by `bun run lint:routes`).

```yaml
schema: routes/v1
active_profile: economy-api
profiles:
  economy-api:
    bulk:       { provider: meta-contributor, model: "<verify at build>", family: meta,     training: allowed,   fallback: review }
    typed:      { provider: typesafe,         model: "<verify at build>", family: jev,      training: unknown,   fallback: bulk }
    review:     { provider: deepseek,         model: "<verify at build>", family: deepseek, training: disallowed, fallback: bulk }
    advocate-a: { route: bulk }
    advocate-b: { route: review }
    judge:      { provider: anthropic,        model: "<latest small Claude model, verify>", family: anthropic, training: disallowed, fallback: none }
    deep-dive:  { provider: anthropic,        model: "<latest Claude Opus model, verify>",  family: anthropic, training: disallowed, fallback: judge }
  subscription:                                # operator opt-in only, recorded change event
    bulk:       { provider: opencode-go, model: "<verify>", family: meta, training: allowed }
providers:
  meta-contributor: { base_url: "<verify>", key_secret: ROUTE_KEY_META, price_in_per_m: "0.10 (verify)", price_out_per_m: "0.20 (verify)", rpm: 100 }
  deepseek:         { base_url: "<verify>", key_secret: ROUTE_KEY_DEEPSEEK, price_in_per_m: "0.15 to 0.30 (verify)", price_out_per_m: "0.60 to 1.20 (verify)" }
  typesafe:         { base_url: "<verify>", key_secret: ROUTE_KEY_JEV, price_in_per_m: "0.042 (verify)", price_out_per_m: "0 (verify)" }
  anthropic:        { base_url: "https://api.anthropic.com", key_secret: ROUTE_KEY_ANTHROPIC }
rules:
  identifiers_in_prompts: forbidden             # SPEC-138
  live_position_data: no-training-routes-only    # SPEC-138
  proposer_reviewer_families: must-differ        # SPEC-092
  tribunal_families: three-distinct              # SPEC-087, SPEC-089
```

Placeholders marked "verify at build" are resolved by task T190 against providers and recorded in the ledger; a route with an unresolved placeholder cannot be activated.

Budget (`firm/manifest/runtime.yaml`): `firm_ceiling_usd_month: 25` (owner setting); seat shares in parts per million; `reserve_essential: 0.20`; throttle order as in plan CTX-010; alert thresholds 0.5 and 0.8; hard stop 1.0 (SPEC-136, SPEC-137).
