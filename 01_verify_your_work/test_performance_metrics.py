"""
Tests for performance_metrics.py using known analytical values.

These tests define what "correct" means — Claude should make all of them pass.
"""
import numpy as np
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from performance_metrics import compute_nse, compute_kge


# --- NSE tests ---

def test_nse_perfect_prediction():
    obs = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
    sim = obs.copy()
    assert compute_nse(obs, sim) == pytest.approx(1.0)


def test_nse_mean_prediction():
    """Predicting the observed mean for every timestep gives NSE = 0."""
    obs = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
    sim = np.full_like(obs, obs.mean())
    assert compute_nse(obs, sim) == pytest.approx(0.0)


def test_nse_negative_for_poor_model():
    """A model that predicts the wrong direction gets NSE < 0."""
    obs = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
    sim = np.array([50.0, 40.0, 30.0, 20.0, 10.0])
    assert compute_nse(obs, sim) < 0.0


def test_nse_known_value():
    """Hand-computed example: obs=[1,2,3], sim=[1,2,4]. mean_obs=2.
    numerator   = (1-1)^2 + (2-2)^2 + (3-4)^2 = 1
    denominator = (1-2)^2 + (2-2)^2 + (3-2)^2 = 2
    NSE = 1 - 1/2 = 0.5
    """
    obs = np.array([1.0, 2.0, 3.0])
    sim = np.array([1.0, 2.0, 4.0])
    assert compute_nse(obs, sim) == pytest.approx(0.5)


# --- KGE tests ---

def test_kge_perfect_prediction():
    obs = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
    sim = obs.copy()
    assert compute_kge(obs, sim) == pytest.approx(1.0)


def test_kge_returns_float():
    obs = np.array([5.0, 10.0, 15.0, 20.0])
    sim = np.array([4.0, 11.0, 14.0, 21.0])
    result = compute_kge(obs, sim)
    assert isinstance(result, float)


def test_kge_scaled_sim():
    """If sim = 2 * obs: r=1, alpha=2, beta=2.
    KGE = 1 - sqrt((1-1)^2 + (2-1)^2 + (2-1)^2) = 1 - sqrt(2) ≈ -0.414
    """
    obs = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
    sim = obs * 2.0
    expected = 1.0 - np.sqrt(2.0)
    assert compute_kge(obs, sim) == pytest.approx(expected, abs=1e-6)


def test_kge_below_one_for_imperfect():
    obs = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
    sim = np.array([12.0, 18.0, 31.0, 39.0, 52.0])
    assert compute_kge(obs, sim) < 1.0
