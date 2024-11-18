#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# param-sweep.py: Computes a parameters sweep for a cellML export model
# Author: Mathias Roesler
# Last modified: 11/24

import sys
import argparse
import pickle
import numpy as np
import Roesler2024
import Means2023
import functions
import plots

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Perform a parameter sweep for a given parameter"
    )

    parser.add_argument("param", type=str, help="name of the parameter")
    parser.add_argument(
        "metric",
        type=str,
        choices={"l2", "rmse", "mae", "correl"},
        help="comparison metric",
    )
    parser.add_argument(
        "model",
        type=str,
        choices={"Means", "Roesler"},
        help="model to compare with",
    )

    # Create subparser for the sweep and plot commands
    subparser = parser.add_subparsers(help="commands", dest="command")

    # Sweep subcommand arguments
    sweep_subparser = subparser.add_parser(
        "sweep",
        help="performs parameter sweep",
    )
    sweep_subparser.add_argument(
        "start_val",
        type=float,
        metavar="start-value",
        help="value to start the sweep at",
    )
    sweep_subparser.add_argument(
        "end_val",
        type=float,
        metavar="end-value",
        help="value to end the sweep at",
    )
    sweep_subparser.add_argument(
        "nb_points",
        metavar="nb-points",
        type=int,
        help="number of points for the parameter sweep",
    )
    sweep_subparser.add_argument(
        "--estrus",
        type=str,
        default="all",
        choices={"estrus", "metestrus", "proestrus", "diestrus", "all"},
        help="estrus stage",
    )

    # Plot subcommand arguments
    plot_subparser = subparser.add_parser(
        "plot",
        help="plots results without doing a parameter sweep",
    )

    # Parse input arguments
    args = parser.parse_args()

    if args.command == "plot":
        # Plot if estrus is all or plot subcommand is used
        plots.plotParamSweep(args.param, args.metric)
        exit()

    # Error check
    try:
        assert args.start_val < args.end_val

    except AssertionError:
        sys.stderr.write("Error: start value must be smaller than end value\n")
        exit(1)

    init_states_R, constants_R = Roesler2024.initConsts()
    init_states_M, constants_M = Means2023.initConsts()
    _, _, _, legend_constants_R = Roesler2024.createLegends()

    # Error check and index retrival
    try:
        _, idx = functions.setParams(
            constants_R,
            legend_constants_R,
            args.param,
            None,
        )

    except IndexError:
        sys.stderr.write(
            "Error: parameter sweep for {} can't be done\n".format(
                args.param,
            )
        )
        exit(1)

    # Error check
    try:
        assert args.nb_points > 0

    except AssertionError:
        sys.stderr.write(
            "Error: the number of points must be greater than 0\n",
        )
        exit(1)

    if args.estrus == "all":
        plot_only = True
        estrus_stage = ["proestrus", "estrus", "metestrus", "diestrus"]

    else:
        estrus_stage = [args.estrus]

    if args.model == "Means":
        # Compute Means model once
        print("Computing original simulation")
        (
            _,
            orig_states,
            _,
        ) = Means2023.solveModel(init_states_M, constants_M)

    for estrus in estrus_stage:
        constants_R = functions.setEstrusParams(
            constants_R,
            legend_constants_R,
            estrus,
        )

        print("{} stage".format(estrus.capitalize()))

        # Original model solution
        if args.model == "Roesler":
            # Recompute for each stage of the cycle
            print("  Computing original simulation")
            (
                _,
                orig_states,
                _,
            ) = Roesler2024.solveModel(init_states_R, constants_R)

        # Preset the size of the comparison points
        values = np.linspace(args.start_val, args.end_val, args.nb_points)
        comp_points = np.zeros(len(values))

        for i, value in enumerate(values):
            # Run the simulations with different values
            print("    Computing simulation {}".format(i + 1))
            constants_R[idx] = value
            (
                _,
                states,
                _,
            ) = Roesler2024.solveModel(init_states_R, constants_R)
            comp_points[i] = functions.computeComparison(
                orig_states[0, :] / max(abs(orig_states[0, :])),
                states[0, :] / max(abs(states[0, :])),
                args.metric,
            )

        print("  Writing results\n")
        output_file = "../res/{}_{}_{}_sweep.pkl".format(
            args.param, estrus, args.metric
        )

        with open(output_file, "wb") as handler:
            pickle.dump([comp_points, values], handler)
