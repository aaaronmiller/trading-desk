#!/usr/bin/env python3
"""Refuse task completion without recorded evidence (constitution Principle IX).

A task in tasks.md is complete only when it is checked ("- [X] T123" or "- [x] T123")
AND specs/<feature>/evidence/T123.md exists with the required fields:

    task: T123
    status: pass
    commands:
      - cmd: <command that was run>
        exit: 0
        output_sha256: <64 hex characters of the captured output>
    artifacts:            (optional list of path: sha256 pairs)
    recorded_at: <ISO 8601 UTC>

and the ledger mentions the task identifier at least once. Unchecked tasks need nothing.

Usage:
    python3 .specify/gates/check-task-evidence.py [--feature DIR] [--task T123]
Exit codes: 0 all checked tasks have evidence; 1 violations found; 2 usage or file error.
Standard library only, so it runs before any project dependency is installed.
"""

import argparse
import re
import sys
from pathlib import Path

TASK_RE = re.compile(r"^\s*-\s*\[(?P<mark>[ xX])\]\s+(?P<id>T\d{3,4})\b", re.MULTILINE)
FIELD_RE = {
    "task": re.compile(r"^task:\s*(T\d{3,4})\s*$", re.MULTILINE),
    "status": re.compile(r"^status:\s*(pass)\s*$", re.MULTILINE),
    "recorded_at": re.compile(r"^recorded_at:\s*\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?(\.\d+)?Z\s*$", re.MULTILINE),
}
CMD_RE = re.compile(r"-\s*cmd:\s*(?P<cmd>.+?)\s*\n\s*exit:\s*(?P<exit>-?\d+)\s*\n\s*output_sha256:\s*(?P<sha>[0-9a-f]{64})\s*$", re.MULTILINE)


def repo_root(start: Path) -> Path:
    for d in [start, *start.parents]:
        if (d / ".specify").is_dir():
            return d
    return start


def check(feature: Path, only: str | None) -> list[str]:
    tasks_file = feature / "tasks.md"
    if not tasks_file.is_file():
        raise FileNotFoundError(f"missing {tasks_file}")
    tasks = tasks_file.read_text(encoding="utf-8")
    ledger_file = feature / "ledger" / "ledger.md"
    ledger = ledger_file.read_text(encoding="utf-8") if ledger_file.is_file() else ""
    errors: list[str] = []
    seen: set[str] = set()
    for m in TASK_RE.finditer(tasks):
        tid = m.group("id")
        if tid in seen:
            errors.append(f"{tid}: duplicate task identifier in tasks.md")
        seen.add(tid)
        if only and tid != only:
            continue
        if m.group("mark") == " ":
            continue
        ev = feature / "evidence" / f"{tid}.md"
        if not ev.is_file():
            errors.append(f"{tid}: checked in tasks.md but {ev.relative_to(feature)} is missing")
            continue
        body = ev.read_text(encoding="utf-8")
        for name, rx in FIELD_RE.items():
            fm = rx.search(body)
            if not fm:
                errors.append(f"{tid}: evidence lacks a valid '{name}' field")
            elif name == "task" and fm.group(1) != tid:
                errors.append(f"{tid}: evidence names task {fm.group(1)}")
        cmds = list(CMD_RE.finditer(body))
        if not cmds:
            errors.append(f"{tid}: evidence lists no command with exit code and output_sha256")
        for c in cmds:
            if int(c.group("exit")) != 0:
                errors.append(f"{tid}: gate command exited {c.group('exit')}: {c.group('cmd')[:80]}")
        if not re.search(rf"\b{tid}\b", ledger):
            errors.append(f"{tid}: no ledger entry mentions this task")
    if only and only not in seen:
        errors.append(f"{only}: not found in tasks.md")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--feature", default=None, help="feature directory (default: specs/001-autonomous-trading-firm)")
    ap.add_argument("--task", default=None, help="check only this task identifier")
    args = ap.parse_args()
    root = repo_root(Path.cwd().resolve())
    feature = Path(args.feature).resolve() if args.feature else root / "specs" / "001-autonomous-trading-firm"
    try:
        errors = check(feature, args.task)
    except (OSError, ValueError) as exc:
        print(f"check-task-evidence: {exc}", file=sys.stderr)
        return 2
    if errors:
        print("Task evidence gate FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        print("Record evidence (see .specify/gates/evidence-template.md) or uncheck the task.", file=sys.stderr)
        return 1
    print("Task evidence gate passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
