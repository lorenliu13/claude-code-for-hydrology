# Exercise 9: Parallel Fan-Out with Subagents

**Best practice:** When you need the same analysis run across multiple configurations, spawn one subagent per configuration in parallel — then collect all results with a single reporter subagent.

---

## What is the parallel fan-out pattern?

In the sequential write→review→revise pattern (Exercise 6), subagents run one after another. The parallel fan-out pattern is different: the parent spawns several subagents **at the same time**, waits for all of them to finish, then passes every result to a final aggregator.

```
Parent (Orchestrator)
  ├─► Subagent: SPI-1  ──┐
  ├─► Subagent: SPI-3  ──┤  (all run in parallel)
  ├─► Subagent: SPI-6  ──┤
  └─► Subagent: SPI-12 ──┘
                          │
                  Reporter subagent
                  (collects all 4 results → writes drought_report.md)
```

This is the right pattern when:
- Each configuration is **independent** (no result feeds into another)
- You want results **faster** (wall time ≈ slowest subagent, not sum of all)
- You need a **unified report** across all configurations at the end

---

## Background: Standardized Precipitation Index (SPI)

The SPI is the most widely used drought index in hydrology. It transforms a precipitation record into z-scores so that wet and dry periods can be compared across locations and seasons.

**How it works:**
1. Aggregate monthly precipitation over a rolling window of `k` months (the *timescale*)
2. Fit a Gamma distribution to the aggregated totals
3. Transform each aggregated value to its normal-distribution equivalent (z-score)

**Timescale convention:**

| Timescale | What it captures |
|-----------|-----------------|
| SPI-1  | Short-term soil moisture and flash drought |
| SPI-3  | Seasonal agricultural drought |
| SPI-6  | Medium-term streamflow impact |
| SPI-12 | Long-term groundwater and reservoir drought |

**Interpretation:** SPI < −1.0 is moderate drought; SPI < −1.5 is severe; SPI < −2.0 is extreme.

---

## What you have

- `spi_analysis.py` — stub function `compute_spi(precipitation, timescale) -> list[float]`
- `test_spi_analysis.py` — 12 tests covering correctness, edge cases, and multi-timescale behaviour

---

## Before: ask Claude directly (sequential)

Paste this into Claude Code:

```
implement compute_spi in 09_parallel_fanout/spi_analysis.py.
Then compute SPI-1, SPI-3, SPI-6, and SPI-12 on this 5-year monthly
precipitation record (mm) and summarise the drought periods found:

precip = [62,45,80,120,95,110,30,15,8,42,70,88,
          55,40,75,130,100,95,20,10,5,38,65,82,
          70,50,90,140,110,105,25,12,6,40,68,90,
          48,35,68,115,88,92,18,8,4,35,60,78,
          58,42,72,125,98,100,22,11,5,37,63,85]

write results to 09_parallel_fanout/drought_report.md
```

Claude will implement the function and run all four timescales sequentially in one context. Note how long it takes and whether the report clearly separates SPI-1 vs SPI-12 findings.

---

## After: parallel fan-out with subagents

Clear context (`/clear`), then paste this prompt:

```
implement compute_spi in 09_parallel_fanout/spi_analysis.py first.

Then spawn four subagents in parallel — one per SPI timescale:

Shared precipitation record (60 months of monthly totals in mm):
precip = [62,45,80,120,95,110,30,15,8,42,70,88,
          55,40,75,130,100,95,20,10,5,38,65,82,
          70,50,90,140,110,105,25,12,6,40,68,90,
          48,35,68,115,88,92,18,8,4,35,60,78,
          58,42,72,125,98,100,22,11,5,37,63,85]

Each subagent receives: the precipitation record, its assigned timescale,
and this task — nothing else:
  - Compute SPI for its timescale using compute_spi from spi_analysis.py
  - Identify all drought events (consecutive months with SPI < -1.0)
  - Report: timescale, drought event count, longest drought duration (months),
    minimum SPI value and the month index where it occurs

Wait for all four subagents to finish, then have a reporter subagent collect
all four result sets and write a comparison table to
09_parallel_fanout/drought_report.md with:
  - A header row: Timescale | Drought Events | Longest Duration | Min SPI | Month of Min SPI
  - One row per timescale (SPI-1 through SPI-12)
  - A two-sentence interpretation below the table explaining what the
    difference between short- and long-timescale results means for water management
```

Then validate the implementation:

```bash
python -m pytest 09_parallel_fanout/test_spi_analysis.py -v
```

---

## What to notice

**Speed:** The four SPI calculations run concurrently. Wall time is roughly the duration of the slowest single subagent, not the sum of all four.

**Context isolation:** Each subagent sees only its own timescale result. The reporter sees only the four result summaries — not the intermediate SPI arrays. This keeps the reporter focused on comparison, not recomputation.

**Report quality:** Compare the sequential "before" report with the parallel "after" report. The parallel version separates short-timescale (SPI-1, SPI-3) flash drought signals from long-timescale (SPI-6, SPI-12) groundwater drought — a distinction that matters for water managers choosing between emergency response vs. reservoir drawdown policy.

**Scaling:** Change the four timescales to eight (add SPI-2, SPI-9, SPI-18, SPI-24) — the prompt structure is identical and wall time barely increases because subagents still run in parallel.

---

## Optional extension: add a convergence loop

If you want to search for the timescale that best predicts observed streamflow, append to the "after" prompt:

```
After the report is written, spawn a search subagent that tests additional
timescales (2, 4, 9, 18, 24 months) one at a time, computing the correlation
between SPI and the streamflow proxy below. Stop when correlation exceeds 0.85
or all timescales are tested. Report the best timescale found.

streamflow_proxy = [0.8,0.6,1.1,1.9,1.5,1.7,0.3,0.1,0.05,0.5,0.9,1.2,
                    0.7,0.5,1.0,2.0,1.6,1.5,0.2,0.1,0.04,0.4,0.8,1.1,
                    0.9,0.6,1.2,2.2,1.7,1.6,0.3,0.1,0.05,0.5,0.9,1.3,
                    0.6,0.4,0.9,1.8,1.4,1.4,0.2,0.1,0.03,0.4,0.7,1.0,
                    0.7,0.5,1.0,1.9,1.5,1.5,0.25,0.1,0.04,0.45,0.8,1.1]
```

This combines the fan-out pattern (parallel configurations) with a search loop (sequential convergence) — the two most common multi-agent structures in scientific computing.
