import pytest
import numpy as np
from conversion import metrics


def test_l2_norm_correctness():
    # Identical arrays
    y_true = np.array([1, 2, 3])
    y_pred = np.array([1, 2, 3])
    assert metrics.computeL2Norm(y_true, y_pred) == 0

    # Different arrays
    y_true = np.array([1, 2, 3])
    y_pred = np.array([4, 5, 6])
    expected = np.linalg.norm(y_true - y_pred)
    assert np.isclose(metrics.computeL2Norm(y_true, y_pred), expected)


def test_l2_norm_empty_arrays():
    # Empty arrays
    y_true = np.array([])
    y_pred = np.array([])
    with pytest.raises(ValueError):
        metrics.computeL2Norm(y_true, y_pred)


def test_l2_norm_dimension_mismatch():
    # Arrays of different sizes
    y_true = np.array([1, 2, 3])
    y_pred = np.array([1, 2])
    with pytest.raises(ValueError):
        metrics.computeL2Norm(y_true, y_pred)
