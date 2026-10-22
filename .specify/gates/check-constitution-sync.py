#!/usr/bin/env python3
"""Keep the constitution copy in CLAUDE.md and the plan's Constitution Check honest.

1. The block between the CONSTITUTION markers in CLAUDE.md must equal
   .specify/memory/constitution.md byte for byte (the canonical file is the only
   editable copy; the inlined block exists so the text survives context compaction).
2. plan.md's Constitution Check must name every '### ' principle heading of the
   constitution exactly once, each with PASS, FAIL or N/A.

Usage: python3 .specify/gates/check-constitution-sync.py [--write]
--write regenerates the CLAUDE.md block from the canonical file (never the reverse).
Exit codes: 0 in sync; 1 drift found; 2 file error.
"""

import re
import sys
from pathlib import Path

BEGIN = "<!-- CONSTITUTION:BEGIN (generated from .specify/memory/constitution.md; do not edit here) -->"
END = "<!-- CONSTITUTION:END -->"


def root() -> Path:
    here = Path.cwd().resolve()
    for d in [here, *here.parents]:
        if (d / ".specify" / "memory" / "constitution.md").is_file():
            return d
    return here


def main() -> int:
    r = root()
    try:
        canon = (r / ".specify" / "memory" / "constitution.md").read_text(encoding="utf-8")
        claude_path = r / "CLAUDE.md"
        claude = claude_path.read_text(encoding="utf-8")
        plan = (r / "specs" / "001-autonomous-trading-firm" / "plan.md").read_text(encoding="utf-8")
    except OSError as exc:
        print(f"check-constitution-sync: {exc}", file=sys.stderr)
        return 2
    if "--write" in sys.argv[1:]:
        pattern = re.compile(re.escape(BEGIN) + r"\n.*?\n" + re.escape(END), re.S)
        new_block = f"{BEGIN}\n{canon.rstrip()}\n{END}"
        if not pattern.search(claude):
            print("CLAUDE.md has no constitution markers", file=sys.stderr)
            return 2
        claude_path.write_text(pattern.sub(lambda _m: new_block, claude), encoding="utf-8")
        print("CLAUDE.md constitution block regenerated.")
        return 0
    errors = []
    m = re.search(re.escape(BEGIN) + r"\n(.*?)\n" + re.escape(END), claude, re.S)
    if not m:
        errors.append("CLAUDE.md lacks the constitution block markers")
    elif m.group(1).rstrip() != canon.rstrip():
        errors.append("CLAUDE.md constitution block differs from .specify/memory/constitution.md (run with --write)")
    headings = [h.strip() for h in re.findall(r"^### (.+)$", canon, re.M)]
    for h in headings:
        rows = [line for line in plan.splitlines() if line.startswith(f"| {h} |")]
        if len(rows) != 1:
            errors.append(f"plan.md Constitution Check lists '{h}' {len(rows)} times (expected 1)")
        elif not re.search(r"\| (PASS|FAIL|N/A) \|", rows[0]):
            errors.append(f"plan.md Constitution Check row for '{h}' lacks PASS, FAIL or N/A")
    listed = [line.split("|")[1].strip() for line in plan.splitlines()
              if re.match(r"^\| [IVX]+\. ", line)]
    for name in listed:
        if name not in headings:
            errors.append(f"plan.md Constitution Check lists '{name}', which is not a constitution heading")
    if errors:
        print("Constitution sync gate FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print(f"Constitution sync gate passed ({len(headings)} principles).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
