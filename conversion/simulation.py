#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simulation.py

Functions for performing simulations
Author: Mathias Roesler
Date: 11/24
"""

import os

from conversion import Tong2011, Tong2014, Means2023, Roesler2024, utils
import numpy as np

from conversion import Tong2011, Tong2014, Means2023, Roesler2024
from conversion import utils, metrics

from conversion.constants import RES_DIR, ESTRUS


def run_simulation(
    model, start=0, end=15000, nb_steps=100000, estrus="", param="", value=None
):
    """Runs a simulation for the given model

    If a parameter and its value are provided the parameter is updated.

    Args:
    model -- str, name of the model to use {"Roesler2024", "Means2023",
    "Tong2011", "Tong2014"}.
    start -- float, start time in ms for the simulation, default value 0.
    end -- float, end time in ms for the simulation, default value 15000.
    nb_steps -- int, number of steps in the simulation, default value 100000.
    estrus -- str, estrus stage for the Roesler2024 model, default value "".
    param -- str, name of the parameter to update if running a parameter sweep.
    value -- int, value of the parameter to update if running a
    parameter sweep.

    Returns:
    voi -- np.array, timesteps in ms.
    states -- np.array, simulation data.

    Raises:
    ValueError -- if the start number is less than 0.
    ValueError -- if the end number is smaller than start value.
    ValueError -- if nb_steps is not an integer.
    ValueError -- if the model name is incorrect.
    KeyError -- if the estrus stage is incorrect.

    """
    if start < 0:
        raise ValueError("start value must be greater than 0")
    if end < start:
        raise ValueError("end value must be greater than start value")
    if not isinstance(nb_steps, int):
        raise ValueError("step number must be an integer")

    match model:
        case "Tong2011":
            init_states, constants = Tong2011.init_consts()
            if param != "":
                try:
                    # If running a sweep update the constants
                    _, _, _, legend_constants = Tong2011.create_legends()
                    constants, _ = utils.set_params(
                        constants,
                        legend_constants,
                        param,
                        value,
                    )
                except IndexError:
                    raise
            (
                voi,
                states,
                _,
            ) = Tong2011.solve_model(
                init_states,
                constants,
                start,
                end,
                nb_steps,
            )
        case "Tong2014":
            init_states, constants = Tong2014.init_consts()
            if param != "":
                try:
                    # If running a sweep update the constants
                    _, _, _, legend_constants = Tong2014.create_legends()
                    constants, _ = utils.set_params(
                        constants,
                        legend_constants,
                        param,
                        value,
                    )
                except IndexError:
                    raise
            (
                voi,
                states,
                _,
            ) = Tong2014.solve_model(
                init_states,
                constants,
                start,
                end,
                nb_steps,
            )
        case "Means2023":
            init_states, constants = Means2023.init_consts()
            if param != "":
                try:
                    # If running a sweep update the constants
                    _, _, _, legend_constants = Means2023.create_legends()
                    constants, _ = utils.set_params(
                        constants,
                        legend_constants,
                        param,
                        value,
                    )
                except IndexError:
                    raise
            (
                voi,
                states,
                _,
            ) = Means2023.solve_model(
                init_states,
                constants,
                start,
                end,
                nb_steps,
            )
        case "Roesler2024":
            init_states, constants = Roesler2024.init_consts()
            _, _, _, legend_constants = Roesler2024.create_legends()
            try:
                # Set estrus specific parameters
                constants = utils.set_estrus_params(
                    constants,
                    legend_constants,
                    estrus,
                )
                if param != "":
                    # If running a sweep update the constants
                    _, _, _, legend_constants = Roesler2024.create_legends()
                    constants, _ = utils.set_params(
                        constants,
                        legend_constants,
                        param,
                        value,
                    )

            except (IndexError, KeyError):
                raise
            (
                voi,
                states,
                _,
            ) = Roesler2024.solve_model(
                init_states,
                constants,
                start,
                end,
                nb_steps,
            )
        case _:
            raise ValueError(f"{model} incorrect model name")

    return voi, states


def run_sweep(sweep_model, param, values, metric, base_sim, estrus=""):
    """Runs a parameter sweep and compares the results to a base simulation

    Args:
    sweep_model -- str, name of the model to use {"Roesler2024", "Means2023",
    "Tong2011", "Tong2014"}.
    param -- str, name of the parameter to sweep over.
    values -- np.array, array of values to sweep over.
    metric -- str, name of the metric to use from {l2, rmse, mae, correl}.
    base_sim -- np.array, base simulation to compare to.
    estrus -- str, estrus stage for the Roesler2024 model, default value "".

    Returns:
    comp_points -- np.array, array of comparison points between base simulation
    and sweep using input metric.

    Raises:
    ValueError -- if the start number is less than 0.
    ValueError -- if the end number is smaller than start value.
    ValueError -- if nb_steps is not an integer.
    ValueError -- if the model name is incorrect.
    KeyError -- if the estrus stage is incorrect.
    ValueError -- if the provided metric is not one of
    {'l2', 'rmse', 'mae', 'correl'}.

    """
    comp_points = np.zeros(len(values))

    try:
        for i, value in enumerate(values):
            print(f"  Computing simulation {i+1}")
            _, sweep_data = run_simulation(
                sweep_model,
                estrus=estrus,
                param=param,
                value=value,
            )
            comp_points[i] = metrics.compute_comparison(
                base_sim,
                sweep_data[0, :],
                metric,
            )
    except (ValueError, KeyError):
        raise

    return comp_points

def save_simulation(model_name, sim_data, t, estrus=""):
    """Saves the results of a simulation as {model_name}_{duration}s.pkl with
    duration the last timestep in t. If the model is Roesler2024 then the save
    name includes the estrus stage between model_name and duration.

    The data and time are stored in a dictionnary with respective keys being
    data and time.

    Args:
    model_name -- str, name of the model to use {"Roesler2024", "Means2023",
    "Tong2011", "Tong2014"}.
    sim_data -- np.array, simulation data to save.
    t -- np.array, simulation timestamps in ms.
    estrus -- str, estrus stage for the Roesler2024 model, default value "".

    Returns:

    Raises:

    """
    duration = int(t[len(t) - 1] * 1e-3)  # Duration converted in seconds

    if model_name == "Roesler2024":
        res_file = os.path.join(
            RES_DIR,
            f"{model_name}_{estrus}_{duration}s.pkl",
        )
    else:
        res_file = os.path.join(RES_DIR, f"{model_name}_{duration}s.pkl")

    save_dict = {"data": sim_data, "time": t}

    utils.save_data(res_file, save_dict)


def check_sweep_parameters(start_val, end_val, nb_points):
    """Checks that the sweep parameters are valid.

    Args:
    start_val -- float, value to start the sweep at.
    end_val -- float, value to end the sweep at.
    nb_points -- int, number of simulation to run.

    Returns:

    Raises:
    ValueError -- if the start value is smaller than the end value.
    ValueError -- if the number of simulations is negative.
    ValueError -- if the number of simulations is not an integer.

    """
    if end_val < start_val:
        raise ValueError("the end value is smaller than the start value")
    if nb_points < 0:
        raise ValueError("the number of simulations must be positive")
    if not isinstance(nb_points, int):
        raise ValueError("the number of simulations must be an integer")
