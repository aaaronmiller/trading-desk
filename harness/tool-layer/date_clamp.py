#!/usr/bin/env python3
"""Date-clamp utilities for the trading-desk harness tool layer.

Implements the point-in-time discipline from
`sources/tradingagents/backtest-methodology.md`:

1. as_of / clamp_window — no tool ever reaches a vendor with a date later
   than the decision date.
2. in_window — dated items are trimmed to the analysis window (upper bound
   exclusive at midnight after `end`); an undated item is kept ONLY when the
   window reaches the present (a backtest cannot prove it isn't from the
   future).
3. coverage_gaps — windows a feed cannot cover are reported as UNAVAILABLE,
   never as empty.

Pure stdlib. No API keys, no network, no trading paths. Test with:
    python3 test_date_clamp.py
"""
from __future__ import annotations

from datetime import date

DATE_FMT = "%Y-%m-%d"


def parse(d: str) -> date:
    return date.fromisoformat(d)


def fmt(d: date) -> str:
    return d.strftime(DATE_FMT)


def as_of(requested: str, decision_date: str) -> str:
    """Clamp a single date: the model never sees later than the decision date."""
    return fmt(min(parse(requested), parse(decision_date)))


def clamp_window(start: str, end: str, decision_date: str) -> tuple[str, str]:
    """Clamp a requested [start, end] window to the decision date.

    The start is never moved forward (the model asked for history); only the
    end is clamped. Returns (start, end) with end <= decision_date.
    """
    s, e, dd = parse(start), parse(end), parse(decision_date)
    return fmt(s), fmt(min(e, dd))


def in_window(
    items: list[dict],
    start: str,
    end: str,
    *,
    window_reaches_present: bool,
    date_key: str = "date",
) -> list[dict]:
    """Trim dated items to the analysis window.

    - Keeps items with start <= date <= end (upper bound inclusive at date
      granularity; the exclusive-midnight rule lives in the vendor fetch).
    - Drops items dated AFTER the window end (future leakage).
    - Drops UNDATED items unless the window reaches the present.
    """
    s, e = parse(start), parse(end)
    kept = []
    for item in items:
        d = item.get(date_key)
        if d is None:
            if window_reaches_present:
                kept.append(item)
            continue
        if s <= parse(d) <= e:
            kept.append(item)
    return kept


def coverage_gaps(
    window_start: str, window_end: str, covered: list[tuple[str, str]]
) -> list[tuple[str, str]]:
    """Return the sub-windows of [window_start, window_end] the feed did NOT cover.

    `covered` is a list of (start, end) ranges the feed actually observed.
    Callers must label every returned gap as UNAVAILABLE, never as empty.
    """
    ws, we = parse(window_start), parse(window_end)
    spans = sorted((parse(s), parse(e)) for s, e in covered)
    gaps: list[tuple[str, str]] = []
    cursor = ws
    for s, e in spans:
        if e < cursor:
            continue
        if s > cursor:
            # gap from cursor up to (but excluding) s, in date granularity
            gaps.append((fmt(cursor), fmt(s)))
        cursor = max(cursor, e)
        if cursor > we:
            break
    if cursor < we:
        gaps.append((fmt(cursor), fmt(we)))
    # merge adjacent / overlapping gaps
    merged: list[tuple[str, str]] = []
    for gs, ge in gaps:
        if merged and merged[-1][1] >= gs:
            merged[-1] = (merged[-1][0], max(merged[-1][1], ge))
        else:
            merged.append((gs, ge))
    return merged


def feed_status(
    window_start: str, window_end: str, covered: list[tuple[str, str]]
) -> str:
    """Human/machine label for a feed over a window: 'ok' or 'unavailable:<gaps>'."""
    gaps = coverage_gaps(window_start, window_end, covered)
    if not gaps:
        return "ok"
    return "unavailable:" + ",".join(f"{s}..{e}" for s, e in gaps)
