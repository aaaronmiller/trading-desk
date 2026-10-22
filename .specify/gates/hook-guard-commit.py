#!/usr/bin/env python3
"""Claude Code PreToolUse hook: refuse `git commit` while the task evidence gate fails.

Reads the hook payload (JSON) on stdin. For Bash tool calls whose command runs
`git commit`, it runs check-task-evidence.py; on failure it exits 2 so the harness
blocks the call and shows the gate's message to the agent. Any other tool call, or a
payload it cannot parse, passes through untouched (exit 0), so a malformed payload
never blocks unrelated work.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

COMMIT_RE = re.compile(r"(^|[;&|]\s*|\s)git(\s+-[cC]\s+\S+)*\s+commit\b")


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    if payload.get("tool_name") != "Bash":
        return 0
    command = str((payload.get("tool_input") or {}).get("command", ""))
    if not COMMIT_RE.search(command):
        return 0
    gate = Path(__file__).with_name("check-task-evidence.py")
    cwd = payload.get("cwd") or None
    proc = subprocess.run([sys.executable, "-I", str(gate)], capture_output=True, text=True, cwd=cwd)
    if proc.returncode == 0:
        return 0
    sys.stderr.write(proc.stderr or proc.stdout)
    sys.stderr.write("\nCommit blocked by the constitution's evidence gate (Principle IX).\n")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
