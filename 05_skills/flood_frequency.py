"""Flood frequency analysis utilities (US conventions, Weibull / log-linear interpolation)."""
from datetime import date


def extract_annual_maxima(
    flows: list[float], dates: list[date]
) -> dict[int, float]:
    """
    Return the peak discharge for each water year.
    Water year N runs Oct 1 of year N-1 through Sep 30 of year N.
    Values equal to -999999 (USGS missing sentinel) are excluded.
    """
    raise NotImplementedError


def weibull_return_periods(annual_maxima: list[float]) -> list[tuple[float, float]]:
    """
    Compute Weibull plotting positions for a list of annual maxima.
    Returns a list of (return_period_years, discharge) sorted ascending by discharge.
    Formula: T = (n + 1) / rank, where rank 1 = smallest value.
    """
    raise NotImplementedError


def estimate_quantile(annual_maxima: list[float], return_period: float) -> float:
    """
    Estimate discharge for a given return period using log-linear interpolation
    on Weibull plotting positions.
    Raises ValueError if return_period is outside the range the data can support.
    """
    raise NotImplementedError


def data_quality_summary(flows: list[float]) -> dict:
    """
    Summarise the quality of a raw discharge record.
    Returns a dict with keys:
        total        - total number of values
        missing      - count of -999999 sentinels
        negative     - count of physically-impossible negative values
        clean_count  - values that are neither missing nor negative
        quality_grade - 'GOOD', 'FAIR', or 'POOR' (see README for thresholds)
    """
    raise NotImplementedError
