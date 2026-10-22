task: T000
status: pass
summary: One or two sentences on what the gate proved.
commands:
  - cmd: bun test packages/example
    exit: 0
    output_sha256: 0000000000000000000000000000000000000000000000000000000000000000
artifacts:
  - packages/example/src/index.ts: 0000000000000000000000000000000000000000000000000000000000000000
recorded_at: 2026-01-01T00:00:00Z

Notes: key output lines (counts, pass totals), anything skipped and why, follow-ups.

How to record: run each gate command with its output captured, for example
`bun test packages/example 2>&1 | tee /tmp/out.txt; echo "exit=${PIPESTATUS[0]}"`,
then `sha256sum /tmp/out.txt`. Copy this file to
`specs/001-autonomous-trading-firm/evidence/T###.md`, fill it in, append a ledger entry
naming the task, overwrite standing, then check the task in tasks.md.
