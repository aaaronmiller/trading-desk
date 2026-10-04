#!/usr/bin/env python3
"""Offline evals for the date-clamp contract (no API keys, no network).

Each test is a keyless fixture check against SPEC-005/006/007's behavior.
Run:  python3 test_date_clamp.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from date_clamp import as_of, clamp_window, coverage_gaps, feed_status, in_window

PASS = []
FAIL = []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name + (f" — {detail}" if detail and not cond else ""))


# --- EVAL-005: no future-dated data in historical runs ---
# Fixture: one future-dated item per feed, decision date 2026-06-15.
feeds = {
    "news": [
        {"id": "n1", "date": "2026-06-10", "text": "earnings beat"},
        {"id": "n2", "date": "2026-07-01", "text": "FUTURE: merger announced"},
    ],
    "social": [
        {"id": "s1", "date": "2026-06-12", "text": "bullish"},
        {"id": "s2", "date": "2026-08-20", "text": "FUTURE: CEO resigns"},
    ],
    "prices": [
        {"id": "p1", "date": "2026-06-14", "close": 100.0},
        {"id": "p2", "date": "2026-06-16", "close": 120.0},  # future
    ],
}
decision_date = "2026-06-15"
record = {}
for feed, items in feeds.items():
    start, end = clamp_window("2026-06-01", "2026-06-30", decision_date)
    record[feed] = in_window(items, start, end, window_reaches_present=False)
leaked = [i["id"] for items in record.values() for i in items if "FUTURE" in str(i)]
check("EVAL-005 no future-dated item in decision record", leaked == [], f"leaked={leaked}")
check("EVAL-005 window end clamped to decision date", end == decision_date, f"end={end}")

# --- EVAL-006: undated items excluded from past windows ---
items = [
    {"id": "u1", "date": None, "text": "undated rumor"},
    {"id": "d1", "date": "2026-06-10", "text": "dated news"},
]
kept = in_window(items, "2026-06-01", "2026-06-15", window_reaches_present=False)
check("EVAL-006 undated item excluded from past window",
      [i["id"] for i in kept] == ["d1"], f"kept={[i['id'] for i in kept]}")
kept_live = in_window(items, "2026-06-01", "2026-10-03", window_reaches_present=True)
check("EVAL-006 undated item kept when window reaches present",
      sorted(i["id"] for i in kept_live) == ["d1", "u1"])

# --- EVAL-007: coverage gaps labeled unavailable, not empty ---
# Feed whose coverage starts after the window start.
gaps = coverage_gaps("2026-01-01", "2026-06-30", [("2026-04-01", "2026-06-30")])
check("EVAL-007 gap detected at window start", gaps == [("2026-01-01", "2026-04-01")],
      f"gaps={gaps}")
status = feed_status("2026-01-01", "2026-06-30", [("2026-04-01", "2026-06-30")])
check("EVAL-007 labeled unavailable, not empty", status.startswith("unavailable:"),
      f"status={status}")
check("EVAL-007 fully covered window is ok",
      feed_status("2026-01-01", "2026-06-30",
                  [("2026-01-01", "2026-03-31"), ("2026-03-31", "2026-06-30")]) == "ok")
check("EVAL-007 mid-window gap", ("2026-03-31", "2026-05-01") in
      coverage_gaps("2026-01-01", "2026-06-30",
                    [("2026-01-01", "2026-03-31"), ("2026-05-01", "2026-06-30")]))

# --- as_of sanity ---
check("as_of clamps later dates", as_of("2026-12-01", "2026-06-15") == "2026-06-15")
check("as_of passes earlier dates", as_of("2026-05-01", "2026-06-15") == "2026-05-01")

print(f"\n{len(PASS)} passed, {len(FAIL)} failed")
sys.exit(1 if FAIL else 0)
