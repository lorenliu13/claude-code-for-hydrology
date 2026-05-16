"""Tests for watershed.py — Rational Method calculations."""
import pytest
from watershed import compute_peak_runoff, estimate_time_of_concentration, runoff_volume


# --- compute_peak_runoff ---

def test_peak_runoff_known_value():
    # C=0.5, i=50 mm/hr, A=2 km² → Q = 0.5*50*2/360 ≈ 0.1389 m³/s
    result = compute_peak_runoff(50, 2.0, 0.5)
    assert abs(result - 0.13889) < 1e-4


def test_peak_runoff_impervious_surface():
    # C=1.0 (fully impervious) should give maximum runoff
    result = compute_peak_runoff(100, 1.0, 1.0)
    assert abs(result - 100 / 360) < 1e-9


def test_peak_runoff_zero_intensity():
    assert compute_peak_runoff(0, 5.0, 0.4) == 0.0


def test_peak_runoff_invalid_coefficient():
    with pytest.raises(ValueError):
        compute_peak_runoff(50, 2.0, 1.5)


def test_peak_runoff_negative_intensity():
    with pytest.raises(ValueError):
        compute_peak_runoff(-10, 2.0, 0.5)


# --- estimate_time_of_concentration ---

def test_tc_known_value():
    # L=500m, S=0.01 → Tc = 0.0195*(500/0.1)^0.77
    tc = estimate_time_of_concentration(500, 0.01)
    # 500/sqrt(0.01) = 5000; 5000^0.77 ≈ 795.9; *0.0195 ≈ 15.52 min
    assert 10 < tc < 25


def test_tc_steeper_slope_gives_shorter_tc():
    tc_gentle = estimate_time_of_concentration(1000, 0.005)
    tc_steep = estimate_time_of_concentration(1000, 0.05)
    assert tc_steep < tc_gentle


def test_tc_invalid_slope():
    with pytest.raises(ValueError):
        estimate_time_of_concentration(500, 0.0)


# --- runoff_volume ---

def test_runoff_volume_known_value():
    # C=0.6, P=30mm, A=1km² → V = 0.6*0.03*1e6 = 18000 m³
    result = runoff_volume(30, 1.0, 0.6)
    assert abs(result - 18000) < 1


def test_runoff_volume_zero_rainfall():
    assert runoff_volume(0, 5.0, 0.5) == 0.0


def test_runoff_volume_invalid_area():
    with pytest.raises(ValueError):
        runoff_volume(20, 0, 0.5)
