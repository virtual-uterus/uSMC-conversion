#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plots.py

Plot function for the conversion module
Author: Mathias Roesler
Date: 12/24
"""

import numpy as np
import matplotlib.pyplot as plt

from .constants import (
    ESTRUS,
    COLOURS,
    LABELS,
    PARAM,
    UNITS,
    LEFT,
    RIGHT,
    BOTTOM,
    Y_LIMS,
)


def plot_single_simulation(data, time):
    """Plots the output of a single simulation

    Args:
    data -- np.array, array containing the data to plot.
    time -- np.array, array of timestamps in seconds.

    Returns:

    Raises:
    ValueError -- if data and time do not have the same shape

    """
    if not data.shape == time.shape:
        raise ValueError("data and time array should have the same shape\n")

    fig, ax = plt.subplots(dpi=300)

    plt.plot(time, data, "-k")
    plt.xlabel("Time (s)")
    plt.ylabel("Membrane potential (mV)")

    plt.xlim((time[0], time[-1]))
    plt.ylim(Y_LIMS)
    plt.subplots_adjust(left=LEFT, right=RIGHT, bottom=BOTTOM)

    plt.show()


def plot_multi_simulation(data, time, param, values):
    """Plots the output of multiple simulation with different
    values of the parameter

    Args:
    data -- np.array, array containing the data to plot.
    time -- np.array, array of timestamps in seconds.
    param -- str, name of the parameter.
    values -- np.array, values of the parameter.

    Returns:

    Raises:
    ValueError -- if data and time do not have the same shape
    ValueError -- if data and values do not have the same length

    """
    if not data.shape[1] == time.shape[0]:
        raise ValueError("data and time array should have the same length\n")

    if not data.shape[0] == values.shape[0]:
        raise ValueError("data and values array should have the same length\n")

    fig, ax = plt.subplots(dpi=300)
    legend = []

    for i, value in enumerate(values):
        plt.plot(time, data[i, :])
        legend.append(f"{PARAM[param]} = {value} {UNITS[param]}")

    plt.xlabel("Time (s)")
    plt.ylabel("Membrane potential (mV)")

    plt.xlim((time[0], time[-1]))
    plt.ylim(Y_LIMS)

    plt.subplots_adjust(left=LEFT, right=RIGHT, bottom=BOTTOM)

    plt.show()


def plot_sensitivity_index(plot_data, params, metric):
    """Plots the sensitivity index from different stages of the estrus for
    all parameters with a given metric

    Args:
    plot_data -- dict(list(tuple), param), dictionnary containing a list of
    tuples with the comparison points, the value of the parameters, and
    the estrus stage as values and the parameter name as the key.
    params -- list(str), list of the keys to plot.
    metric -- str, name of the used metric, {l2, rmse, mae, correl, vrd}.

    Returns:

    Raises:

    """
    fig, ax = plt.subplots(dpi=300)

    np.random.seed(2048)  # Initialise random seed
    param_labels = []  # Labels for the ticks

    for i, param in enumerate(params):
        param_labels.append(PARAM[param])
        for j in range(len(plot_data[param])):
            data_tuple = plot_data[param][j]
            jitter = np.random.uniform(-0.1, 0.1)  # Jitter for the scatter

            # Calculate the sensitivity index for the current stage
            d_max = np.max(data_tuple[0])
            d_min = np.min(data_tuple[0])
            SI = (d_max - d_min) / d_max

            plt.scatter(
                i + jitter,
                SI,
                c=COLOURS[data_tuple[2]],
            )

    # Reset x-axis labels
    ax.set_xticks(np.arange(len(params)))
    ax.set_xticklabels(param_labels)

    plt.ylabel("VRD sensitivity index (%)")

    plt.legend([e.capitalize() for e in ESTRUS])

    # Adjust plot limits
    plt.ylim([0, 1])
    plt.subplots_adjust(left=LEFT, right=RIGHT, bottom=BOTTOM)
    plt.show()


def plot_comparison_output(sim_output, comp_points, metric):
    """Plots the output of a non-pregnant simulation and the
    comparison metric

    Args:
    sim_output -- dict{str: np.array}, dict containing the simulation
            outputs for each stage in mV and the timesteps in s.
    comp_points -- list, list of comparison points.
    metric -- str, name of the used metric, {l2, rmse, mae, correl, vrd}.

    Returns:

    Raises:

    """
    t = sim_output["time"]
    for i in range(len(comp_points)):
        fig, ax = plt.subplots(dpi=300)
        ax.plot(t, sim_output[ESTRUS[i]], color="black")
        ax.text(
            10.7,
            9,
            LABELS[metric] + " {:.2f} (mV)".format(comp_points[i]),
        )
        ax.set_xlim([0, int(max(t))])
        ax.set_ylim(Y_LIMS)
        ax.set_title(ESTRUS[i].capitalize())

        plt.subplots_adjust(left=LEFT, right=RIGHT, bottom=BOTTOM)
        plt.show()
