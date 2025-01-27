#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
constants.py

Constants for the Python code
Author: Mathias Roesler
Date: 11/24
"""

import os

HOME = os.path.expanduser("~")
BASE = "Documents/phd"
# Directory to store results
RES_DIR = os.path.join(HOME, BASE, "uSMC-conversion/res")

# Model solving constants
SOLVER = "vode"
METHOD = "bdf"
ATOL = 1e-07
RTOL = 1e-07
MAX_STEP = 0.1

# Specific values for different estrus stages
ESTRUS_PARAMS = {
    "proestrus": {
        "gkv43": 1.2,
        "stim_current": -0.40,
        "stim_interval": 49300,
        "P4": 42,
        "E2": 92,
    },
    "estrus": {
        "gkv43": 2.65,
        "stim_current": -0.28,
        "stim_interval": 46500,
        "P4": 14,
        "E2": 40,
    },
    "metestrus": {
        "gkv43": 2.2,
        "stim_current": -0.3,
        "stim_interval": 60200,
        "P4": 25,
        "E2": 49,
    },
    "diestrus": {
        "gkv43": 1.2,
        "stim_current": -0.20,
        "stim_interval": 38300,
        "P4": 10,
        "E2": 90,
    },
}

# Hard coded values of the P4 dependent constants
# Could probably be optimised
P4_MAP = {"P4": 5, "P4_max": 7, "mod_P4": 26}

# Hard coded values of the E2 dependent constants
# Could probably be optimised
E2_MAP = {"E2": 6, "E2_max": 8, "mod_E2": 25}

# Plot constants
LEFT = 0.22
BOTTOM = 0.17
RIGHT = 0.80
Y_LIMS = [-75, 15]

COLOURS = {
    "proestrus": "r",
    "estrus": "b",
    "metestrus": "g",
    "diestrus": "k",
}

PARAM = {
    "gkv43": r"g$_{Kv4.3}$",
    "gcal": r"g$_{CaL}$",
    "gna": r"g$_{Na}$",
    "stim_current": r"I$_{stim}$",
}

UNITS = {
    "gkv43": r"nS pF$^1$",
    "gcal": r"nS pF$^1$",
    "gkca": r"nS pF$^1$",
    "gna": r"nS pF$^1$",
    "stim_current": r"pA pF$^1$",
}

LABELS = {
    "l2": "L2-norm",
    "mae": "MAE",
    "rmse": "RMSE",
    "correl": "Pearson correlation",
    "vrd": "VRD",
}

ESTRUS = ["proestrus", "estrus", "metestrus", "diestrus"]
