"""
Hydrological model performance metrics.

NSE (Nash-Sutcliffe Efficiency) and KGE (Kling-Gupta Efficiency) are standard
metrics for evaluating how well a hydrological model reproduces observed streamflow.
"""
import numpy as np
from numpy.typing import ArrayLike


def compute_nse(observed: ArrayLike, simulated: ArrayLike) -> float:
    """
    Compute Nash-Sutcliffe Efficiency.

    NSE = 1 - sum((obs - sim)^2) / sum((obs - mean(obs))^2)

    Returns:
        float in (-inf, 1]. 1.0 = perfect, 0.0 = no better than mean prediction.
    """
    pass


def compute_kge(observed: ArrayLike, simulated: ArrayLike) -> float:
    """
    Compute Kling-Gupta Efficiency.

    KGE = 1 - sqrt((r - 1)^2 + (alpha - 1)^2 + (beta - 1)^2)
    where:
        r     = Pearson correlation coefficient
        alpha = std(simulated) / std(observed)   (variability ratio)
        beta  = mean(simulated) / mean(observed) (bias ratio)

    Returns:
        float in (-inf, 1]. 1.0 = perfect.
    """
    pass
