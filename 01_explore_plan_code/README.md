# Exercise 2: Explore First, Then Plan, Then Code

**Best practice:** Use plan mode to separate exploration from implementation. This prevents Claude from solving the wrong problem or making changes without understanding the existing code.

---

## What you have

- `flow_analysis.py` — a working Python script that loads daily discharge data and computes basic statistics
- `sample_flow.csv` — 2 years of daily streamflow data (m³/s) for a fictional gauge station
- `test_flow_analysis.py` — tests for the existing functions

The script already has:
- `load_flow_data(path)` — loads the CSV into a pandas DataFrame
- `compute_basic_stats(df)` — returns mean, std, min, max discharge
- `find_peak_flows(df, n=5)` — returns the n highest discharge events

**Your task:** Add low-flow analysis — specifically, compute exceedance probability flows (Q90 and Q95), which represent the discharge exceeded 90% and 95% of the time. These are critical for water availability and environmental flow assessments.

---

## Exercise

### Step 1 — Enter plan mode

In Claude Code, press `Shift+Tab` twice (or use the menu) to enter plan mode. In plan mode, Claude reads and explores without making any changes.

### Step 2 — Explore

In plan mode, prompt:

```
read flow_analysis.py and understand how it's structured.
look at sample_flow.csv to understand the data format.
also read the existing tests in test_flow_analysis.py.
```

### Step 3 — Plan

Still in plan mode, prompt:

```
I want to add a function compute_exceedance_flows(df) that returns Q90 and Q95
(the discharge values exceeded 90% and 95% of the time respectively).
Q90 means only 10% of days have flows below this value.
What exactly needs to change? Create a step-by-step plan.
```

Review Claude's plan. Press `Ctrl+G` to open it in your text editor and add any notes.

### Step 4 — Implement

Exit plan mode (press `Shift+Tab` once), then:

```
implement compute_exceedance_flows from the plan.
add 2 pytest tests for it.
run the tests after implementing and fix any failures.
```

### Step 5 — Commit

```
commit the changes with a descriptive message
```

---

## What to notice

- In plan mode, Claude cannot modify files — exploration is safe
- Planning catches misunderstandings before they become code changes
- Claude's plan will reference the actual structure it found (column names, data types)
- The plan step is most valuable when: the codebase is unfamiliar, changes span multiple places, or you're not sure of the right approach

## When to skip planning

For a simple one-line fix or when the change is obvious, go straight to implementation. Planning adds overhead — use it when the scope or approach is uncertain.
