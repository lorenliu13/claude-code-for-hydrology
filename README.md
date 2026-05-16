# Claude Code for Hydrology — Hands-On Tutorials

A collection of self-contained exercises for learning [Claude Code](https://claude.ai/code) best practices, built specifically for the **hydrological research community**. All code examples use real hydrology concepts — streamflow analysis, drought indices, model performance metrics, and USGS gauge data.

Each exercise demonstrates a **"before vs. after" prompt pattern** — you try a vague prompt, clear context, then try a specific prompt, and compare what Claude produces.

---

## Who This Is For

Hydrologists, water scientists, and researchers who want to use AI-assisted coding more effectively. No prior Claude Code experience needed — just Python familiarity and curiosity about LLM-based workflows.

---

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed (`npm install -g @anthropic-ai/claude-code`)
- Python 3.10+ with `pip`
- Basic familiarity with the terminal

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/lorenliu13/claude-code-for-hydrology.git
cd claude-code-for-hydrology

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Open Claude Code
claude
```

Then pick an exercise below and follow its `README.md`.

---

## Exercises

The exercises are ordered from highest-leverage fundamentals to more advanced workflows. Start at the beginning — each exercise builds on the habits established by the previous ones.

**Foundations (Exercises 1–4)** cover the core prompting practices that improve every interaction with Claude Code. These are the skills you will use in every session.

**Workflows (Exercises 5–9)** introduce tools and patterns that automate, extend, and scale what you can do — once the foundations are solid.

| # | Folder | Best Practice | Level |
|---|--------|--------------|-------|
| 1 | [`01_explore_plan_code/`](01_explore_plan_code/) | Explore → Plan → Code with plan mode | Beginner |
| 2 | [`02_specific_context/`](02_specific_context/) | Reference specific files and symptoms in prompts | Beginner |
| 3 | [`03_verify_your_work/`](03_verify_your_work/) | Give Claude tests so it can verify its own output | Beginner |
| 4 | [`04_init_claude_md/`](04_init_claude_md/) | Use `/init` to create CLAUDE.md for persistent project context | Beginner |
| 5 | [`05_skills/`](05_skills/) | Create custom skills for domain knowledge and repeatable workflows | Intermediate |
| 6 | [`06_subagent_review/`](06_subagent_review/) | Orchestrate coder and reviewer subagents in sequence | Advanced |
| 7 | [`07_aws_cli_workflow/`](07_aws_cli_workflow/) | Use AWS CLI with Claude to download public hydrological datasets | Intermediate |
| 8 | [`08_mcp_usgs_gauge/`](08_mcp_usgs_gauge/) | Use MCP fetch server to query the USGS NWIS API | Intermediate |
| 9 | [`09_parallel_fanout/`](09_parallel_fanout/) | Spawn subagents in parallel for multi-configuration analysis; aggregate with a reporter subagent | Advanced |

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
python -m pytest 01_explore_plan_code/ -v
```

Or run all exercises at once:

```bash
python -m pytest -v
```

> **Note:** Use `python3` instead of `python` on systems where Python 2 is the default.

---

## Exercise Details

### Exercise 1 — Explore → Plan → Code
**Concept:** Use plan mode (`Shift+Tab` twice) to separate exploration from implementation. Claude reads existing code before making changes, preventing it from overwriting things it hasn't seen.

Feature to add: `compute_exceedance_flows()` returning Q90 and Q95 flow thresholds.

### Exercise 2 — Specific Context
**Concept:** Vague prompts make Claude guess. Naming the file, function, failing test, and symptom lets Claude go directly to the root cause instead of exploring blind.

Bug to fix: swapped mean/std in the Standardized Precipitation Index (SPI) formula.

### Exercise 3 — Verify Your Work
**Concept:** The single highest-leverage habit is giving Claude tests with known expected values. Claude becomes its own quality checker and can iterate without your involvement.

Metrics covered: Nash-Sutcliffe Efficiency (NSE) and Kling-Gupta Efficiency (KGE).

### Exercise 4 — Initialize CLAUDE.md
**Concept:** Use `/init` to generate a `CLAUDE.md` that gives Claude persistent project context across sessions — so you stop re-explaining your codebase every time you open a new conversation.

### Exercise 5 — Skills
**Concept:** Create reusable skills for domain knowledge (`/hydro-context`) and repeatable workflows (`/flow-report`) so you don't re-explain hydrology conventions every session. Skills compose with everything else in this repo.

### Exercise 6 — Subagent Review
**Concept:** Orchestrate a coder subagent and a reviewer subagent in sequence. The parent agent controls context isolation and loops until the review passes — offloading an entire quality gate to Claude.

### Exercise 7 — AWS CLI Workflow
**Concept:** Combine Claude with the AWS CLI to discover and download public hydrological datasets (USGS, NOAA, etc.) without leaving the terminal. Claude handles flag lookup and command construction; you supply the science intent.

### Exercise 8 — MCP USGS Gauge
**Concept:** Use the MCP fetch server to query the USGS NWIS API in real time, then implement correct response parsing in Python. Demonstrates how MCP tools extend Claude's reach to live external data.

### Exercise 9 — Parallel Fan-Out with Subagents
**Concept:** When the same analysis must run across multiple independent configurations, spawn one subagent per configuration simultaneously — then collect all results with a single reporter subagent. Wall time equals the slowest single subagent, not the sum of all. Applied here to computing SPI drought indices (SPI-1, SPI-3, SPI-6, SPI-12) in parallel and aggregating findings into a unified comparison report.

---

## Contributing

Contributions are welcome. If you have an idea for a new best-practice exercise:

1. Fork the repo and create a branch.
2. Add a new numbered folder following the existing pattern (a subject Python file, a test file, and a README with before/after prompts).
3. Open a pull request with a short description of the best practice being demonstrated.

---

## License

MIT — see [LICENSE](LICENSE).
