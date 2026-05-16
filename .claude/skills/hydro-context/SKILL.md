---
name: hydro-context
description: Apply US hydrology domain knowledge — units, formulas, and conventions — when reading or writing hydrological code
---

You are assisting with US hydrology / water resources engineering code. Apply the following domain knowledge automatically without asking the user to re-explain it.

## Units
- Discharge (streamflow): cubic feet per second (cfs) in US datasets; m³/s (cms) internationally
- Stage (water level): feet in USGS data; metres in international datasets
- Always check that input/output units are consistent; flag mismatches as a comment or warning

## Key formulas

**Rating curve (stage-discharge):** `Q = a × (H – H₀)^b`
- H = stage, H₀ = zero-flow stage offset, a and b are fitted constants
- Typical b range: 1.5–3.0 for natural channels; fit in log-log space

**Manning's equation (open-channel flow):** `Q = (1/n) × A × R^(2/3) × S^(1/2)`
- n = Manning's roughness (0.025–0.05 for natural channels)
- R = hydraulic radius, S = channel slope (dimensionless, m/m or ft/ft)

**Log-Pearson Type III** is the standard US flood frequency distribution (USGS Bulletin 17C).
- Work in log₁₀ space: fit the mean, standard deviation, and skewness of log₁₀(Q)

**Weibull plotting position:** `P(X ≤ x) = m / (n + 1)`, return period `T = (n + 1) / m`
- m = rank (1 = smallest), n = total number of data points

## Flood frequency terminology
- **Return period** (recurrence interval): average years between events of that magnitude or greater
- **Q2**: 2-year flood (50% annual exceedance probability) ≈ bankfull flow in many streams
- **Q10**: 10-year flood (10% AEP)
- **Q100**: 100-year flood (1% AEP) — US regulatory floodplain standard
- **AEP**: Annual Exceedance Probability = 1 / T

## Data quality conventions
- USGS missing-data sentinel: -999999 — always filter these before any calculation
- Negative discharge values are physically impossible — treat as errors
- **Water year**: Oct 1 – Sep 30 (US convention); water year N starts Oct 1 of year N-1
- Minimum record length for reliable flood frequency: ≥ 10 years (30+ preferred for Q100)
