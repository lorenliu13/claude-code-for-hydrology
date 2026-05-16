# Exercise 6: Write-then-Review with Subagents

**Best practice:** Ask Claude Code to orchestrate two isolated subagents — one writes the code, another reviews it independently.

---

## What are subagents?

A subagent is a separate Claude call with its own clean context window. Claude Code can spawn them internally via its Agent tool. You control what each subagent sees by describing the boundary in your prompt.

```
Claude Code (parent)
  │
  ├─► coder subagent    receives: task only        → writes code
  └─► reviewer subagent receives: task + code only → writes review
```

The reviewer gets no coder reasoning — only the finished code. This mirrors a real code review.

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

Note which tests fail, then clear context and try the subagent approach.

---

## After: two subagents in Claude Code

Clear context (`/clear`), then paste this prompt:

```
Use two subagents in sequence:

1. Coder subagent: implement fit_lp3(flows: list[float]) -> dict that fits a
   Log-Pearson Type III distribution to annual maximum streamflow data and
   returns 2, 10, 50, and 100-year return period discharge estimates using
   numpy and scipy.stats. Return only the Python code.

2. Reviewer subagent: pass it the task description and the code from step 1 —
   nothing else. Ask it to review for LP3 correctness, edge cases (zero or
   negative flows, records shorter than 10 observations), and code quality.

Show me the reviewer's feedback, then write the final code to
06_subagent_review/lp3_frequency.py.
```

Then validate:

```bash
python -m pytest 06_subagent_review/test_lp3_frequency.py -v
```

---

## What to notice

The reviewer subagent starts with a blank slate — it has no memory of how the coder reasoned or what it considered. It evaluates the code on its own merits, which surfaces issues the coder glossed over.

Compare the reviewer's feedback to the test failures from the "before" run. They should overlap: the reviewer catches the same gaps the tests expose.
