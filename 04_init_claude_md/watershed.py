"""Watershed runoff calculations using the Rational Method."""


def compute_peak_runoff(rainfall_intensity, area_km2, runoff_coefficient):
    """
    Estimate peak runoff rate using the Rational Method.

    Q = C * i * A / 360

    Args:
        rainfall_intensity: design storm intensity in mm/hr
        area_km2: catchment area in km²
        runoff_coefficient: dimensionless C value (0–1), e.g. 0.3 for grassland

    Returns:
        peak runoff in m³/s
    """
    if not 0.0 <= runoff_coefficient <= 1.0:
        raise ValueError("runoff_coefficient must be between 0 and 1")
    if rainfall_intensity < 0:
        raise ValueError("rainfall_intensity must be non-negative")
    if area_km2 <= 0:
        raise ValueError("area_km2 must be positive")
    return (runoff_coefficient * rainfall_intensity * area_km2) / 360.0


def estimate_time_of_concentration(length_m, slope_m_per_m, manning_n=0.05):
    """
    Estimate time of concentration (Tc) using the Kirpich formula.

    Tc = 0.0195 * (L / S^0.5)^0.77   (minutes)

    Args:
        length_m: longest flow path length in metres
        slope_m_per_m: average channel slope (dimensionless)
        manning_n: Manning's roughness (not used in Kirpich, kept for API compat)

    Returns:
        time of concentration in minutes
    """
    if length_m <= 0:
        raise ValueError("length_m must be positive")
    if slope_m_per_m <= 0:
        raise ValueError("slope_m_per_m must be positive")
    return 0.0195 * ((length_m / (slope_m_per_m ** 0.5)) ** 0.77)


def runoff_volume(rainfall_depth_mm, area_km2, runoff_coefficient):
    """
    Compute total runoff volume for a storm event.

    V = C * P * A   (converted to m³)

    Args:
        rainfall_depth_mm: total storm depth in mm
        area_km2: catchment area in km²
        runoff_coefficient: dimensionless C value (0–1)

    Returns:
        runoff volume in m³
    """
    if not 0.0 <= runoff_coefficient <= 1.0:
        raise ValueError("runoff_coefficient must be between 0 and 1")
    if rainfall_depth_mm < 0:
        raise ValueError("rainfall_depth_mm must be non-negative")
    if area_km2 <= 0:
        raise ValueError("area_km2 must be positive")
    area_m2 = area_km2 * 1e6
    depth_m = rainfall_depth_mm / 1000.0
    return runoff_coefficient * rainfall_depth_mm / 1000.0 * area_m2
