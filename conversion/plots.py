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

    plt.legend(legend, fontsize="x-small")
    plt.subplots_adjust(left=LEFT, right=RIGHT, bottom=BOTTOM)

    plt.show()


def plot_sweep_data(plot_data, param, metric):
    """Plots the comparison data from different stages of the estrus for
    a given parameter and metric

    Args:
    param -- str, name of the parameter to use.
    metric -- str, name of the used metric, {l2, rmse, mae, correl, vrd}.

    Returns:

    """
    fig, ax = plt.subplots(dpi=300)

    for comp_points, values, estrus in plot_data:
        comp_points /= np.max(comp_points)  # Normalise the data

        plt.plot(values, comp_points, COLOURS[estrus], linestyle="-")

    plt.legend([estrus.capitalize() for estrus in ESTRUS])

    plt.xlabel(PARAM[param] + r" values (pA pF$^{-1}$)")
    plt.ylabel("Normalised {}".format(LABELS[metric]))

    plt.subplots_adjust(left=LEFT, right=RIGHT, bottom=BOTTOM)
    plt.show()


def plot_sensitivity(plot_data, metric):
    """Plots the results of the sensitivity analysis for a certain metric

    Args:
    plot_data -- dict(list(tuple)), dictionnary with the parameter name as key
    and list of comparison points, parameter values, and the estrus stage for
    each sweep as values.
    metric -- str, name of the used metric, {l2, rmse, mae, correl, vrd}.

    Returns:

    """
    fig, ax = plt.subplots(dpi=300)

    for i, param in enumerate(plot_data.keys()):
        data = plot_data[param]
        comp_points = []  # Store the results for each stage

        for j in range(len(data)):
            comp_points = data[j][0]
            stage = data[j][2]

            mean = np.mean(comp_points)
            std = np.std(comp_points)

            _, caps, bars = ax.errorbar(
                i + j * 0.1,
                mean,
                yerr=std,
                fmt=COLOURS[stage],
                linestyle="",
                capsize=3,
            )

            # Change cap marker
            caps[0].set_marker("_")
            caps[1].set_marker("_")

    plt.legend([estrus.capitalize() for estrus in ESTRUS])

    # Reset x-axis ticks
    plt.xticks(
        ticks=np.arange(len(plot_data.keys())) + 0.15,
        labels=PARAM.values(),
    )

    plt.xlabel("Parameters")
    plt.ylabel("{}".format(LABELS[metric]))

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
    fig, ax = plt.subplots(2, 2, dpi=300, sharex=True, sharey=True)

    cpt = 0
    t = sim_output["time"]

    for i in range(2):
        for j in range(2):
            ax[i, j].plot(t, sim_output[ESTRUS[cpt]], color="black")
            ax[i, j].text(
                10.7,
                9,
                LABELS[metric] + " {:.2f}".format(comp_points[cpt]),
                fontsize="x-small",
            )
            ax[i, j].set_xlim([0, int(max(t))])
            # ax[i, j].set_title(ESTRUS[cpt])
            cpt += 1

    # Labels are added on Illustrator
    plt.subplots_adjust(left=LEFT, right=RIGHT, bottom=BOTTOM)
    plt.show()
