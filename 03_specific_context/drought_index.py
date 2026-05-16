"""
Drought index calculations.

Implements the Standardized Precipitation Index (SPI), which expresses
precipitation as a z-score relative to a historical baseline. Positive
values indicate wetter than normal conditions; negative values indicate drier.

Reference: McKee et al. (1993)
"""
import numpy as np
from numpy.typing import ArrayLike


def compute_spi(precipitation: ArrayLike) -> np.ndarray:
    """
    Compute the Standardized Precipitation Index for a precipitation series.

    SPI = (P - mean(P)) / std(P)

    Args:
        precipitation: Array of precipitation values (any units, same period length).

    Returns:
        Array of SPI values, same length as input.
        SPI = 0 means exactly average; SPI = -2 means severely dry anomaly.
    """
    p = np.asarray(precipitation, dtype=float)
    mean = p.mean()
    std = p.std(ddof=1)

    if std == 0:
        return np.zeros_like(p)

    # BUG: mean and std are swapped — divides by mean, subtracts std
    return (p - std) / mean
