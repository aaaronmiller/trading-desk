# trading-desk

An autonomous multi-agent trading desk: specialist research agents, adversarial
debate, risk review, and portfolio approval — run as a governed organization,
not a script. Paper trading first; live capital only after validation.

## The idea

Two proven things, combined:

- **A research lab**: the open-source TradingAgents framework showed that
  role-specialized agents (analysts → bull/bear debate → trader → risk →
  portfolio manager) make better trading decisions than a single agent, and
  established the point-in-time backtest discipline that keeps historical
  evaluation honest. Its orchestration, however, is fused to a graph
  framework, and it has no answer for cost control, approvals, or audit.
- **A management layer**: the Paperclip orchestration model — org charts,
  heartbeat scheduling, per-agent spend budgets with hard stops, approval
  workflows for high-risk actions, and a replayable audit log. It ships no
  trading logic, but it solves the live-money governance problem.

This project extracts the durable domain content from the former (prompts,
tools, evaluation discipline — not the plumbing) and re-houses it as
harness-based agents under the latter's governance.

## Phased plan

1. **Reference paper runs** — run the research framework stock on paper;
   establish the baseline and learn which roles carry signal.
2. **Extract** — move the 12 role prompts, tool schemas, and debate protocol
   into thin harness agents (model + tools + loop + guardrails).
3. **Backtest** — historical evaluation with date-clamped tools:
   no future-dated data, undated items excluded, coverage gaps labeled as
   unavailable (never as empty).
4. **Paper-run** — heartbeat-scheduled trading against a simulated venue
   with budgets, approvals, risk limits, and a full decision log.
5. **Multi-venue** — one adapter per class: stocks, crypto, forex,
   prediction markets.
6. **Live readiness** — only after paper results clear a human-ratified bar.
   No code change enables live trading without it.

> **Paper trading only until validated.** The live-execution path is not
> built in phase 1 by design; the order gateway terminates at a simulated
> venue unless a human has enabled live trading *and* a portfolio approval
> exists for that order.

## Repo layout

```
trading-desk/
  sources/               curated reference extractions (read-only input)
    tradingagents/       12 role prompts, tool inventory, dataflow inventory,
                         backtest methodology, SOURCING.md
    paperclip/           orchestration model summary, trading-firm prompt
                         template, SOURCING.md files
  strata/trading-desk/   project contract: intent, spec, context, plays,
                         ledger, substrate (intent/spec are DRAFT awaiting
                         human ratification)
  strata/evals/          eval manifest (deliberately outside the build tree)
  harness/               (phase 2+) role agents, tool layer, order gateway
```

The strata documents own the contract. `strata-validate.py` enforces it:
zero technology tokens in intent/spec, every spec clause testable with an
EVAL-ID, context in contact with spec, continuity via the ledger.

## Status

Kickoff. Sources curated (22 files); contract authored and validated;
no implementation yet. Three open questions for the operator:

1. What quantitative bar clears the paper-to-live gate?
2. What starting capital per venue class?
3. Which specific venues and accounts?

See `strata/trading-desk/intent.md` section 11.
