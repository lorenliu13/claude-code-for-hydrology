# Claude Code Best Practices — Hands-On Tutorials

A collection of self-contained exercises for learning [Claude Code](https://claude.ai/code) best practices, using hydrology-themed Python code as the subject matter.

Each exercise demonstrates a **"before vs. after" prompt pattern** — you try a vague prompt, clear context, then try a specific prompt, and compare what Claude produces.

---

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed (`npm install -g @anthropic-ai/claude-code`)
- Python 3.10+ with `pip`
- Basic familiarity with the terminal

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/your-username/claude-code-tutorials.git
cd claude-code-tutorials

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Open Claude Code
claude
```

Then pick an exercise below and follow its `README.md`.

---

## Exercises

| # | Folder | Best Practice | Skill Level |
|---|--------|--------------|-------------|
| 1 | [`01_verify_your_work/`](01_verify_your_work/) | Give Claude tests so it can verify its own output | Beginner |
| 2 | [`02_explore_plan_code/`](02_explore_plan_code/) | Explore → Plan → Code with plan mode | Beginner |
| 3 | [`03_specific_context/`](03_specific_context/) | Reference specific files and symptoms in prompts | Beginner |

---

## How Each Exercise Works

1. Read the `README.md` inside the exercise folder — it explains the concept and both prompts.
2. Try the **"before" prompt** — observe what Claude produces without guidance.
3. Clear context with `/clear` in Claude Code.
4. Try the **"after" prompt** — compare the quality of the result.

The difference between the two prompts is the lesson.

---

## Running Tests

Each exercise folder contains a `test_*.py` file. To run tests for an exercise:

```bash
python -m pytest 01_verify_your_work/ -v
python -m pytest 02_explore_plan_code/ -v
python -m pytest 03_specific_context/ -v
```

Or run all exercises at once:

```bash
python -m pytest -v
```

> **Note:** Use `python3` instead of `python` on systems where Python 2 is the default.

---

## Project Structure

```
claude-code-tutorials/
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
├── CLAUDE.md                        # Claude Code project instructions
│
├── .claude/
│   ├── settings.json                # Claude Code project permissions
│   ├── skills/run-tests/SKILL.md    # Custom /run-tests slash command
│   └── agents/code-reviewer.md     # Example subagent definition
│
├── 01_verify_your_work/
│   ├── README.md                    # Exercise instructions
│   ├── performance_metrics.py       # Stub functions to implement
│   └── test_performance_metrics.py  # Tests that define correctness
│
├── 02_explore_plan_code/
│   ├── README.md
│   ├── flow_analysis.py             # Working code to extend
│   ├── sample_flow.csv              # Fictional gauge station data
│   └── test_flow_analysis.py
│
└── 03_specific_context/
    ├── README.md
    ├── drought_index.py             # Code with an intentional bug
    └── test_drought_index.py
```

### `.claude/` folder

The `.claude/` folder is part of the learning material — examine it alongside the exercises:

- **`skills/run-tests/SKILL.md`** — a custom `/run-tests` slash command. Type `/run-tests` in Claude Code to run pytest and get a formatted summary. Shows how to build your own skills.
- **`agents/code-reviewer.md`** — an example subagent that reviews Python code. Shows how to define agents with restricted tools and focused instructions.

---

## Exercise Details

### Exercise 1 — Verify Your Work
**Concept:** The single highest-leverage thing you can do is give Claude tests with known expected values. Claude becomes its own quality checker — you don't need to verify manually.

Metrics covered: Nash-Sutcliffe Efficiency (NSE) and Kling-Gupta Efficiency (KGE).

### Exercise 2 — Explore → Plan → Code
**Concept:** Use plan mode (`Shift+Tab` twice) to separate exploration from implementation. Claude reads and understands existing code before making any changes, preventing it from solving the wrong problem.

Feature to add: `compute_exceedance_flows()` returning Q90 and Q95 flow thresholds.

### Exercise 3 — Specific Context
**Concept:** Vague prompts make Claude guess. Naming the file, function, failing test, and symptom lets Claude go directly to the root cause.

Bug to fix: swapped mean/std in the Standardized Precipitation Index (SPI) formula.

---

## Contributing

Contributions are welcome. If you have an idea for a new best-practice exercise:

1. Fork the repo and create a branch.
2. Add a new numbered folder following the existing pattern (a subject Python file, a test file, and a README with before/after prompts).
3. Open a pull request with a short description of the best practice being demonstrated.

---

## License

MIT — see [LICENSE](LICENSE).
