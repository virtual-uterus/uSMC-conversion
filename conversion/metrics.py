#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
metrics.py

Functions for computing different comparison metrics
Author: Mathias Roesler
Date: 11/24
"""

import conversion.utils

import numpy as np
import sklearn.metrics as skm
import scipy.stats as stat

from elephant.spike_train_dissimilarity import van_rossum_distance


def compute_L2_norm(y_true, y_pred):
    """Computes the Euclidean distance between y_true and y_pred

    Args:
    y_true -- np.array, ground truth values.
    y_pred -- np.array, estimated values.

    Returns:
    l2 -- float, Euclidean distance.

    Raises:
    ValueError -- if one of the arrays is empty.

    """
    if len(y_true) == 0:
        raise ValueError("empty array y_true")
    if len(y_pred) == 0:
        raise ValueError("empty array y_pred")

    return np.linalg.norm(y_true - y_pred)


def compute_mae(y_true, y_pred):
    """Computes the Mean Absolute Error between y_true and y_pred

    Args:
    y_true -- np.array, ground truth values.
    y_pred -- np.array, estimated values.

    Returns:
    mae -- float, mean absolute error.

    """
    return skm.mean_absolute_error(y_true, y_pred)


def compute_rmse(y_true, y_pred):
    """Computes the Root Mean Squared Error between y_true and y_pred

    Args:
    y_true -- np.array, ground truth values.
    y_pred -- np.array, estimated values.

    Returns:
    rmse -- float, root mean square error

    """
    return skm.mean_squared_error(y_true, y_pred, squared=False)


def compute_correlation(y_true, y_pred):
    """Computes the Pearson correlation between y_true and y_pred

    Args:
    y_true -- np.array, ground truth values.
    y_pred -- np.array, estimated values.

    Returns:
    correl -- float, Pearson correlation

    """
    correl, _ = stat.pearsonr(y_true, y_pred)
    return correl


def compute_van_rossum_distance(y_true, y_pred, time, tau=1.0):
    """Computes the Van Rossum distance between two spike trains.

    Args:
    y_true -- np.array, ground truth values.
    y_pred -- np.array, estimated values.
    time -- np.array, corresponding time points.
    tau -- float, time constant for the exponential kernel, default: 1.

    Returns:
    distance -- float, Van Rossum distance.
    """
    st_true = conversion.utils.create_spike_train(
        conversion.utils.extract_spike_times(y_true, time),
        time[-1],
    )
    st_pred = conversion.utils.create_spike_train(
        conversion.utils.extract_spike_times(y_pred, time),
        time[-1],
    )
    return van_rossum_distance(
        [st_true, st_pred],
        tau * conversion.utils.quant.s,
    )[0, 1]


def compute_comparison(y_true, y_pred, metric, tau=1.0, time=np.array([])):
    """Computes the comparison between y_true and y_pred based on the metric

    Args:
    y_true -- np.array or SpikeTrain object, ground truth values.
    y_pred -- np.array or SpikeTrain object, estimated values.
    metric -- str, comparison metric, {l2, rmse, mae, correl, vrd}.
    tau -- float, time constant for the exponential kernel in the
    Van Rossum distance, default: 1.
    time -- np.array, corresponding time points, default: [].

    Returns:
    comp_point -- float, comparison point.

    Raises:
    ValueError -- if the provided metric is not one of
    {'l2', 'rmse', 'mae', 'correl', 'vrd'}.

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
        case "vrd":
            return compute_van_rossum_distance(y_true, y_pred, time, tau)
        case _:
            raise ValueError("invalid metric {}".format(metric))
