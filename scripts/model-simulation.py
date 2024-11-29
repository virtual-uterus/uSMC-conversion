#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
model-simulation.py

Runs a simulation for a given model
Author: Mathias Roesler
Last modified: 11/24
"""

import sys
import argparse
from conversion import plots, simulation, utils

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Runs a simulation for a given model",
    )

    parser.add_argument(
        "model",
        type=str,
        choices={"Tong2011", "Tong2014", "Means2023", "Roesler2024"},
        help="model to use",
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
        type=float,
        default=0,
        help="start time for the simulation",
    )
    parser.add_argument(
        "-e",
        "--end",
        type=float,
        default=15000,
        help="end time for the simulation",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=100000,
        help="number of simulation steps",
    )
    parser.add_argument(
        "--estrus",
        type=str,
        choices={"", "proestrus", "estrus", "metestrus", "diestrus"},
        default="",
        help="estrus stage for the Roesler2024 model",
    )

    args = parser.parse_args()

    try:
        if not args.plot_only:
            time, data = simulation.run_simulation(
                args.model,
                args.start,
                args.end,
                args.steps,
                args.estrus,
            )
            sim_data = data[0, :]
            simulation.save_simulation(args.model, sim_data, time, args.estrus)

        else:
            res_file = utils.results_path(
                args.model,
                int(args.end * 1e-3),
                args.estrus,
            )
            data = utils.load_data(res_file)
            sim_data = data["data"]
            time = data["time"]

        # Plot results
        plots.plot_simulation(sim_data, time / 1e3)

    except Exception as e:
        sys.stderr.write(f"Error: {e}")
        exit()
