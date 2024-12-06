#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
script_fct.py

Functions used in the scripts
Author: Mathias Roesler
Date: 11/24
"""

import numpy as np

from conversion.constants import ESTRUS
from conversion import utils, simulation


def sweep_func(args):
    """Function called by the param-sweep script to run the parameter sweep

    The data for the comparison is saved in RES_DIR.

    Args:
    args -- argparse.Namespace with following arguments:
      base_model -- str, name of the base model for comparison from
      {"Roesler2024", "Means2023", "Tong2011", "Tong2014"}.
      sweep_model -- str, name of the model to use from
      {"Roesler2024", "Means2023", "Tong2011", "Tong2014"}.
      metric -- str, name of the metric to use from
      {l2, rmse, mae, correl}.
      param -- str, name of the parameter to sweep over.
      start_val -- float, value to start the sweep at.
      end_val -- float, value to end the sweep at.
      nb_points -- int, number of points for the parameter sweep
      estrus -- str, estrus stage for the Roesler2024 model, default value "".

    Returns:
    plot_data -- list(tuple), list of comparison points, parameter values,
    and the estrus stage for each sweep.

    Raises:
    ValueError -- if the start number is less than 0.
    ValueError -- if the end number is smaller than start value.
    ValueError -- if nb_steps is not an integer.
    ValueError -- if the model name is incorrect.
    ValueError -- if the provided metric is not one of
    {'l2', 'rmse', 'mae', 'correl'}.
    ValueError -- if the parameter is not valid.
    ValueError -- if the start value is smaller than the end value.
    ValueError -- if the number of simulations is negative.
    ValueError -- if the number of simulations is not an integer.
    KeyError -- if the estrus stage is incorrect.


    """
    try:
        # Check that sweep parameters are valid
        simulation.check_sweep_parameters(
            args.start_val,
            args.end_val,
            args.nb_points,
        )

        # Compute base model if pregnant model
        if args.base_model != "Roesler2024":
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

            save_file = utils.sweep_path(
                args.base_model,
                args.sweep_model,
                args.param,
                args.metric,
                stage,
            )

            if args.base_model == "Roesler2024":
                print(
                    "Computing {} simulation with default times".format(
                        args.base_model,
                    )
                )
                t, base_data = simulation.run_simulation(
                    args.base_model,
                    estrus=stage,
                )

            # Main sweep
            comp_points = simulation.run_sweep(
                args.sweep_model,
                args.param,
                values,
                args.metric,
                base_data[0, :],
                stage,
            )

            # Save data and prepare for plotting
            plot_data.append((comp_points, values, stage))
            utils.save_data(save_file, (comp_points, values, stage))

    except (ValueError, KeyError):
        raise

    return plot_data


def plot_func(args):
    """Function called by the param-sweep script to plot the parameter sweep

    The data is loaded from RES_DIR

    Args:
    args -- argparse.Namespace with following arguments:
      base_model -- str, name of the base model for comparison from
      {"Roesler2024", "Means2023", "Tong2011", "Tong2014"}.
      sweep_model -- str, name of the model to use from
      {"Roesler2024", "Means2023", "Tong2011", "Tong2014"}.
      metric -- str, name of the metric to use from
      {l2, rmse, mae, correl}.
      param -- str, name of the parameter to sweep over.
      estrus -- str, estrus stage for the Roesler2024 model, default value "".

    Returns:
    plot_data -- list(tuple), list of comparison points, parameter values,
    and the estrus stage for each sweep.

    Raises:
    FileNotFoundError -- if the results files are not found.
    ValueError -- if the model name is incorrect.
    ValueError -- if the provided metric is not one of
    {'l2', 'rmse', 'mae', 'correl'}.
    KeyError -- if the estrus stage is incorrect.


    """
    try:
        plot_data = []

        if args.estrus == "all":
            estrus = ESTRUS
        else:
            estrus = [args.estrus]

        for stage in estrus:
            # Loop over estrus cycle
            save_file = utils.sweep_path(
                args.base_model,
                args.sweep_model,
                args.param,
                args.metric,
                stage,
            )

            loaded_data = utils.load_data(save_file)
            plot_data.append(loaded_data)

    except (FileNotFoundError, ValueError, KeyError):
        raise

    return plot_data


def single_func(args):
    """Function called by the model-simulation script to run
    a single simulation

    The data is saved in RES_DIR.

    Args:
    args -- argparse.Namespace with following arguments:
      model -- str, name of the model from
      {"Roesler2024", "Means2023", "Tong2011", "Tong2014"}.
      start -- float, start time of the simulation.
      end -- float, end time of the simulation.
      steps -- int, number of timesteps in the simulation.
      estrus -- str, estrus stage for the Roesler2024 model, default value "".
      plot_only -- bool, flag used to plot an already computed model.

    Returns:
    sim_data -- np.array, simulation output.
    time -- np.array, time values of the simulation.

    Raises:
    ValueError -- if the model name is incorrect.
    ValueError -- if the start time is smaller than the end time.
    FileNotFoundError -- if the data file is not found.
    KeyError -- if the estrus stage is incorrect.


    """
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

    return sim_data, time


def multi_func(args):
    """Function called by the model-simulation script to run
    multiple simulations

    Args:
    args -- argparse.Namespace with following arguments:
      model -- str, name of the model from
      {"Roesler2024", "Means2023", "Tong2011", "Tong2014"}.
      param -- str, name of the parameter to sweep over.
      values -- list(float), list of values for the parameter.
      start -- float, start time of the simulation.
      end -- float, end time of the simulation.
      steps -- int, number of timesteps in the simulation.
      estrus -- str, estrus stage for the Roesler2024 model, default value "".

    Returns:
    sim_data -- np.array, simulations output one column per simulation.
    time -- np.array, time values of the simulation.

    Raises:
    ValueError -- if the model name is incorrect.
    ValueError -- if the start time is smaller than the end time.
    ValueError -- if the parameter is not valid.
    KeyError -- if the estrus stage is incorrect.


    """
    sim_data = np.zeros((len(args.values), args.steps))  # Pre-allocate space

    for i, value in enumerate(args.values):
        print(f"Running simulation with {args.param} at {value}")
        time, data = simulation.run_simulation(
            args.model,
            args.start,
            args.end,
            args.steps,
            args.estrus,
            args.param,
            value,
        )
        sim_data[i, :] = data[0, :]

    return sim_data, time
