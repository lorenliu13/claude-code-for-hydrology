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

## Workflow for Each Exercise

1. Read the `README.md` in the exercise folder
2. Try the "before" prompt — observe what Claude produces
3. Clear context with `/clear`
4. Try the "after" prompt — compare the results

## Notes

- All exercises use hydrology/water science Python code (streamflow, drought indices, model metrics)
- The `.claude/` folder contains a pre-built skill (`/run-tests`) and a subagent (`code-reviewer`) to examine as examples
