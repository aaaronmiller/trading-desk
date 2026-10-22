---
date: 2026-10-22 08:37:18 UTC
ver: 1.0.0
author: Claude Code session (system-derived)
model: Claude (Claude Code session)
tags: [contract, plan-language, expression-grammar, compiler]
layer: derived
---
# Contract: plan language

Clauses: SPEC-048, SPEC-053 to SPEC-062, SPEC-059. Implemented in `packages/plan`. A compiled plan is data; nothing in it is executed as code.

## Compiled plan (Zod schema `plan/v1`)

```ts
type CompiledPlan = {
  schema: "plan/v1";
  id: string; version: number; book_id: string; author_seat: string; source_text_ref: string;
  kind: "single" | "multi-in-class" | "cross-asset" | "allocation";
  thesis: string;                         // one paragraph, grounded
  legs: Array<{
    leg: number;
    instrument: string;                   // must exist and be enabled
    direction: "long" | "short";
    form: "spot" | "short-sale" | "inverse-fund" | "call" | "put" | "perpetual" | "event-yes" | "event-no";
    entry: { type: "market" | "limit" | "stop"; level?: Price; when?: Expr; tif: "day" | "gtc" | "ioc" };
    exits: { stop: Price; target?: Price; trail?: { atr_multiple: number }; time_stop?: string; when?: Expr };
    sizing: { rule: "heat-kelly" | "fixed-risk" | "target-weight"; risk_fraction?: number; weight?: number };
  }>;
  allocation?: Array<{ instrument: string; target_weight: number }>;   // kind = allocation
  risk_rules: { max_loss_minor: string; invalidation?: Expr };
  schedule: { review_every: string; expires_at?: string };
  predictions: string[];                  // prediction ids committed with the plan
  grounding: { analysis_refs: string[]; price_levels: Array<{ value: Price; analysis_ref: string }> };
};
type Price = string;                      // decimal string at the instrument's scale
type Expr = string;                       // parsed by the grammar below
```

Compilation checks (each failure returns `{ code, field, message }`): instrument exists and its class is enabled; the form is available for the instrument (SPEC-059); levels are absolute prices present in `grounding.price_levels` (SPEC-057); stop is on the loss side of entry; persona constraints hold (SPEC-048); size within limits at the book's heat; schedule fits the calendar; at least one linked prediction; expressions parse and type-check.

## Expression grammar

```
expr     := or
or       := and ( "or" and )*
and      := not ( "and" not )*
not      := "not" not | cmp
cmp      := sum ( ( "<" | "<=" | ">" | ">=" | "==" | "!=" ) sum )?
sum      := prod ( ( "+" | "-" ) prod )*
prod     := unary ( ( "*" | "/" ) unary )*
unary    := "-" unary | atom
atom     := number | duration | symbol | call | "(" expr ")"
call     := fname "(" args? ")"
args     := expr ( "," expr )*
symbol   := /[A-Z0-9]{1,12}(-[A-Z0-9]{1,12})?/      (instrument symbols only)
duration := /[0-9]+(m|h|d|w)/
```

Whitelisted functions (arity, return type): `price(sym)`, `bar(sym, field, interval, offset)`, `sma(sym, n, interval)`, `ema(sym, n, interval)`, `rsi(sym, n, interval)`, `atr(sym, n, interval)`, `zscore(sym, n, interval)`, `change(sym, window)`, `funding(sym)`, `basis(sym)`, `spread(sym)`, `iv(sym, expiry, strike)`, `time()`, `between(x, lo, hi)`, `crosses_above(a, b)`, `crosses_below(a, b)`. No member access, no assignment, no string literals, maximum depth 12, maximum length 512 characters. Unknown names fail compilation (SPEC-055).
