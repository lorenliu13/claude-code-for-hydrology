# Exercise 3: Provide Specific Context in Your Prompts

**Best practice:** Reference specific files, name the symptom, and point to the failing test. Vague prompts make Claude guess — specific prompts let Claude find the root cause.

---

## What you have

- `drought_index.py` — computes the Standardized Precipitation Index (SPI)
- `test_drought_index.py` — one failing test that reveals a bug

**SPI background:** SPI is the z-score of precipitation relative to a historical baseline:
```
SPI = (P - mean(P)) / std(P)
```
- SPI ≈ 0 → normal conditions
- SPI < -1 → moderately dry; SPI < -2 → severely dry
- SPI > 1 → moderately wet

The code has a bug: the mean and standard deviation are swapped in the formula.

---

## Exercise

### Part A — Vague prompt (the frustrating way)

**Before starting:** Copy `drought_index.py` into a separate backup folder (e.g. `_originals/`) so you can restore it before Part B.

Open Claude Code and run:

```
fix the SPI calculation bug in drought_index.py
```

Observe: Claude has to guess what the bug is. It might explore the file, make changes, or ask clarifying questions. It may fix it, or it may fix the wrong thing.

### Part B — Specific prompt (the effective way)

**Before starting:** Replace `drought_index.py` with your backup copy from `_originals/` to restore the original buggy file.

Clear context with `/clear`, then try:

```
users report that SPI values don't look right — even months with normal rainfall show large anomalies.
the bug is in drought_index.py in the compute_spi function.
test_drought_index.py::test_spi_of_mean_is_zero is failing — run it to see the error.
fix the root cause of the wrong formula, not a workaround.
run the test after fixing to confirm it passes.
```

Observe: Claude goes directly to the right function, runs the test to understand the failure, and fixes the formula.

---

## What to notice

- The specific prompt names: the **file**, the **function**, the **failing test**, and the **symptom**
- Claude doesn't need to guess or explore broadly — it goes straight to the problem
- The test gives Claude a concrete pass/fail signal, not just your description
- "Fix the root cause" prevents Claude from patching over the symptom

## Prompt anatomy for bug reports

| Element | Example |
|---------|---------|
| Symptom | "SPI values don't look right for normal months" |
| Location | "the bug is in `drought_index.py`, `compute_spi()`" |
| Evidence | "test `test_spi_of_mean_is_zero` is failing" |
| Constraint | "fix the root cause, not a workaround" |
| Verification | "run the test after fixing to confirm it passes" |

---

## Check your starting state

Run this — one test should FAIL (the bug is present, which is intentional):

```powershell
python -m pytest test_drought_index.py -v
```
