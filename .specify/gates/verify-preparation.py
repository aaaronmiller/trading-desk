#!/usr/bin/env python3
"""Verify the preparation receipt before trusting prepared artifacts.

Reads preparation.json at the repository root, checks lifecycle, that every gate record
passed, and that every listed artifact still hashes to its recorded sha256. A changed
immutable artifact invalidates the receipt (artifacts marked mutable, such as tasks.md and
the ledger, are expected to change once the build starts): the session must re-run the preparation gates (or
record the change as a layer-scoped change request) before relying on it.

Usage:
    python3 .specify/gates/verify-preparation.py [--brief]
--brief prints a short session-start summary and never fails the session (exit 0),
but states clearly when the receipt is stale. Without --brief, a stale or invalid
receipt exits 1.
"""

import hashlib
import json
import sys
from pathlib import Path

REQUIRED_GATES = ("constitution", "prerequisites", "analysis", "traceability")


def root() -> Path:
    here = Path.cwd().resolve()
    for d in [here, *here.parents]:
        if (d / "preparation.json").is_file() and (d / ".specify").is_dir():
            return d
    return here


notes: list[str] = []


def verify(r: Path) -> tuple[list[str], dict]:
    errors: list[str] = []
    receipt = json.loads((r / "preparation.json").read_text(encoding="utf-8"))
    if receipt.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")
    if receipt.get("lifecycle") not in ("specification-prepared", "initiated"):
        errors.append(f"lifecycle is {receipt.get('lifecycle')!r}")
    gates = {g.get("name"): g for g in receipt.get("gates", [])}
    for name in REQUIRED_GATES:
        g = gates.get(name)
        if not g:
            errors.append(f"gate record missing: {name}")
        elif g.get("status") != "passed" or not g.get("evidence") or not g.get("command"):
            errors.append(f"gate {name} lacks passed status, command or evidence")
    for art in receipt.get("artifacts", []):
        p = r / art["path"]
        if not p.is_file():
            errors.append(f"artifact missing: {art['path']}")
            continue
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        if digest != art.get("sha256"):
            if art.get("mutable"):
                notes.append(f"changed as expected during the build: {art['path']}")
            else:
                errors.append(f"artifact changed since preparation: {art['path']}")
    return errors, receipt


def main() -> int:
    brief = "--brief" in sys.argv[1:]
    r = root()
    if not (r / "preparation.json").is_file():
        print("Preparation receipt not found (preparation.json). Treat prepared artifacts as unverified.")
        return 0 if brief else 1
    try:
        errors, receipt = verify(r)
    except (OSError, ValueError, KeyError) as exc:
        print(f"Preparation receipt unreadable: {exc}")
        return 0 if brief else 1
    if brief:
        state = "VALID" if not errors else "STALE"
        print(f"Preparation receipt {state} for {receipt.get('feature')} (prepared {receipt.get('preparedAt')}).")
        print("Read order: reset-handoff.md, then the feature ledger standing and tail, the constitution, intent, spec, plan, tasks.")
        print("Gates: every task needs its gate commands run and evidence recorded; commits are refused while the task evidence gate fails.")
        for e in errors[:10]:
            print(f"  - {e}")
        if notes:
            print(f"  ({len(notes)} mutable artifacts changed since preparation, as expected once tasks start)")
        return 0
    if errors:
        print("Preparation receipt INVALID:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("Preparation receipt valid: lifecycle, four gates and all artifact hashes verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
