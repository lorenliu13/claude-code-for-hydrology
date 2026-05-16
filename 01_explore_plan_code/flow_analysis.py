"""
Streamflow analysis tools for daily discharge time series.

Loads gauge station data and computes summary statistics and peak flow events.
"""
import pandas as pd
import numpy as np
from pathlib import Path


def load_flow_data(path: str | Path) -> pd.DataFrame:
    """
    Load daily discharge data from a CSV file.

    Expected columns: date (YYYY-MM-DD), discharge_m3s (float)

    Returns a DataFrame with a DatetimeIndex and a 'discharge_m3s' column.
    """
    df = pd.read_csv(path, parse_dates=["date"], index_col="date")
    df = df.sort_index()
    return df


def compute_basic_stats(df: pd.DataFrame) -> dict:
    """
    Compute basic summary statistics for discharge.

    Returns a dict with: mean, std, min, max (all in m³/s).
    """
    q = df["discharge_m3s"]
    return {
        "mean": float(q.mean()),
        "std": float(q.std()),
        "min": float(q.min()),
        "max": float(q.max()),
    }


def find_peak_flows(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """
    Return the n highest discharge events, sorted descending.

    Returns a DataFrame subset with the same columns as the input.
    """
    return df.nlargest(n, "discharge_m3s")
