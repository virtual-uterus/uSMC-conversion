#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
utils.py

Utilities functions for model comparison
Author: Mathias Roesler
Date: 11/24
"""

import os
import sys
import pickle
import quantities as quant

from conversion.constants import ESTRUS_PARAMS, E2_MAP, P4_MAP, RES_DIR

from scipy.signal import find_peaks
from neo.core import SpikeTrain


def set_params(constants, legend_constants, param, value):
    """Sets the new value for the specified parameter

    Args:
    constants -- list[int], list of constant values.
    legend_constants -- list[str], list of legends for constants.
    param -- str, name of the parameter to change.
    value -- float, new value for the parameter, if None the value
            is not updated.

    Returns:
    updated_constants -- list[int], list of updated constant values.
    idx -- int, index of the parameter.

    Raises:
    IndexError -- if the parameter is not in the list.

    """
    found = False
    idx = 0

    if param in E2_MAP.keys():
        # Make sure the E2 modulator is updated
        constants[E2_MAP[param]] = value
        constants[E2_MAP["mod_E2"]] = (
            constants[E2_MAP["E2"]] / constants[E2_MAP["E2_max"]]
        )
        return constants, E2_MAP[param]

    if param in P4_MAP.keys():
        # Make sure the P4 modulator is updated
        constants[P4_MAP[param]] = value
        constants[P4_MAP["mod_P4"]] = (
            constants[P4_MAP["P4"]] / constants[P4_MAP["P4_max"]]
        )
        return constants, P4_MAP[param]

    for i, legend in enumerate(legend_constants):
        words = legend.split(" ")

        if words[0] == param:
            found = True
            idx = i

            if value is not None:
                constants[i] = value

            break

    if not found:
        raise IndexError("{} was not found in parameter list".format(param))

    return constants, idx


def set_estrus_params(constants, legend_constants, estrus):
    """Sets the specific values of the constants for the estrus stage

    Args:
    constants -- list[int], list of constant values.
    legend_constants -- list[str], list of legends for constants.
    estrus -- str, estrus stage,
            {all, proestrus, estrus, metestrus, diestrus}.

    Returns:
    updated_constants -- list[int], list of updated constant values.

    Raises:
    KeyError -- if estrus is not in ESTRUS_PARAMS keys.

    """
    if estrus not in ESTRUS_PARAMS.keys():
        raise KeyError(f"the key {estrus} is not a valid estrus stage")

    for key in ESTRUS_PARAMS[estrus].keys():
        try:
            constants, _ = set_params(
                constants, legend_constants, key, ESTRUS_PARAMS[estrus][key]
            )

        except IndexError:
            sys.stderr.write(
                "Warning: {} estrus parameter not set".format(key),
            )

    return constants


def save_data(save_file, data):
    """Saves data to the save file

    Args:
    save_file -- str, path to the save file.
    data -- dict, dictionnary of data to save.

    Returns:

    Raises:
    FileNotFoundError -- if the save_file is not found.

    """
    try:
        with open(save_file, "wb") as handler:
            # Pickle data
            pickle.dump(data, handler)
    except FileNotFoundError:
        raise


def load_data(load_file):
    """Loads data to the load file

    Args:
    load_file -- str, path to the load file.

    Returns:
    loaded_data -- dict, dictionnary containing loaded data.

    Raises:
    FileNotFoundError -- if the save_file is not found.

    """
    try:
        with open(load_file, "rb") as handler:
            return pickle.load(handler)
    except FileNotFoundError:
        raise


def results_path(model_name, duration, estrus=""):
    """Gets the results path based on the model name and the simulation
    duration

    Args:
    model_name -- str, name of the model to use {"Roesler2024", "Means2023",
    "Tong2011", "Tong2014"}.
    duration -- int, duration of the simulation to load in s.
    estrus -- str, estrus stage for the Roesler2024 model, default value "".

    Returns:
    res_path -- str, path to the result file.

    Raises:

    """
    if model_name == "Roesler2024":
        return os.path.join(RES_DIR, f"{model_name}_{estrus}_{duration}s.pkl")
    else:
        return os.path.join(RES_DIR, f"{model_name}_{duration}s.pkl")


def sweep_path(
    base_model,
    sweep_model,
    param,
    metric,
    estrus="",
    base_estrus="",
):
    """Gets the sweep path based on the base model, sweep model and the metric.

    If the base model and sweep model are Roesler2024 the estrus is assume to
    the same for both.

    Args:
    base_model -- str, name of the base model to use from
    {"Roesler2024", "Means2023", "Tong2011", "Tong2014"}.
    sweep_model -- str, name of the base model to use from
    {"Roesler2024", "Means2023", "Tong2011", "Tong2014"}.
    param -- str, name of the parameter to use.
    metric -- str, name of the metric to use from {l2, rmse, mae, correl}.
    estrus -- str, estrus stage for the Roesler2024 model, default value "".
    base_estrus -- str, estrus stage for the Roesler2024 model,
    default value "".

    Returns:
    res_path -- str, path to the result file.

    Raises:

    """
    if base_model == "Roesler2024":
        b_model = f"{base_model}_{base_estrus}"
    else:
        b_model = f"{base_model}"

    if sweep_model == "Roesler2024":
        s_model = f"{sweep_model}_{estrus}"
    else:
        s_model = f"{sweep_model}"

    return os.path.join(RES_DIR, f"{b_model}_{s_model}_{param}_{metric}.pkl")


def extract_spike_times(signal, time, height=-50):
    """Extract spike times from a signal using peak detection

    Args:
    signal -- np.array, signal amplitudes over time.
    time -- np.array, corresponding time points.
    height -- float, minimum height for peaks to be considered spikes.
    distance -- int, minimum distance between peaks.

    Returns:
    spike_times -- np.array, times of detected spikes.

    Raises:

    """
    peaks, _ = find_peaks(signal, height=height)
    return time[peaks]


def create_spike_train(spike_times, t_stop):
    """Convert spike times to a SpikeTrain object

    Args:
    spike_times -- np.array, detected spike times.
    t_stop -- float, total duration of the signal.

    Returns:
    spike_train -- SpikeTrain object, spike times of train.

    Raises:

    """
    return SpikeTrain(spike_times * quant.ms, t_stop=t_stop * quant.ms)
