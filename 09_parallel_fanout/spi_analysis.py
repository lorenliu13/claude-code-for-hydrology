"""
Standardized Precipitation Index (SPI) computation.
Implement compute_spi below; do not change the function signature.
"""


def compute_spi(precipitation: list[float], timescale: int) -> list[float]:
    """
    Compute the Standardized Precipitation Index for a given timescale.

    Args:
        precipitation: Monthly precipitation totals (mm), chronological order.
        timescale: Rolling aggregation window in months (must be >= 1).

    Returns:
        List of SPI z-scores. Length == len(precipitation) - timescale + 1.

    Raises:
        ValueError: if timescale < 1, or if the record is too short to fit
                    the Gamma distribution (fewer than timescale + 1 values).
        ValueError: if all aggregated totals are zero (no precipitation signal).
    """
    raise NotImplementedError
