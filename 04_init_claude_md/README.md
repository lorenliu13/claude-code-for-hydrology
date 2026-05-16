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

## How to use `/init`

Navigate to the root of your project and run:

```
/init
```

Claude will scan your codebase and generate a `CLAUDE.md` tailored to what it finds — test commands, module summaries, and any conventions it observes. You can edit the generated file to add or correct anything domain-specific.

The CLAUDE.md at the root of *this* repository was created this way. Open it to see what `/init` produces for a real project.

---

## When CLAUDE.md pays off most

| Situation | Benefit |
|-----------|---------|
| Multiple sessions on the same project | Context is free after the first write |
| Team with multiple contributors | Everyone's Claude gets the same baseline |
| Complex test/build setup | No guessing at `make test` vs `pytest` vs `npm test` |
| Domain-specific conventions | One place to capture them instead of repeating in prompts |
