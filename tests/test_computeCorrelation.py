import pytest
import numpy as np
from conversion import metrics


def test_correlation_correctness():
    # Identical arrays (correlation should be 1)
    y_true = np.array([1, 2, 3])
    y_pred = np.array([1, 2, 3])
    epsilon = 1e-6
    assert metrics.computeCorrelation(y_true, y_pred) - 1 < epsilon

    # Inversely correlated arrays (correlation should be -1)
    y_true = np.array([1, 2, 3])
    y_pred = np.array([3, 2, 1])
    assert metrics.computeCorrelation(y_true, y_pred) + 1 < epsilon

    # No correlation (correlation should be around 0)
    y_true = np.array([1, 2, 3])
    y_pred = np.array([10, 11, 12])
    assert np.isclose(metrics.computeCorrelation(y_true, y_pred), 1.0)


def test_correlation_empty_arrays():
    # Empty arrays
    y_true = np.array([])
    y_pred = np.array([])
    with pytest.raises(ValueError):
        metrics.computeCorrelation(y_true, y_pred)


def test_correlation_with_nan():
    # Arrays with NaN values
    y_true = np.array([1, 2, np.nan])
    y_pred = np.array([1, 2, 3])
    with pytest.raises(ValueError):
        metrics.computeCorrelation(y_true, y_pred)
