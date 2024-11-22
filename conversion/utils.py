#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
utils.py

Utilities functions for model comparison
Author: Mathias Roesler
Date: 11/24
"""

import sys
from .constants import ESTRUS_PARAMS, E2_MAP, P4_MAP


def setParams(constants, legend_constants, param, value):
    """Sets the new value for the specified parameter

    Raises an IndexError if the parameter was not found in the list.

    Arguments:
    constants -- list[int], list of constant values.
    legend_constants -- list[str], list of legends for constants.
    param -- str, name of the parameter to change.
    value -- float, new value for the parameter, if None the value
            is not updated.

    Return:
    updated_constants -- list[int], list of updated constant values.
    idx -- int, index of the parameter.

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
        sys.stderr.write(
            "Warning: {} was not found in parameter list\n".format(param),
        )
        raise IndexError

    return constants, idx


def setEstrusParams(constants, legend_constants, estrus):
    """Sets the specific values of the constants for the estrus stage

    Arguments:
    constants -- list[int], list of constant values.
    legend_constants -- list[str], list of legends for constants.
    estrus -- str, estrus stage,
            {all, proestrus, estrus, metestrus, diestrus}.

    Return:
    updated_constants -- list[int], list of updated constant values.

    """
    try:
        assert estrus in ESTRUS_PARAMS.keys()

    except AssertionError:
        sys.stderr.write("Error: the key {} is not valid\n".format(estrus))
        exit(1)

    for key in ESTRUS_PARAMS[estrus].keys():
        try:
            constants, _ = setParams(
                constants, legend_constants, key, ESTRUS_PARAMS[estrus][key]
            )

        except IndexError:
            sys.stderr.write(
                "Warning: {} estrus parameter not set\n".format(key),
            )

    return constants
