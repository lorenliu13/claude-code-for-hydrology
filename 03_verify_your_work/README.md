# Exercise 3: Give Claude a Way to Verify Its Work

**Best practice:** Include tests with known expected values so Claude can check itself and iterate until correct. This is the single highest-leverage thing you can do.

---

## What you have

- `performance_metrics.py` — stub functions for two common hydrological model performance metrics
- `test_performance_metrics.py` — 8 tests with known expected values

The two metrics are:

**Nash-Sutcliffe Efficiency (NSE)**
```
NSE = 1 - sum((obs - sim)^2) / sum((obs - mean(obs))^2)
```
- NSE = 1.0 → perfect model
- NSE = 0.0 → model no better than predicting the mean
- NSE < 0 → model worse than the mean

**Kling-Gupta Efficiency (KGE)**
```
KGE = 1 - sqrt((r - 1)^2 + (alpha - 1)^2 + (beta - 1)^2)
```
where r = Pearson correlation, alpha = std(sim)/std(obs), beta = mean(sim)/mean(obs)
- KGE = 1.0 → perfect model

---

## Exercise

### Part A — Without verification (the risky way)

**Before starting:** Copy `performance_metrics.py` into a separate backup folder (e.g. `_originals/`) so you can restore it before Part B.

Open Claude Code and run this prompt:

```
implement the compute_nse and compute_kge functions in 03_verify_your_work/performance_metrics.py
```

Claude will write something. But will it handle all edge cases? You'd have to check manually.

### Part B — With verification (the reliable way)

**Before starting:** Replace `performance_metrics.py` with your backup copy from `_originals/` to restore the original stubs.

Clear context with `/clear`, then try:

```
implement compute_nse and compute_kge in 03_verify_your_work/performance_metrics.py.
after implementing, run:
  python -m pytest 03_verify_your_work/test_performance_metrics.py -v
all 8 tests must pass. fix any failures before stopping.
```

Claude will now run tests after implementing, see any failures, and fix them before it considers the task done.

---

## What to notice

- In Part B, Claude becomes its own quality checker — you don't need to verify manually
- The test file IS the specification: it defines exactly what "correct" means
- Claude can iterate on its own implementation, catching subtle formula errors
- If you can't write tests, at minimum paste expected outputs: "for obs=[10,20,30] and sim=[10,20,30], NSE should be 1.0"

---

## Check your starting state

Run this to confirm the stubs are not yet implemented (all 8 should FAIL — that's correct):

```powershell
python -m pytest 03_verify_your_work/test_performance_metrics.py -v
```
