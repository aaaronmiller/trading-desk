# Debate Protocol — DRAFT

> Status: draft, written 2026-10-03 (PDT). Captures the behavioral semantics
> of the upstream debate machinery (TauricResearch/TradingAgents @
> `1394a3f72aa4393e1a98f51b382434c4b4c2d972`), which is domain content worth
> preserving even though the graph wiring is not ported. Ratified intent/spec
> still gate the scaffold play.

## Investment debate (bull vs bear)

- The bull and bear each receive the same analyst reports plus the
  conversation history and the opponent's last argument.
- **Empty-opponent handling**: the first speaker receives no opponent text.
  Upstream marks this explicitly ("The bear analyst has not spoken yet —
  open the debate with your own case") rather than interpolating emptiness,
  because interpolating an empty opponent makes the model fabricate the
  other side's position (upstream #1176). The harness must preserve this
  marker.
- Reports are injected verbatim or marked absent via `report_or_absent`:
  a missing report is labeled as missing, never silently dropped or
  zero-filled.
- Each side's argument must quote or restate at least one of the other's
  claims before rebutting (SPEC-002 eval).

## Risk debate (aggressive / conservative / neutral)

- Three stances debate the trader's proposal; each sees the others'
  arguments, the instrument and portfolio context, and the analyst reports.
- The neutral stance is a genuine participant, not a tiebreaker.

## Trader grounding

- The trader receives the research manager's investment plan and — only when
  it has content — the technical market report, with an explicit grounding
  instruction: entry, stop, and sizing levels come from the report's price
  structure (current price, support/resistance, ATR); the plan supplies
  direction (upstream #1167).
- **Entry/stop are absolute price levels in the quote currency** (e.g.
  189.5), never percentages or ranges; convert percentage distances to the
  implied level or omit the field (upstream #1288).
- The trader offers no external-tool claims: its prompt states the
  no-external-tools constraint explicitly rather than relying on the
  binding alone (upstream #1130).

## Portfolio manager

- Synthesizes the risk debate into a single rating on the fixed scale:
  Buy / Overweight / Hold / Underweight / Sell.
- Conflict alone is not a reason to Hold; commit to the stronger case, sized
  by how decisively it wins. Hold only when the evidence is still balanced
  after weighing, or too thin to support a call.
- Analysts are weighed on their merits, independent of speaking order.
- Past lessons are injected when present; structured output is preferred,
  with free-text fallback and the rating re-read from text.

## Research manager

- Digests the investment debate into the plan the trader acts on.

## Analysts (tool-using)

- The analyst keeps tool-calling until its tool rounds are spent, then a
  wrap-up instruction tells it to write the final report from the tool
  results above and state which data it could not retrieve.
- Sentiment analyst is the exception: data is pre-fetched into its prompt
  (news + StockTwits + Reddit blocks, trimmed to the analysis window), and
  its preamble carries the no-external-tools constraint instead of
  tool-range wording.

## Multilingual output

- When the output language is not English, every role writes its entire
  response in that language — except labelled lines ("**Rating**:",
  "FINAL TRANSACTION PROPOSAL:"), which keep their English label and value
  so downstream parsers still find them (upstream #1435).
