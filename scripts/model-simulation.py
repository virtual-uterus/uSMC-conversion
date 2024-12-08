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

import numpy as np

from conversion import plots, script_fct, metrics
from conversion.utils import ESTRUS_PARAMS


def add_shared_arguments(parser):
    parser.add_argument(
        "model",
        type=str,
        choices={"Tong2011", "Tong2014", "Means2023", "Roesler2024"},
        help="model to use",
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
        choices={"proestrus", "estrus", "metestrus", "diestrus"},
        default="estrus",
        help="estrus stage for the Roesler2024 model",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Tool for performing model simulations"
    )
    subparsers = parser.add_subparsers(
        title="subcommands",
        description="Available subcommands",
        dest="command",
    )

    # Single subparser
    single_parser = subparsers.add_parser(
        "single",
        help="Perform a single simulation and plots results",
    )
    # Add common arguments
    add_shared_arguments(single_parser)

    single_parser.add_argument(
        "-p",
        "--plot-only",
        action="store_true",
        help="flag used just to plot data",
    )

    single_parser.set_defaults(func=script_fct.single_func)

    # Multi subparser
    multi_parser = subparsers.add_parser(
        "multi",
        help="Perform multiple simulations changing a parameter",
    )

    # Add common arguments
    add_shared_arguments(multi_parser)

    multi_parser.add_argument("param", type=str, help="name of the parameter")
    multi_parser.add_argument(
        "values",
        type=float,
        nargs="+",
        help="values of the parameter to use",
    )
    multi_parser.set_defaults(func=script_fct.multi_func)

    args = parser.parse_args()

    try:
        sim_data, time = args.func(args)

        if args.command == "single":
            plots.plot_single_simulation(sim_data, time / 1e3)

            # Hardcoded comparison between first and last event
            if args.end == 210000 and args.start == 0:
                stim_duration = 10000  # Hardcoded value of stim duration
                duration = ESTRUS_PARAMS[args.estrus]["stim_interval"] + \
                    stim_duration
                nb_events = int(args.end // duration)

                first_event = sim_data[0:12000]
                last_event = sim_data[
                    duration * nb_events - 1000: duration * nb_events
                    + (stim_duration + 1000)
                ]
                vrd = metrics.compute_comparison(
                    first_event, last_event, "vrd", time=time
                )
                print("First and last event VRD: {:.2f}".format(vrd))

        else:
            plots.plot_multi_simulation(
                sim_data, time / 1e3, args.param, np.array(args.values)
            )

    except Exception as e:
        sys.stderr.write(f"Error: {e}")
        exit()
