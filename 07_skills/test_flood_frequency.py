import pytest
from datetime import date
from flood_frequency import (
    extract_annual_maxima,
    weibull_return_periods,
    estimate_quantile,
    data_quality_summary,
)


# ---------------------------------------------------------------------------
# extract_annual_maxima
# ---------------------------------------------------------------------------

def test_single_water_year():
    flows = [100.0, 200.0, 150.0]
    dates = [date(2020, 1, 1), date(2020, 6, 15), date(2020, 9, 1)]
    assert extract_annual_maxima(flows, dates) == {2020: 200.0}


def test_two_water_years_split_at_october():
    # WY 2020 = Oct 2019 – Sep 2020; WY 2021 = Oct 2020 – Sep 2021
    flows = [80.0, 500.0, 300.0]
    dates = [date(2020, 3, 1), date(2020, 10, 15), date(2021, 2, 1)]
    result = extract_annual_maxima(flows, dates)
    assert result[2020] == 80.0
    assert result[2021] == 500.0


def test_oct_1_belongs_to_next_water_year():
    flows = [100.0, 600.0]
    dates = [date(2020, 9, 30), date(2020, 10, 1)]
    result = extract_annual_maxima(flows, dates)
    assert result[2020] == 100.0   # Sep 30 → WY 2020
    assert result[2021] == 600.0   # Oct 1  → WY 2021


def test_missing_sentinel_excluded():
    flows = [-999999.0, 400.0, 200.0]
    dates = [date(2020, 1, 1), date(2020, 4, 1), date(2020, 7, 1)]
    result = extract_annual_maxima(flows, dates)
    assert result[2020] == 400.0


def test_year_with_only_sentinels_absent_from_result():
    flows = [-999999.0, -999999.0, 300.0]
    dates = [date(2020, 1, 1), date(2020, 6, 1), date(2021, 3, 1)]
    result = extract_annual_maxima(flows, dates)
    assert 2020 not in result
    assert result[2021] == 300.0


# ---------------------------------------------------------------------------
# weibull_return_periods
# ---------------------------------------------------------------------------

def test_weibull_three_values_return_periods():
    # n=3: T = (3+1)/rank → rank1=4.0, rank2=2.0, rank3=4/3≈1.333
    result = weibull_return_periods([100.0, 200.0, 300.0])
    periods = [t for t, _ in result]
    discharges = [q for _, q in result]
    assert discharges == sorted(discharges), "must be sorted ascending by discharge"
    assert abs(periods[0] - 4.0) < 0.01    # smallest Q → longest T
    assert abs(periods[1] - 2.0) < 0.01
    assert abs(periods[2] - 4 / 3) < 0.01  # largest Q → shortest T


def test_weibull_single_value():
    result = weibull_return_periods([500.0])
    assert len(result) == 1
    assert abs(result[0][0] - 2.0) < 0.01   # T = (1+1)/1 = 2


def test_weibull_order_independent_of_input_order():
    result_a = weibull_return_periods([300.0, 100.0, 200.0])
    result_b = weibull_return_periods([100.0, 200.0, 300.0])
    assert result_a == result_b


# ---------------------------------------------------------------------------
# estimate_quantile
# ---------------------------------------------------------------------------

def test_quantile_at_rank2_return_period():
    # n=3: rank-2 value (200 cfs) sits at T=2 years
    result = estimate_quantile([100.0, 200.0, 300.0], 2.0)
    assert abs(result - 200.0) < 10.0


def test_quantile_raises_for_out_of_range():
    with pytest.raises(ValueError):
        estimate_quantile([100.0, 200.0, 300.0], 500.0)


def test_quantile_interpolates_between_points():
    maxima = [100.0, 200.0, 300.0, 400.0]
    # Should return a value between the two bounding observed discharges
    q = estimate_quantile(maxima, 2.5)
    assert 100.0 < q < 400.0


# ---------------------------------------------------------------------------
# data_quality_summary
# ---------------------------------------------------------------------------

def test_good_quality_all_clean():
    flows = [100.0, 200.0, 150.0, 300.0]
    r = data_quality_summary(flows)
    assert r["total"] == 4
    assert r["missing"] == 0
    assert r["negative"] == 0
    assert r["clean_count"] == 4
    assert r["quality_grade"] == "GOOD"


def test_fair_quality_moderate_missing():
    # 2 of 20 missing = 10 %
    flows = [100.0] * 18 + [-999999.0, -999999.0]
    r = data_quality_summary(flows)
    assert r["missing"] == 2
    assert r["quality_grade"] == "FAIR"


def test_poor_quality_due_to_negatives():
    flows = [100.0, -5.0, 200.0]
    r = data_quality_summary(flows)
    assert r["negative"] == 1
    assert r["quality_grade"] == "POOR"


def test_poor_quality_high_missing_fraction():
    # 4 of 10 missing = 40 %
    flows = [100.0] * 6 + [-999999.0] * 4
    r = data_quality_summary(flows)
    assert r["quality_grade"] == "POOR"


def test_clean_count_excludes_sentinel_and_negatives():
    flows = [100.0, -999999.0, -3.0, 200.0]
    r = data_quality_summary(flows)
    assert r["clean_count"] == 2
