#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plots.py

Plot function for the conversion module
Author: Mathias Roesler
Date: 12/24
"""

import pickle
import numpy as np
import matplotlib.pyplot as plt

from .constants import ESTRUS, COLOURS, LABELS, PARAM


def plot_simulation(data, time):
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

    plt.xlim((time[0], time[len(time) - 1]))

    plt.show()


def plot_PNP_comp(metric):
    """Plots the pregnant and non-pregnant comparison results

    Args:
    metric -- str, metric use for comparison to load the correct data.

    Returns:

    """
    fig, ax = plt.subplots(dpi=300)

    input_file = "../res/{}_comp.pkl".format(metric)

    with open(input_file, "rb") as handler:
        # Unpack pickled data
        pickled_data = pickle.load(handler)

    plt.plot(np.arange(1, 5), pickled_data, ".b")

    # Reset x-axis ticks
    plt.xticks(
        ticks=[1, 2, 3, 4],
        labels=[estrus.capitalize() for estrus in ESTRUS],
    )

    plt.ylabel("Normalised {} (mV)".format(LABELS[metric]))
    plt.show()


def plot_sweep_data(plot_data, param, metric):
    """Plots the comparison data from different stages of the estrus for
    a given parameter and metric

    Args:
    param -- str, name of the parameter to use.
    metric -- str, name of the used metric, {l2, rmse, mae, correl}.

    Returns:

    """
    fig, ax = plt.subplots(dpi=300)

    for comp_points, values, estrus in plot_data:
        comp_points /= np.max(comp_points)  # Normalise the data

        plt.plot(values, comp_points, COLOURS[estrus], linestyle="-")

    plt.legend([estrus.capitalize() for estrus in ESTRUS])

    plt.xlabel(PARAM[param] + r" values (pA.pF$^{-1}$)")
    plt.ylabel("Normalised {} (mV)".format(LABELS[metric]))
    plt.show()


def plot_sensitivity(metric):
    """Plots the results of the sensitivity analysis for a certain metric

    Args:
    metric -- str, name of the used metric, {l2, rmse, mae, correl}.

    Returns:

    """
    fig, ax = plt.subplots(dpi=300)

    values = np.arange(len(PARAM))  # x-values for plot

    for i, stage in enumerate(ESTRUS):
        comp_points = []  # Store the results for each stage

        for j, param in enumerate(PARAM):
            input_file = "../res/{}_{}_{}_sweep.pkl".format(
                param,
                stage,
                metric,
            )

            with open(input_file, "rb") as handler:
                # Unpack pickled data
                pickled_data = pickle.load(handler)
                comp_points.append(pickled_data[0])

        mean = np.mean(comp_points, axis=1)
        std = np.std(comp_points, axis=1)
        _, caps, bars = ax.errorbar(
            values + i * 0.1,
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
    plt.xticks(ticks=values + 0.15, labels=PARAM.values())

    plt.xlabel("Parameters")
    plt.ylabel("{} (mV)".format(LABELS[metric]))
    plt.show()


def plot_comparison_output(sim_output, comp_points, metric):
    """Plots the output of a non-pregnant simulation and the
    comparison metric

    Args:
    sim_output -- dict{str: np.array}, dict containing the simulation
            outputs for each stage in mV and the timesteps in s.
    comp_points -- list, list of comparison points.
    metric -- str, name of the used metric, {l2, rmse, mae, correl}.

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
                9.8,
                10,
                LABELS[metric] + " {:.2f} mV".format(comp_points[cpt]),
                fontsize="x-small",
            )
            ax[i, j].set_xlim([0, int(max(t))])
            # ax[i, j].set_title(ESTRUS[cpt])
            cpt += 1

    # Labels are added on Illustrator
    plt.show()
