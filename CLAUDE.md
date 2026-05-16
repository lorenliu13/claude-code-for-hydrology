# Claude Code Best Practices — Learning Project

Structured exercises for learning Claude Code best practices, using hydrology-themed Python code.
Each numbered folder is a self-contained exercise. Read the folder's `README.md` before starting.

## Python Environment

```bash
python -m pytest <exercise_folder>/ -v
```

Use `python3` on systems where `python` defaults to Python 2.

## Exercise Index

| Folder | Best Practice |
|--------|--------------|
| `01_verify_your_work/` | Give Claude tests so it can verify its own output |
| `02_explore_plan_code/` | Explore → Plan → Code with plan mode |
| `03_specific_context/` | Reference specific files and symptoms in prompts |
| `04_init_claude_md/` | Use `/init` to create CLAUDE.md for persistent project context |
| `05_aws_cli_workflow/` | Use AWS CLI with Claude to download public hydrological datasets |
| `06_mcp_usgs_gauge/` | Use MCP fetch server to query the USGS NWIS API and implement correct parsing code |
| `07_skills/` | Create and use skills for domain knowledge (`/hydro-context`) and repeatable workflows (`/flow-report`) |
| `08_subagent_review/` | Orchestrate coder and reviewer subagents in sequence; parent controls context isolation and loops until review passes |

## Workflow for Each Exercise

1. Read the `README.md` in the exercise folder
2. Try the "before" prompt — observe what Claude produces
3. Clear context with `/clear`
4. Try the "after" prompt — compare the results

## Notes

- All exercises use hydrology/water science Python code (streamflow, drought indices, model metrics)
- The `.claude/` folder contains a pre-built skill (`/run-tests`) and a subagent (`code-reviewer`) to examine as examples
