---
name: flow-report
description: Run a standardized 5-step quality-check and summary report on a streamflow dataset
---

When the user invokes /flow-report or asks for a flow report, perform these five steps in order. Do not skip steps or reorder them.

## Step 1 — Data quality check
- Count total records; count missing values (sentinel -999999 or NaN)
- Count negative discharge values (physically impossible in streamflow)
- Report the date range covered and flag any gaps longer than 7 consecutive days

## Step 2 — Basic statistics (clean data only)
Exclude missing sentinels and negative values from all calculations:
- Mean, median, and standard deviation of discharge
- Minimum and maximum discharge with their dates
- Count of zero-flow days (intermittent streams may have these; perennial streams should not)

## Step 3 — Annual maxima summary
- Extract one peak discharge per water year (water year N = Oct 1 of N-1 through Sep 30 of N)
- List the three highest annual peaks with their dates and water years
- Note how many complete water years are in the record

## Step 4 — Outlier flag
- Compute the median of annual maxima (Q̃_annual)
- Flag any single daily or instantaneous value exceeding 5 × Q̃_annual as a potential outlier worth human review
- Do not remove flagged values automatically — report them for the user to investigate

## Step 5 — Summary verdict
Assign a quality grade and print it prominently:
- **GOOD**: missing < 5% AND no negative values
- **FAIR**: missing 5–15% (no negatives)
- **POOR**: missing > 15% OR any negative values present

Also warn if the record contains fewer than 10 complete water years, since flood frequency estimates will be unreliable.

---

Format the report with a header for each step. Present statistics in a compact markdown table where possible. End with the quality grade on its own line: `Data quality: GOOD / FAIR / POOR`.
