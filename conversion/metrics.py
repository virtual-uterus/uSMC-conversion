#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
metrics.py

Functions for computing different comparison metrics
Author: Mathias Roesler
Date: 11/24
"""

import numpy as np
import sklearn.metrics as skm
import scipy.stats as stat


def compute_L2_norm(y_true, y_pred):
    """Computes the Euclidean distance between y_true and y_pred

    Arguments:
    y_true -- np.array, ground truth values.
    y_pred -- np.array, estimated values.

    Return:
    l2 -- float, Euclidean distance.

    Raises:
    ValueError -- if one of the arrays is empty.

    """
    if len(y_true) == 0:
        raise ValueError("Error: empty array y_true\n")
    if len(y_pred) == 0:
        raise ValueError("Error: empty array y_pred\n")

    return np.linalg.norm(y_true - y_pred)


def compute_mae(y_true, y_pred):
    """Computes the Mean Absolute Error between y_true and y_pred

    Arguments:
    y_true -- np.array, ground truth values.
    y_pred -- np.array, estimated values.

    Return:
    mae -- float, mean absolute error.

    """
    return skm.mean_absolute_error(y_true, y_pred)


def compute_rmse(y_true, y_pred):
    """Computes the Root Mean Squared Error between y_true and y_pred

    Arguments:
    y_true -- np.array, ground truth values.
    y_pred -- np.array, estimated values.

    Return:
    rmse -- float, root mean square error

    """
    return skm.mean_squared_error(y_true, y_pred, squared=False)


def compute_correlation(y_true, y_pred):
    """Computes the Pearson correlation between y_true and y_pred

    Arguments:
    y_true -- np.array, ground truth values.
    y_pred -- np.array, estimated values.

    Return:
    correl -- float, Pearson correlation

    """
    correl, _ = stat.pearsonr(y_true, y_pred)
    return correl


def compute_comparison(y_true, y_pred, metric):
    """Computes the comparison between y_true and y_pred based on the metric

    Arguments:
    y_true -- np.array, ground truth values.
    y_pred -- np.array, estimated values.
    metric -- str, comparison metric, {l2, rmse, mae, correl}.

    Return:
    comp_point -- float, comparison point.

    Raises:
    ValueError -- if the provided metric is not one of
    {'l2', 'rmse', 'mae', 'correl'}.
    """
    match metric:
        case "l2":
            return compute_L2_norm(y_true, y_pred)

        case "rmse":
            return compute_rmse(y_true, y_pred)

        case "mae":
            return compute_mae(y_true, y_pred)

        case "correl":
            return compute_correlation(y_true, y_pred)
        case _:
            raise ValueError("Error: invalid metric {}\n".format(metric))
