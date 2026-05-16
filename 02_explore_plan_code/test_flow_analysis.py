"""Tests for flow_analysis.py — these cover the existing functions."""
import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from flow_analysis import load_flow_data, compute_basic_stats, find_peak_flows

DATA_PATH = Path(__file__).parent / "sample_flow.csv"


@pytest.fixture
def flow_df():
    return load_flow_data(DATA_PATH)


def test_load_returns_dataframe(flow_df):
    assert isinstance(flow_df, pd.DataFrame)
    assert "discharge_m3s" in flow_df.columns


def test_load_has_datetime_index(flow_df):
    assert isinstance(flow_df.index, pd.DatetimeIndex)


def test_basic_stats_keys(flow_df):
    stats = compute_basic_stats(flow_df)
    assert set(stats.keys()) == {"mean", "std", "min", "max"}


def test_basic_stats_ordering(flow_df):
    stats = compute_basic_stats(flow_df)
    assert stats["min"] <= stats["mean"] <= stats["max"]
    assert stats["std"] >= 0


def test_peak_flows_count(flow_df):
    peaks = find_peak_flows(flow_df, n=5)
    assert len(peaks) == 5


def test_peak_flows_are_largest(flow_df):
    peaks = find_peak_flows(flow_df, n=3)
    fifth_largest = flow_df["discharge_m3s"].nlargest(4).iloc[-1]
    assert peaks["discharge_m3s"].min() >= fifth_largest
