"""
Tests for usgs_gauge.py using a fixture NWIS response.

The fixture in fixtures/nwis_response.json is a real-format USGS NWIS response
for site 06610000 (Missouri River at Omaha, NE), parameter 00060 (streamflow).
"""
import json
import pytest
from datetime import datetime
from pathlib import Path

from usgs_gauge import parse_nwis_response, compute_flow_exceedance, flag_flood_events

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "nwis_response.json"


@pytest.fixture
def nwis_response():
    with open(FIXTURE_PATH) as f:
        return json.load(f)


class TestParseNwisResponse:
    def test_returns_five_records(self, nwis_response):
        records = parse_nwis_response(nwis_response)
        assert len(records) == 5

    def test_each_record_is_datetime_float(self, nwis_response):
        records = parse_nwis_response(nwis_response)
        for dt, flow in records:
            assert isinstance(dt, datetime)
            assert isinstance(flow, float)

    def test_flow_values_match_fixture(self, nwis_response):
        records = parse_nwis_response(nwis_response)
        flows = [flow for _, flow in records]
        assert flows == [12400.0, 12300.0, 12200.0, 12100.0, 12000.0]

    def test_skips_no_data_sentinel(self):
        response = {
            "value": {
                "timeSeries": [
                    {
                        "variable": {"noDataValue": -999999.0},
                        "values": [
                            {
                                "value": [
                                    {"value": "500", "dateTime": "2023-06-01T00:00:00.000-05:00"},
                                    {"value": "-999999", "dateTime": "2023-06-01T01:00:00.000-05:00"},
                                    {"value": "600", "dateTime": "2023-06-01T02:00:00.000-05:00"},
                                ]
                            }
                        ],
                    }
                ]
            }
        }
        records = parse_nwis_response(response)
        assert len(records) == 2


class TestComputeFlowExceedance:
    def test_q50_is_median(self):
        flows = [10.0, 20.0, 30.0, 40.0, 50.0]
        assert compute_flow_exceedance(flows, 50) == 30.0

    def test_q0_is_maximum(self):
        flows = [10.0, 20.0, 30.0, 40.0, 50.0]
        assert compute_flow_exceedance(flows, 0) == 50.0

    def test_q100_is_minimum(self):
        flows = [10.0, 20.0, 30.0, 40.0, 50.0]
        assert compute_flow_exceedance(flows, 100) == 10.0

    def test_q10_returns_high_flow(self):
        # flows 1..100: the top 10% are values >= 90
        flows = list(range(1, 101))
        assert compute_flow_exceedance(flows, 10) >= 90.0


class TestFlagFloodEvents:
    def test_all_below_threshold(self):
        flows = [100.0, 200.0, 300.0]
        assert flag_flood_events(flows, 400.0) == [False, False, False]

    def test_all_above_threshold(self):
        flows = [500.0, 600.0, 700.0]
        assert flag_flood_events(flows, 400.0) == [True, True, True]

    def test_mixed_values(self):
        flows = [100.0, 500.0, 200.0, 800.0]
        assert flag_flood_events(flows, 400.0) == [False, True, False, True]

    def test_equal_to_threshold_is_not_flagged(self):
        # strictly greater than, not greater-than-or-equal
        flows = [400.0]
        assert flag_flood_events(flows, 400.0) == [False]
