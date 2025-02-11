#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_utils.py

Unit tests for the utility functions in utils.py.
Author: Mathias Roesler
Date: 11/24

This file contains test cases for the functions:
- set_params
- set_estrus_params

The tests cover various scenarios including valid inputs, invalid inputs.
"""

import pytest

import conversion.Roesler2024 as Roesler2024

from conversion.utils import set_params, set_estrus_params
from conversion.constants import E2_MAP, P4_MAP, ESTRUS_PARAMS

# Data for testing
init_states_R, constants_R = Roesler2024.init_consts()
_, _, _, legend_constants_R = Roesler2024.create_legends()

# Tests for set_params


def test_set_params_normal_case():
    updated_constants, idx = set_params(
        constants_R.copy(), legend_constants_R, "gcal", 100
    )
    assert updated_constants[idx] == 100


def test_set_params_modulators():
    # Try E2 modulator
    updated_constants, idx = set_params(
        constants_R.copy(),
        legend_constants_R,
        "E2",
        50,
    )
    assert updated_constants[idx] == 50  # E2 updated

    compare_value = 50 / constants_R[E2_MAP["E2_max"]]
    assert updated_constants[E2_MAP["mod_E2"]] == compare_value

    # Try P4 modulator
    updated_constants, idx = set_params(
        constants_R.copy(),
        legend_constants_R,
        "P4",
        50,
    )
    assert updated_constants[idx] == 50  # P4 updated

    compare_value = 50 / constants_R[P4_MAP["P4_max"]]
    assert updated_constants[P4_MAP["mod_P4"]] == compare_value


def test_set_params_not_found():
    with pytest.raises(IndexError):
        set_params(constants_R.copy(), legend_constants_R, "wrong", 100)


def test_set_params_no_value():
    updated_constants, idx = set_params(
        constants_R.copy(), legend_constants_R, "gcal", None
    )
    # Original value remains unchanged
    assert updated_constants[idx] == constants_R[idx]


# Tests for set_estrus_params


def test_set_estrus_params_normal_case():
    updated_constants = set_estrus_params(
        constants_R.copy(), legend_constants_R, "estrus"
    )
    for key, value in ESTRUS_PARAMS["estrus"].items():
        if key in legend_constants_R:
            idx = legend_constants_R.index(key)
        else:
            idx = None

        if idx is not None:
            assert updated_constants[idx] == value


def test_set_estrus_params_invalid_stage():
    with pytest.raises(KeyError):
        set_estrus_params(constants_R.copy(), legend_constants_R, "invalid_stage")
