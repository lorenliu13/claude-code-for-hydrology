"""
USGS gauge data retrieval and processing.

Uses the USGS National Water Information System (NWIS) Instantaneous Values API
to retrieve streamflow data from stream gauges across the US.

API documentation: https://waterservices.usgs.gov/rest/IV-Service.html
"""
import json
import urllib.request
import urllib.parse
from datetime import datetime

import numpy as np

NWIS_IV_URL = "https://waterservices.usgs.gov/nwis/iv/"
STREAMFLOW_PARAM = "00060"  # discharge in ft³/s


def fetch_usgs_streamflow(site_id: str, start_date: str, end_date: str) -> dict:
    """
    Fetch streamflow data from the USGS NWIS Instantaneous Values API.

    Args:
        site_id:    8-digit USGS site number, e.g. "06610000"
        start_date: ISO date string "YYYY-MM-DD"
        end_date:   ISO date string "YYYY-MM-DD"

    Returns:
        Parsed JSON response dict from the NWIS API
    """
    pass


def parse_nwis_response(response: dict) -> list[tuple[datetime, float]]:
    """
    Extract a time series of (datetime, discharge_cfs) from a NWIS JSON response.

    Skips records whose value equals the NWIS no-data sentinel (-999999).

    Returns:
        List of (datetime, float) tuples, one per valid measurement, in time order
    """
    pass


def compute_flow_exceedance(flows: list[float], exceedance_pct: float) -> float:
    """
    Return the flow value at a given exceedance probability (flow duration curve).

        exceedance_pct=50  -> median flow (Q50), exceeded half the time
        exceedance_pct=10  -> high flow (Q10), exceeded 10% of the time
        exceedance_pct=90  -> low flow (Q90), exceeded 90% of the time

    Args:
        flows:          list of discharge values (ft3/s)
        exceedance_pct: exceedance probability in [0, 100]

    Returns:
        Flow value (ft3/s) at the given exceedance probability
    """
    pass


def flag_flood_events(flows: list[float], threshold_cfs: float) -> list[bool]:
    """
    Return a boolean list marking timesteps where flow strictly exceeds threshold.

    Args:
        flows:         list of discharge values (ft3/s)
        threshold_cfs: flood stage threshold in ft3/s

    Returns:
        List of bool, True where flow > threshold_cfs
    """
    pass
