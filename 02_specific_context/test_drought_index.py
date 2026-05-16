"""Tests for drought_index.py."""
import numpy as np
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from drought_index import compute_spi


def test_spi_of_mean_is_zero():
    """The SPI of the mean precipitation value must be exactly 0.

    Physically: a month with exactly average rainfall has no anomaly (SPI = 0).
    This is the most fundamental property of a z-score.
    """
    precip = np.array([50.0, 80.0, 60.0, 70.0, 90.0, 40.0, 75.0, 55.0, 65.0, 85.0])
    spi = compute_spi(precip)

    mean_precip = precip.mean()
    mean_index = np.argmin(np.abs(precip - mean_precip))

    assert abs(spi[mean_index]) < 0.05, (
        f"SPI at the mean precipitation ({precip[mean_index]:.1f} mm) "
        f"should be ~0 but got {spi[mean_index]:.4f}. "
        "Check that the SPI formula subtracts the mean and divides by std."
    )


def test_spi_length():
    precip = np.array([30.0, 50.0, 70.0, 90.0, 110.0])
    assert len(compute_spi(precip)) == len(precip)


def test_spi_wet_month_positive():
    """A month much wetter than average should have positive SPI."""
    precip = np.array([50.0, 55.0, 48.0, 52.0, 200.0])
    spi = compute_spi(precip)
    assert spi[-1] > 1.0, "Extremely wet month should have SPI > 1"


def test_spi_dry_month_negative():
    """A month much drier than average should have negative SPI."""
    precip = np.array([50.0, 55.0, 48.0, 52.0, 5.0])
    spi = compute_spi(precip)
    assert spi[-1] < -1.0, "Extremely dry month should have SPI < -1"


def test_spi_constant_series():
    """Constant precipitation has no variability — all SPI values are 0."""
    precip = np.full(12, 60.0)
    spi = compute_spi(precip)
    assert np.all(spi == 0.0)
