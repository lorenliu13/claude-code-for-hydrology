# Exercise 6: Write-Review-Revise Loop with Subagents

**Best practice:** Orchestrate a coder and a reviewer subagent in a feedback loop — the reviewer's comments go back to the coder, who revises, until the reviewer is satisfied.

---

## What are subagents?

A subagent is a separate Claude call with its own clean context window. Claude Code can spawn them internally via its Agent tool. You control what each subagent sees by describing the boundary in your prompt.

```
Claude Code (parent — orchestrates the loop)
  │
  ├─► coder subagent    receives: task [+ reviewer feedback]  → writes/revises code
  ├─► reviewer subagent receives: task + code only            → approves or lists issues
  ├─► coder subagent    receives: original task + issues      → revises code
  ├─► reviewer subagent receives: task + revised code         → approves or lists issues
  └─► (repeat up to 3 rounds, then write final file)
```

Each reviewer call starts fresh — it only sees the task description and the current code, never the coder's reasoning or previous rounds. This mirrors a real pull-request review cycle.

---

## Before: ask Claude directly

Paste this into Claude Code:

```
Write a Python function fit_lp3(flows: list[float]) -> dict that fits a
Log-Pearson Type III distribution to annual maximum streamflow data and
returns the 2, 10, 50, and 100-year return period discharge estimates.
Use numpy and scipy.stats.
```

You get code — but Claude wrote and "reviewed" it in the same context. It anchors to its own reasoning and tends to miss the same edge cases it introduced.

Save the output to `lp3_frequency.py` and run the tests:

```bash
python -m pytest 06_subagent_review/test_lp3_frequency.py -v
```

Note which tests fail, then clear context and try the subagent loop approach.

---

## After: coder–reviewer feedback loop

Clear context (`/clear`), then paste this prompt:

```
Orchestrate a coder subagent and a reviewer subagent in a feedback loop.
Run up to 3 rounds. Stop early if the reviewer approves with no blocking issues.

Task for the coder:
  Implement fit_lp3(flows: list[float]) -> dict that fits a Log-Pearson Type III
  distribution to annual maximum streamflow data and returns 2, 10, 50, and
  100-year return period discharge estimates using numpy and scipy.stats.

Loop:
  Round N:
  1. Coder subagent — give it: the task description above + any reviewer feedback
     from the previous round (nothing on round 1). It returns only Python code.
  2. Reviewer subagent — give it: the task description + the coder's code.
     Nothing else — no coder reasoning, no previous rounds.
     It must either:
       (a) Write "APPROVED" and stop, or
       (b) List specific blocking issues (LP3 correctness, edge cases for zero/
           negative flows and records shorter than 10 observations, code quality).
  3. If the reviewer wrote "APPROVED", exit the loop.
     Otherwise feed the issue list back to the coder for the next round.

After the loop ends, write the final code to 06_subagent_review/lp3_frequency.py
and report how many rounds it took and what changed each round.
```

Then validate:

```bash
python -m pytest 06_subagent_review/test_lp3_frequency.py -v
```

---

## What to notice

- **Each reviewer call is stateless** — it sees only the current code, so it can't be biased by the coder's intent or previous drafts. Issues it finds are real issues.
- **The coder improves directionally** — it receives the reviewer's exact complaints and addresses them, rather than guessing what was wrong.
- **Early exit matters** — if the reviewer approves after round 1, there's no reason to run round 2. The loop stops as soon as the code is good enough.
- **Round count is a signal** — one round means the coder got it mostly right; three rounds means the task had real edge-case complexity.

Compare the final code to the single-shot "before" version. The loop version should handle zero flows, short records, and negative skew — the cases the tests exercise.
