# Exercise 4: Initialize a CLAUDE.md with `/init`

**Best practice:** Run `/init` once per project so Claude always starts with the right context — test commands, project structure, and conventions — without spending tokens re-discovering them in every conversation.

---

## What is CLAUDE.md?

CLAUDE.md is a plain Markdown file that Claude reads at the start of every conversation. It works like a permanent briefing: you write it once, and Claude arrives already knowing your project.

Typical contents:
- The command to run tests (`python -m pytest ...`)
- Project structure overview
- Coding conventions (naming, error handling style)
- Any non-obvious constraints or context

Without it, Claude spends the first few turns of every conversation exploring files, guessing at your test runner, and inferring conventions. With it, Claude starts immediately on the actual task.

---

## What you have

- `watershed.py` — three functions for estimating watershed runoff (Rational Method)
- `test_watershed.py` — 11 pytest tests

There is no CLAUDE.md here yet — that's what you'll create.

---

## Exercise

### Part A — Without CLAUDE.md (the slow start)

**Before starting:** Copy `watershed.py` and `test_watershed.py` into a separate backup folder (e.g. `_originals/`) so you can restore them before Part B.

Open Claude Code from this directory and run:

```
add input validation to estimate_time_of_concentration so it also raises
ValueError when length_m is zero. add a test for it.
```

Watch how Claude works:
- It reads `watershed.py` to understand the code
- It may look at other tests to infer the testing style
- It may ask or guess which command to use for running tests
- It discovers conventions by exploration rather than instruction

This works — but that exploration happens again in every new conversation, every time.

---

### Part B — Create CLAUDE.md with `/init`

**Before starting:** Replace `watershed.py` and `test_watershed.py` with your backup copies from `_originals/` to restore the original files.

Run the `/init` skill:

```
/init
```

Claude will read your project and generate a `CLAUDE.md` tailored to what it finds. Review the output — it should include:
- The test command for this directory
- A summary of what the module does
- Any conventions it observed (docstring style, error-raising pattern)

You can edit the generated file to add or correct anything Claude missed.

**Then clear context with `/clear`** and repeat the same task:

```
add input validation to estimate_time_of_concentration so it also raises
ValueError when length_m is zero. add a test for it.
```

Notice that Claude now jumps directly to the implementation — no exploration phase, because the test command and code structure are already in its context from CLAUDE.md.

---

## What to notice

- `/init` does the exploration work once, so you don't repeat it every session
- Claude runs its test command from CLAUDE.md immediately, without guessing
- The generated file is a starting point — edit it to add anything domain-specific
- A well-maintained CLAUDE.md also helps teammates who are new to the codebase

## When CLAUDE.md pays off most

| Situation | Benefit |
|-----------|---------|
| Multiple sessions on the same project | Context is free after the first write |
| Team with multiple contributors | Everyone's Claude gets the same baseline |
| Complex test/build setup | No guessing at `make test` vs `pytest` vs `npm test` |
| Domain-specific conventions | One place to capture them instead of repeating in prompts |

---

## Check your starting state

Run this — all 11 tests should pass:

```powershell
python -m pytest test_watershed.py -v
```
