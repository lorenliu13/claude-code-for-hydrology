"""
Tests for compute_spi in spi_analysis.py.
Run after the parallel fan-out exercise has written the implementation.
"""
import math
import statistics
import pytest
from spi_analysis import compute_spi

# 5-year (60-month) synthetic record: wet summers, dry winters, one severe drought
PRECIP_60 = [
    62, 45, 80, 120, 95, 110, 30, 15,  8, 42, 70, 88,
    55, 40, 75, 130, 100, 95, 20, 10,  5, 38, 65, 82,
    70, 50, 90, 140, 110, 105, 25, 12,  6, 40, 68, 90,
    48, 35, 68, 115,  88,  92, 18,  8,  4, 35, 60, 78,
    58, 42, 72, 125,  98, 100, 22, 11,  5, 37, 63, 85,
]

# Clearly wet record: every month well above average
PRECIP_WET = [200.0] * 30

# Clearly dry record: every month near zero
PRECIP_DRY = [2.0] * 30


# ---------------------------------------------------------------------------
# Output shape
# ---------------------------------------------------------------------------

def test_output_length_timescale_1():
    result = compute_spi(PRECIP_60, 1)
    assert len(result) == len(PRECIP_60) - 1 + 1  # = 60


def test_output_length_timescale_3():
    result = compute_spi(PRECIP_60, 3)
    assert len(result) == len(PRECIP_60) - 3 + 1  # = 58


def test_output_length_timescale_12():
    result = compute_spi(PRECIP_60, 12)
    assert len(result) == len(PRECIP_60) - 12 + 1  # = 49


# ---------------------------------------------------------------------------
# Value sanity
# ---------------------------------------------------------------------------

def test_spi_values_are_finite():
    result = compute_spi(PRECIP_60, 3)
    assert all(math.isfinite(v) for v in result), "All SPI values must be finite"


def test_spi_values_in_plausible_range():
    result = compute_spi(PRECIP_60, 3)
    assert all(-4.0 <= v <= 4.0 for v in result), (
        "SPI z-scores should fall within [-4, 4] for a realistic record"
    )


def test_spi_mean_near_zero():
    result = compute_spi(PRECIP_60, 1)
    mean = sum(result) / len(result)
    assert abs(mean) < 0.5, f"SPI mean should be near 0, got {mean:.3f}"


# ---------------------------------------------------------------------------
# Directional correctness
# ---------------------------------------------------------------------------

def test_wet_record_positive_spi():
    """A uniformly wet record should produce mostly positive SPI values."""
    result = compute_spi(PRECIP_WET, 1)
    positive_count = sum(1 for v in result if v > 0)
    assert positive_count >= len(result) * 0.6, (
        "Wet record should yield majority positive SPI values"
    )


def test_dry_record_negative_spi():
    """A uniformly dry record should produce mostly negative SPI values."""
    result = compute_spi(PRECIP_DRY, 1)
    negative_count = sum(1 for v in result if v < 0)
    assert negative_count >= len(result) * 0.6, (
        "Dry record should yield majority negative SPI values"
    )


# ---------------------------------------------------------------------------
# Multi-timescale behaviour
# ---------------------------------------------------------------------------

def test_spi1_more_variable_than_spi12():
    """Short-timescale SPI must be more volatile than long-timescale SPI."""
    spi1 = compute_spi(PRECIP_60, 1)
    spi12 = compute_spi(PRECIP_60, 12)
    std1 = statistics.stdev(spi1)
    std12 = statistics.stdev(spi12)
    assert std1 > std12, (
        f"SPI-1 std ({std1:.3f}) should exceed SPI-12 std ({std12:.3f})"
    )


def test_scaling_does_not_change_spi():
    """Multiplying all precipitation by a constant should not change SPI values."""
    spi_base = compute_spi(PRECIP_60, 3)
    spi_scaled = compute_spi([p * 10 for p in PRECIP_60], 3)
    for i, (a, b) in enumerate(zip(spi_base, spi_scaled)):
        assert abs(a - b) < 0.05, (
            f"SPI at index {i} changed after scaling: {a:.3f} vs {b:.3f}"
        )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_short_record_raises():
    """Record shorter than timescale + 1 must raise ValueError."""
    with pytest.raises(ValueError):
        compute_spi([50.0, 60.0, 70.0], timescale=5)


def test_zero_timescale_raises():
    with pytest.raises(ValueError):
        compute_spi(PRECIP_60, timescale=0)


def test_all_zero_precipitation_raises_or_returns_nan():
    """All-zero input has no Gamma signal; function must raise or return NaNs."""
    zeros = [0.0] * 30
    try:
        result = compute_spi(zeros, 1)
        assert all(math.isnan(v) or v == 0.0 for v in result)
    except (ValueError, RuntimeError):
        pass
