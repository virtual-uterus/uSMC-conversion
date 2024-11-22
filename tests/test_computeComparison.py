import pytest
import numpy as np
from conversion import metrics


def test_comparison_correctness():
    y_true = np.array([1, 2, 3])
    y_pred = np.array([1, 2, 3])

    # Test each metric
    assert np.isclose(metrics.computeComparison(y_true, y_pred, "l2"), 0)
    assert np.isclose(metrics.computeComparison(y_true, y_pred, "mae"), 0)
    assert np.isclose(metrics.computeComparison(y_true, y_pred, "rmse"), 0)
    assert np.isclose(metrics.computeComparison(y_true, y_pred, "correl"), 1)


def test_comparison_invalid_metric():
    y_true = np.array([1, 2, 3])
    y_pred = np.array([1, 2, 3])

    # Invalid metric
    with pytest.raises(ValueError):
        metrics.computeComparison(y_true, y_pred, "invalid_metric")


def test_comparison_dimension_mismatch():
    y_true = np.array([1, 2, 3])
    y_pred = np.array([1, 2])

    with pytest.raises(ValueError):
        metrics.computeComparison(y_true, y_pred, "l2")
