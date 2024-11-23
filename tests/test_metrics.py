#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_metrics.py

Unit tests for the metrics functions in metrics.py.
Author: Mathias Roesler
Date: 11/24

This file contains test cases for the functions:
- computeL2Norm
- computeRMSE
- computeMAE
- computeCorrelation
- computeComparison

The tests cover various scenarios including valid inputs, invalid inputs,
and edge cases.
"""

import pytest
import numpy as np
import sklearn.metrics as skm

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


def test_mae_correctness():
    # Identical arrays
    y_true = np.array([1, 2, 3])
    y_pred = np.array([1, 2, 3])
    assert metrics.computeMAE(y_true, y_pred) == 0

    # Different arrays
    y_true = np.array([1, 2, 3])
    y_pred = np.array([4, 5, 6])
    expected = skm.mean_absolute_error(y_true, y_pred)
    assert np.isclose(metrics.computeMAE(y_true, y_pred), expected)


def test_mae_empty_arrays():
    # Empty arrays
    y_true = np.array([])
    y_pred = np.array([])
    with pytest.raises(ValueError):
        metrics.computeMAE(y_true, y_pred)


def test_mae_dimension_mismatch():
    # Arrays of different sizes
    y_true = np.array([1, 2, 3])
    y_pred = np.array([1, 2])
    with pytest.raises(ValueError):
        metrics.computeMAE(y_true, y_pred)


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
