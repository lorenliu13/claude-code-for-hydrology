# Exercise 5: Create and Use Skills

**Best practice:** Package domain knowledge and repeatable workflows as skills so Claude applies them consistently — without you re-explaining them every session.

---

## What are skills?

Skills are small Markdown files stored in `.claude/skills/<name>/SKILL.md`. When you type `/skill-name` in a Claude Code conversation, Claude reads the skill file and follows its instructions. Skills let you encode two very different things:

| Skill type | What it captures | Example |
|---|---|---|
| **Domain knowledge** | Formulas, conventions, terminology Claude should assume | `/hydro-context` |
| **Repeatable workflow** | A fixed sequence of steps Claude always follows | `/flow-report` |

This exercise has pre-built examples of both. Read each skill file to understand what it does, then compare Claude's output with and without it.

---

## What you have

**Code to implement:**
- `flood_frequency.py` — four stub functions for flood frequency analysis
- `test_flood_frequency.py` — 16 tests covering all four functions

**Skills already installed (project-level):**
- `.claude/skills/hydro-context/SKILL.md` — domain knowledge: US hydrology formulas, units, and conventions
- `.claude/skills/flow-report/SKILL.md` — repeatable workflow: a 5-step data quality and summary report

---

## Background: flood frequency analysis

Flood frequency analysis estimates how often extreme flows occur. The standard US method:

1. Collect a multi-year record of **annual maxima** — one peak discharge per **water year** (Oct 1 – Sep 30)
2. Rank the peaks and compute **Weibull plotting positions**: `T = (n + 1) / rank`
3. Fit a distribution (often Log-Pearson III) and read off **Q2, Q10, Q100**

Key domain detail: the USGS missing-data sentinel is **-999999** and must be stripped before any calculation. Water years start in **October**, not January.

---

## Exercise

### Part A — Domain knowledge skill (`/hydro-context`)

Run this prompt:

```
/hydro-context
implement the four functions in 05_skills/flood_frequency.py.
run python -m pytest 05_skills/test_flood_frequency.py -v and fix any failures.
```

The `/hydro-context` skill gives Claude the water-year definition, Weibull formula, and -999999 sentinel convention **without you having to spell them out**. Claude should implement correctly on the first or second attempt.

**What to notice:**
- Claude uses Oct 1 as the water-year boundary immediately
- It strips -999999 sentinels in `extract_annual_maxima` and `data_quality_summary`
- The Weibull formula matches what the tests expect

---

### Part B — Repeatable workflow skill (`/flow-report`)

With `flood_frequency.py` fully implemented (from Part B), ask Claude to analyse a dataset:

```
/flow-report
Here is a 5-year daily discharge record (cfs) with some data quality issues.
Analyse it using the flow-report workflow:

flows = [1200, 980, 1450, -999999, 1100, 830, -999999, -999999,
         2300, 1870, 950, 740, 1600, 1250, -999999,
         880, 1020, 1380, 1750, 2100]
dates are 2019-06-01 through 2019-06-20 (daily)
```

**What to notice:**
- Claude follows the exact 5-step sequence in `/flow-report` — in order, every time
- The output format matches what the skill specifies (tables, headers, quality grade line)
- You did not have to prompt Claude to check for missing data, compute stats, or assign a grade — the skill handles all of that
- Run `/flow-report` again on a different dataset: the structure will be identical

---

## How skills are structured

Open `.claude/skills/hydro-context/SKILL.md`:

```
---
name: hydro-context
description: Apply US hydrology domain knowledge...
---

[skill body: what Claude should know and apply]
```

The frontmatter `name` and `description` fields are what appears in the `/` command list. The body is the instruction Claude follows when you invoke it.

Skills live at:
- **Project level:** `.claude/skills/<name>/SKILL.md` — shared with everyone on the project
- **User level:** `~/.claude/skills/<name>/SKILL.md` — personal skills across all projects

---

## What to notice across both parts

| | `/hydro-context` | `/flow-report` |
|---|---|---|
| Water year boundary | Correct (Oct 1) immediately | Reported in Step 1 |
| Missing data handling | Strips -999999 automatically | Counted and reported in Step 1 |
| Weibull formula | Matches tests on first attempt | N/A |
| Report structure | N/A | Identical every time you invoke it |
| Prompting effort | One slash command replaces domain explanation | One slash command replaces workflow instructions |

**Key insight:** Skills encode what you'd otherwise retype every session. Domain knowledge skills reduce errors on first attempt; workflow skills make Claude's output reproducible and auditable.

---

## Check your starting state

All 16 tests should FAIL (stubs not implemented — that is correct):

```powershell
python -m pytest 05_skills/test_flood_frequency.py -v
```
