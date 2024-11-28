#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simulation.py

Functions for performing simulations
Author: Mathias Roesler
Date: 11/24
"""

from conversion import Tong2011, Tong2014, Means2023, Roesler2024, utils


def run_simulation(model, start=0, end=15000, nb_steps=100000, estrus=""):
    """Runs a simulation for the given model

    Arguments:
    model -- str, name of the model to use {"Roesler2024", "Means2023",
    "Tong2011", "Tong2014"}.
    start -- float, start time in ms for the simulation, default value 0.
    end -- float, end time in ms for the simulation, default value 15000.
    nb_steps -- int, number of steps in the simulation, default value 100000.
    estrus -- str, estrus stage for the Roesler2024 model, default value "".

    Return:
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
        raise ValueError("start value must be greater than 0\n")
    if end < start:
        raise ValueError("end value must be greater than start value\n")
    if not isinstance(nb_steps, int):
        raise ValueError("step number must be an integer\n")

    match model:
        case "Tong2011":
            init_states, constants = Tong2011.init_consts()
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
                constants = utils.set_estrus_params(
                    constants, legend_constants, estrus)
            except KeyError:
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
            raise ValueError(f"{model} incorrect model name\n")

    return voi, states
