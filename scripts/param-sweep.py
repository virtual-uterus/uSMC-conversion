#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
param-sweep.py

Computes a parameters sweep for a cellML export model
Author: Mathias Roesler
Last modified: 11/24
"""

import os
import sys
import argparse

import numpy as np

from conversion import utils, metrics, simulation, plots
from conversion.constants import ESTRUS, RES_DIR

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Perform a parameter sweep for a given parameter"
    )
    parser.add_argument(
        "base_model",
        metavar="base-model",
        type=str,
        choices={"Tong2011", "Tong2014", "Means2023", "Roesler2024"},
        help="base model to compare results with",
    )
    parser.add_argument(
        "sweep_model",
        metavar="sweep-model",
        type=str,
        choices={"Tong2011", "Tong2014", "Means2023", "Roesler2024"},
        help="model to perform the sweep on",
    )
    parser.add_argument(
        "metric",
        type=str,
        choices={"l2", "rmse", "mae", "correl"},
        help="comparison metric",
    )
    parser.add_argument("param", type=str, help="name of the parameter")
    parser.add_argument(
        "start_val",
        type=float,
        metavar="start-value",
        help="value to start the sweep at",
    )
    parser.add_argument(
        "end_val",
        type=float,
        metavar="end-value",
        help="value to end the sweep at",
    )
    parser.add_argument(
        "nb_points",
        metavar="nb-points",
        type=int,
        help="number of points for the parameter sweep",
    )
    parser.add_argument(
        "--estrus",
        type=str,
        default="",
        choices={"", "estrus", "metestrus", "proestrus", "diestrus", "all"},
        help="estrus stage",
    )
    # Parse input arguments
    args = parser.parse_args()

    try:
        # Check that sweep parameters are valid
        simulation.check_sweep_parameters(
            args.start_val,
            args.end_val,
            args.nb_points,
        )

        # Compute base model
        print(f"Computing {args.base_model} simulation with default times")
        t, base_data = simulation.run_simulation(args.base_model)

        # Create values to loop through
        values = np.linspace(args.start_val, args.end_val, args.nb_points)

        # Create arrays to store results
        comp_points = np.zeros(len(values))
        plot_data = []

        if args.estrus == "all":
            estrus = ESTRUS
        else:
            estrus = [args.estrus]

        for stage in estrus:
            # Loop over estrus cycle
            if stage != "":
                print(f"{stage.capitalize()} stage")

            save_file = os.path.join(
                RES_DIR,
                utils.sweep_path(
                    args.base_model,
                    args.sweep_model,
                    args.param,
                    args.metric,
                    stage,
                ),
            )

            for i, value in enumerate(values):
                print(f"  Computing simulation {i+1}")
                _, sweep_data = simulation.run_simulation(
                    args.sweep_model,
                    estrus=stage,
                    param=args.param,
                    value=value,
                )
                comp_points[i] = metrics.compute_comparison(
                    base_data[0, :],
                    sweep_data[0, :],
                    args.metric,
                )

            plot_data.append((comp_points, value, stage))
            utils.save_data(save_file, (comp_points, values, stage))

        plots.plot_sweep_data(plot_data, args.param, args.metric)
    except Exception as e:
        sys.stderr.write(f"Error: {e}")
        exit()
