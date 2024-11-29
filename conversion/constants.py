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
    "estrus": {"gkv43": 2.5, "stim_current": -0.41, "P4": 14, "E2": 40},
    "proestrus": {"gkv43": 0.95, "stim_current": -0.41, "P4": 37, "E2": 100},
    "metestrus": {"gkv43": 2.04, "stim_current": -0.35, "P4": 25, "E2": 49},
    "diestrus": {"gkv43": 1.155, "stim_current": -0.2, "P4": 10, "E2": 90},
}

# Hard coded values of the P4 dependent constants
# Could probably be optimised
P4_MAP = {"P4": 4, "P4_max": 6, "mod_P4": 25}

# Hard coded values of the E2 dependent constants
# Could probably be optimised
E2_MAP = {"E2": 5, "E2_max": 7, "mod_E2": 24}

# Plot constants
COLOURS = {
    "proestrus": ".r",
    "estrus": ".b",
    "metestrus": ".g",
    "diestrus": ".k",
}

PARAM = {
    "gkv43": r"g$_{Kv4.3}$",
    "gcal": r"g$_{CaL}$",
    "gkca": r"g$_{KCa}$",
    "gna": r"g$_{Na}$",
    "stim_current": r"I$_{stim}$",
}

LABELS = {
    "l2": "L2-norm",
    "mae": "MAE",
    "rmse": "RMSE",
    "correl": "Pearson correlation",
}

ESTRUS = ["estrus", "proestrus", "metestrus", "diestrus"]
