import pytest
import numpy as np
from conversion import metrics
import sklearn.metrics as skm


def test_rmse_correctness():
    # Identical arrays
    y_true = np.array([1, 2, 3])
    y_pred = np.array([1, 2, 3])
    assert metrics.computeRMSE(y_true, y_pred) == 0

    # Different arrays
    y_true = np.array([1, 2, 3])
    y_pred = np.array([4, 5, 6])
    expected = skm.mean_squared_error(y_true, y_pred, squared=False)
    assert np.isclose(metrics.computeRMSE(y_true, y_pred), expected)


def test_rmse_empty_arrays():
    # Empty arrays
    y_true = np.array([])
    y_pred = np.array([])
    with pytest.raises(ValueError):
        metrics.computeRMSE(y_true, y_pred)


def test_rmse_dimension_mismatch():
    # Arrays of different sizes
    y_true = np.array([1, 2, 3])
    y_pred = np.array([1, 2])
    with pytest.raises(ValueError):
        metrics.computeRMSE(y_true, y_pred)
