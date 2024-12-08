#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PNP-comp.py

Compares the results from pregnant and non-pregnant models
Author: Mathias Roesler
Last modified: 11/24
"""

import os
import sys
import argparse

import numpy as np

from conversion import metrics, simulation, utils, plots
from conversion.constants import ESTRUS, RES_DIR


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compares the pregnant and non-pregnant models"
    )
    parser.add_argument(
        "p_model",
        metavar="p-model",
        type=str,
        choices={"Tong2011", "Tong2014", "Means2023"},
        help="pregnant model to compare with",
    )
    parser.add_argument(
        "metric",
        type=str,
        choices={"l2", "rmse", "mae", "correl", "vrd"},
        help="comparison metric",
    )
    parser.add_argument(
        "-p",
        "--plot-only",
        action="store_true",
        help="flag used just to plot data",
    )
    parser.add_argument(
        "-s",
        "--start",
        type=int,
        default=0,
        help="start time for the simulation",
    )
    parser.add_argument(
        "-e",
        "--end",
        type=int,
        default=15000,
        help="end time for the simulation",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=100000,
        help="number of simulation steps",
    )

    args = parser.parse_args()

    np_model = "Roesler2024"

    # Output files
    comp_file = os.path.join(
        RES_DIR,
        f"{args.p_model}_{np_model}_{args.metric}_comp.pkl",
    )
    comp_points = np.zeros(4)  # Comparison points for each stage of estrus
    sim_data = {}  # Dictionnary for simulation data

    try:
        if not args.plot_only:
            print(f"Computing {args.p_model} simulation")
            t, p_data = simulation.run_simulation(
                args.p_model,
                args.start,
                args.end,
                args.steps,
            )
            simulation.save_simulation(args.p_model, p_data[0, :], t)
            sim_data[args.p_model] = p_data[0, :]
            sim_data["time"] = t * 1e-3  # Conver to s

            for i, estrus_stage in enumerate(ESTRUS):
                # Set estrus dependant constants
                print(f"Computing {np_model} {estrus_stage} simulation")
                _, np_data = simulation.run_simulation(
                    "Roesler2024",
                    args.start,
                    args.end,
                    args.steps,
                    estrus_stage,
                )

                # Save model output
                simulation.save_simulation(
                    np_model,
                    np_data[0, :],
                    t,
                    estrus_stage,
                )
                sim_data[estrus_stage] = np_data[0, :]

                comp_points[i] = metrics.compute_comparison(
                    p_data[0, :],
                    np_data[0, :],
                    args.metric,
                    time=t,
                )

            utils.save_data(comp_file, comp_points)

        else:
            try:
                comp_points = utils.load_data(comp_file)

                for estrus_stage in ESTRUS:
                    # Load non-pregnant data
                    np_data = utils.load_data(
                        utils.results_path(
                            np_model,
                            int(args.end * 1e-3),
                            estrus_stage,
                        )
                    )
                    sim_data[estrus_stage] = np_data["data"]
                    sim_data["time"] = np_data["time"] * 1e-3  # Conver to s
            except FileNotFoundError as e:
                sys.stderr.write(f"Error: {e}")
                exit()
            except KeyError as e:
                sys.stderr.write(f"Error: {e} invalid key")
                exit()

        plots.plot_comparison_output(sim_data, comp_points, args.metric)

    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        exit()
