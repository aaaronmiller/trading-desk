---
date: 2026-10-22 08:37:18 UTC
ver: 1.0.0
author: Claude Code session (system-derived)
model: Claude (Claude Code session)
tags: [contract, order-interface, venue-port, virtual-market, live-adapters]
layer: derived
---
# Contract: order interface shared by the virtual market and live adapters

Clauses: SPEC-063 to SPEC-072, SPEC-069, SPEC-111, SPEC-145 to SPEC-150. Implemented by `packages/market/src/virtual-venue.ts` and `packages/market/src/live/{coinbase,alpaca,kalshi}.ts`. Seats never see which implementation serves them.

```ts
interface VenuePort {
  readonly name: string;                                   // never contains mode words in agent-facing output
  submit(order: OrderRequest, ctx: SubmitContext): Promise<OrderAck>;
  cancel(orderId: string, ctx: SubmitContext): Promise<CancelAck>;
  status(orderId: string): Promise<OrderState>;
  fills(orderId: string): Promise<Fill[]>;
  positions(bookId: string): Promise<PositionView[]>;
  balances(bookId: string): Promise<BalanceView[]>;
  permissions?(): Promise<{ trade: boolean; withdraw: boolean }>;   // live adapters only (SPEC-148)
}

type OrderRequest = {
  id: string;                     // deterministic: sha256(cycleId|planId|planVersion|leg).slice(0,24)
  book_id: string; instrument: string; side: "buy" | "sell" | "sell_short" | "buy_to_cover";
  type: "market" | "limit" | "stop" | "stop_limit"; qty: string; limit_px?: string; stop_px?: string;
  tif: "day" | "gtc" | "ioc"; decided_at: string;          // fills only at prices observed after decided_at (SPEC-027)
};
type SubmitContext = { actor: "seat:execution-trader"; cycle_id: string; live_enabled: boolean; envelope_version: number };
type OrderAck = { id: string; accepted: boolean; state: OrderStatus; reasons?: Reason[] };
type OrderStatus = "new" | "working" | "partially_filled" | "filled" | "canceled" | "rejected";
type Fill = { id: string; order_id: string; seq: number; qty: string; price: string; fee_minor: string; slippage: string; at: string; liquidity_ref: string };
type Reason = { code: "market_closed" | "stale_price" | "limit_breach" | "restricted" | "regulator_order" | "conduct" | "insufficient_funds" | "venue_reject" | "invalid"; detail: string };
```

## Behavioral rules

- Idempotency: a repeated `submit` with the same `id` returns the original acknowledgment and creates nothing.
- Pre-submission checks run in BookDesk before any implementation is called: calendar (SPEC-026), staleness (SPEC-072), hard limits (SPEC-076), restricted list and regulator orders (SPEC-080, SPEC-163), conduct patterns (SPEC-111).
- Live adapters set production and sandbox base URLs explicitly; production is unreachable unless `ctx.live_enabled` is true and the envelope version matches the operator's change event (SPEC-146, SPEC-147).
- Virtual fills follow plan CTX-004 and CTX-005 cost models; the same random seed and prices yield identical fills (SPEC-070).

## Contract test suite (`tests/contract/venue-port.test.ts`)

Runs unchanged against the virtual venue and each live adapter backed by recorded responses: idempotent submit; reject on closed market; partial fill and remainder; cancel of working order; fee and slippage fields present; stale-price refusal; restricted-asset refusal; conduct refusal; status and fills consistency; positions and balances after fills; permission check refusal when withdrawal is allowed.
