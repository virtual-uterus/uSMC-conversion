#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sensitivity.py

Computes or plots sweeps and sensitivity to
parameters for a cellML export model
Author: Mathias Roesler
Last modified: 11/24
"""

import sys
import argparse

from conversion import script_fct, plots


def add_shared_arguments(parser):
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
        choices={"l2", "rmse", "mae", "correl", "vrd"},
        help="comparison metric",
    )
    parser.add_argument("param", type=str, help="name of the parameter")
    parser.add_argument(
        "--estrus",
        type=str,
        default="estrus",
        choices={"estrus", "metestrus", "proestrus", "diestrus", "all"},
        help="estrus stage",
    )
    parser.add_argument(
        "--base-estrus",
        type=str,
        default="estrus",
        choices={"estrus", "metestrus", "proestrus", "diestrus"},
        help="estrus stage for the base model",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Tool for performing and plotting parameter sweeps"
    )
    subparsers = parser.add_subparsers(
        title="subcommands",
        description="Available subcommands",
        dest="command",
    )

    # Sweep subparser
    sweep_parser = subparsers.add_parser(
        "sweep", help="Perform a parameter sweep for a given parameter"
    )

    # Add common arguments
    add_shared_arguments(sweep_parser)

    sweep_parser.add_argument(
        "start_val",
        type=float,
        metavar="start-value",
        help="value to start the sweep at",
    )
    sweep_parser.add_argument(
        "end_val",
        type=float,
        metavar="end-value",
        help="value to end the sweep at",
    )
    sweep_parser.add_argument(
        "nb_points",
        metavar="nb-points",
        type=int,
        help="number of points for the parameter sweep",
    )
    sweep_parser.set_defaults(func=script_fct.sweep_func)

    # Plot subparser
    plot_parser = subparsers.add_parser(
        "plot",
        help="Plots the results of a parameter sweep for a given parameter",
    )

    # Add common arguments
    add_shared_arguments(plot_parser)
    plot_parser.set_defaults(func=script_fct.plot_func)

    # Parse input arguments
    args = parser.parse_args()

    try:
        plot_data, params = args.func(args)

        plots.plot_sensitivity_index(plot_data, params, args.metric)
    except Exception as e:
        sys.stderr.write(f"Error: {e}")
        exit()
