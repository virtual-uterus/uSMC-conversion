#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tong2011.py

Tong2011 cell model Python version
Author: Mathias Roesler
Date: 11/24
"""

import numpy as np

from scipy.integrate import ode
from conversion.constants import SOLVER, METHOD, ATOL, RTOL, MAX_STEP

# Size of variable np.arrays:
sizeAlgebraic = 82
sizeStates = 22
sizeConstants = 83


def create_legends():
    """Creates the lists of legends

    Args:

    Returns:
    legend_states -- list[str], list of legends for states.
    legend_algebraic -- list[str], list of legends for algebraic.
    legend_voi -- list[str], list of legends for voi.
    legend_constants -- list[str], list of legends for constants.

    """
    legend_states = [""] * sizeStates
    legend_rates = [""] * sizeStates
    legend_algebraic = [""] * sizeAlgebraic
    legend_voi = ""
    legend_constants = [""] * sizeConstants
    legend_algebraic[0] = "Ist in component interface (pA_per_pF)"
    legend_voi = "time in component environment (msec)"
    legend_constants[0] = "stim_start in component interface (msec)"
    legend_constants[1] = "stim_period in component interface (msec)"
    legend_constants[2] = "stim_duration in component interface (msec)"
    legend_constants[3] = "stim_current in component interface (pA_per_pF)"
    legend_algebraic[79] = "I_tot in component membrane_potential (pA_per_pF)"
    legend_algebraic[61] = "I_Ca_tot in component membrane_potential (pA_per_pF)"
    legend_states[0] = "v in component membrane_potential (mV)"
    legend_constants[67] = "Cm in component parameters (uF_per_cm2)"
    legend_algebraic[42] = "ina in component I_Na (pA_per_pF)"
    legend_algebraic[49] = "ical in component I_CaL (pA_per_pF)"
    legend_algebraic[51] = "icat in component I_CaT (pA_per_pF)"
    legend_algebraic[52] = "ib in component I_b (pA_per_pF)"
    legend_algebraic[53] = "ik1 in component I_K1 (pA_per_pF)"
    legend_algebraic[54] = "ik2 in component I_K2 (pA_per_pF)"
    legend_algebraic[55] = "ika in component I_Ka (pA_per_pF)"
    legend_algebraic[56] = "iBKa in component I_BKa (pA_per_pF)"
    legend_algebraic[57] = "iBKab in component I_BKab (pA_per_pF)"
    legend_algebraic[58] = "ih in component I_h (pA_per_pF)"
    legend_algebraic[59] = "icl in component I_Cl (pA_per_pF)"
    legend_algebraic[63] = "insna in component I_ns (pA_per_pF)"
    legend_algebraic[60] = "insca in component I_ns (pA_per_pF)"
    legend_algebraic[65] = "insk in component I_ns (pA_per_pF)"
    legend_algebraic[67] = "inak in component I_NaK (pA_per_pF)"
    legend_algebraic[76] = "inaca in component I_NaCa (pA_per_pF)"
    legend_algebraic[80] = "J_tot in component Ca_Concentrations (mM_per_msec)"
    legend_algebraic[62] = "J_Ca_mem in component Ca_Concentrations (mM_per_msec)"
    legend_states[1] = "cai in component Ca_Concentrations (mM)"
    legend_algebraic[75] = "jnaca in component J_NaCa (mM_per_msec)"
    legend_algebraic[77] = "jpmca in component J_PMCA (mM_per_msec)"
    legend_constants[62] = "buff in component parameters (dimensionless)"
    legend_constants[63] = "AV in component parameters (cm2_per_uL)"
    legend_constants[64] = "zca in component parameters (dimensionless)"
    legend_constants[66] = "frdy in component parameters (coulomb_per_mole)"
    legend_algebraic[64] = "jcamem_plot in component Ca_Concentrations (M_per_msec)"
    legend_algebraic[81] = "jpmca_plot in component Ca_Concentrations (M_per_msec)"
    legend_algebraic[78] = "jnaca_plot in component Ca_Concentrations (M_per_msec)"
    legend_constants[4] = "conversion in component Ca_Concentrations (mM_to_M)"
    legend_constants[11] = "ki in component parameters (mM)"
    legend_constants[53] = "nai in component parameters (mM)"
    legend_constants[56] = "cli in component parameters (mM)"
    legend_constants[57] = "ko in component parameters (mM)"
    legend_constants[12] = "cao in component parameters (mM)"
    legend_constants[58] = "nao in component parameters (mM)"
    legend_constants[60] = "clo in component parameters (mM)"
    legend_constants[13] = "mgo in component parameters (mM)"
    legend_constants[14] = "zna in component parameters (dimensionless)"
    legend_constants[15] = "zk in component parameters (dimensionless)"
    legend_constants[65] = "R in component parameters (joule_per_kelvin_per_kilomole)"
    legend_constants[68] = "temp in component parameters (kelvin)"
    legend_constants[16] = "gna in component parameters (nS_per_pF)"
    legend_constants[17] = "gcal in component parameters (nS_per_pF)"
    legend_constants[18] = "ecal in component parameters (mV)"
    legend_constants[19] = "kmca in component parameters (mM)"
    legend_constants[20] = "gcat in component parameters (nS_per_pF)"
    legend_constants[21] = "ecat in component parameters (mV)"
    legend_constants[22] = "gkca in component parameters (nS_per_pF)"
    legend_constants[23] = "gb in component parameters (nS_per_pF)"
    legend_constants[24] = "gk1 in component parameters (nS_per_pF)"
    legend_constants[25] = "gk2 in component parameters (nS_per_pF)"
    legend_constants[26] = "gbka in component parameters (dimensionless)"
    legend_constants[27] = "gbkab in component parameters (dimensionless)"
    legend_constants[28] = "gka in component parameters (nS_per_pF)"
    legend_constants[29] = "gcl in component parameters (nS_per_pF)"
    legend_constants[30] = "gh in component parameters (nS_per_pF)"
    legend_constants[31] = "gns in component parameters (nS_per_pF)"
    legend_constants[32] = "PnsK in component parameters (dimensionless)"
    legend_constants[33] = "PnsNa in component parameters (dimensionless)"
    legend_constants[34] = "PnsCa in component parameters (dimensionless)"
    legend_constants[35] = "PnsCs in component parameters (dimensionless)"
    legend_constants[36] = "gnsCa in component parameters (dimensionless)"
    legend_constants[37] = "gnsNa in component parameters (dimensionless)"
    legend_constants[38] = "gnsK in component parameters (dimensionless)"
    legend_constants[39] = "gnsCs in component parameters (dimensionless)"
    legend_constants[69] = "ginak in component parameters (pA_per_pF)"
    legend_constants[74] = "nakKmko in component parameters (mM)"
    legend_constants[76] = "nakKmnai in component parameters (mM)"
    legend_constants[70] = "PK in component parameters (dimensionless)"
    legend_constants[75] = "PNa in component parameters (dimensionless)"
    legend_constants[40] = "Jpmca in component parameters (mM_per_msec)"
    legend_constants[41] = "Kmpmca in component parameters (mM)"
    legend_constants[42] = "npmca in component parameters (dimensionless)"
    legend_constants[78] = "Jnaca in component parameters (mM_per_msec)"
    legend_constants[43] = "Kmallo in component parameters (mM)"
    legend_constants[44] = "nallo in component parameters (dimensionless)"
    legend_constants[79] = "ksat in component parameters (dimensionless)"
    legend_constants[80] = "xgamma in component parameters (dimensionless)"
    legend_constants[45] = "Kmnai in component parameters (mM)"
    legend_constants[46] = "Kmcai in component parameters (mM)"
    legend_constants[47] = "Kmnao in component parameters (mM)"
    legend_constants[48] = "Kmcao in component parameters (mM)"
    legend_constants[49] = "Fmax in component parameters (uN)"
    legend_constants[50] = "FKm in component parameters (nM)"
    legend_constants[51] = "Fn in component parameters (dimensionless)"
    legend_algebraic[18] = "vFRT in component parameters (dimensionless)"
    legend_constants[71] = "ena in component parameters (mV)"
    legend_constants[72] = "ek in component parameters (mV)"
    legend_constants[77] = "eh in component parameters (mV)"
    legend_constants[73] = "ecl in component parameters (mV)"
    legend_algebraic[37] = "enscc in component parameters (mV)"
    legend_algebraic[1] = "wss in component Ca_dependent_Force (dimensionless)"
    legend_algebraic[19] = "wtc in component Ca_dependent_Force (msec)"
    legend_constants[5] = "conversion in component Ca_dependent_Force (nM_to_mM)"
    legend_algebraic[2] = "Force in component Ca_dependent_Force (uN)"
    legend_states[2] = "w in component Ca_dependent_Force (dimensionless)"
    legend_algebraic[3] = "mss in component I_Na (dimensionless)"
    legend_algebraic[4] = "hss in component I_Na (dimensionless)"
    legend_algebraic[20] = "mtc in component I_Na (msec)"
    legend_algebraic[21] = "htc in component I_Na (msec)"
    legend_states[3] = "m in component I_Na (dimensionless)"
    legend_states[4] = "h in component I_Na (dimensionless)"
    legend_algebraic[5] = "dss in component I_CaL (dimensionless)"
    legend_algebraic[6] = "fss in component I_CaL (dimensionless)"
    legend_algebraic[47] = "fca in component I_CaL (dimensionless)"
    legend_algebraic[22] = "dtc in component I_CaL (msec)"
    legend_constants[52] = "f1tc in component I_CaL (msec)"
    legend_algebraic[23] = "f2tc in component I_CaL (msec)"
    legend_states[5] = "d in component I_CaL (dimensionless)"
    legend_states[6] = "f1 in component I_CaL (dimensionless)"
    legend_states[7] = "f2 in component I_CaL (dimensionless)"
    legend_algebraic[7] = "bss in component I_CaT (dimensionless)"
    legend_algebraic[8] = "gss in component I_CaT (dimensionless)"
    legend_algebraic[24] = "btc in component I_CaT (msec)"
    legend_algebraic[25] = "gtc in component I_CaT (msec)"
    legend_states[8] = "b in component I_CaT (dimensionless)"
    legend_states[9] = "g in component I_CaT (dimensionless)"
    legend_algebraic[9] = "qss in component I_K1 (dimensionless)"
    legend_algebraic[10] = "rss in component I_K1 (dimensionless)"
    legend_algebraic[26] = "qtc in component I_K1 (msec)"
    legend_algebraic[27] = "r1tc in component I_K1 (msec)"
    legend_algebraic[28] = "r2tc in component I_K1 (msec)"
    legend_states[10] = "q in component I_K1 (dimensionless)"
    legend_states[11] = "r1 in component I_K1 (dimensionless)"
    legend_states[12] = "r2 in component I_K1 (dimensionless)"
    legend_algebraic[11] = "pss in component I_K2 (dimensionless)"
    legend_algebraic[12] = "kss in component I_K2 (dimensionless)"
    legend_algebraic[29] = "ptc in component I_K2 (msec)"
    legend_algebraic[30] = "k1tc in component I_K2 (msec)"
    legend_algebraic[31] = "k2tc in component I_K2 (msec)"
    legend_states[13] = "p in component I_K2 (dimensionless)"
    legend_states[14] = "k1 in component I_K2 (dimensionless)"
    legend_states[15] = "k2 in component I_K2 (dimensionless)"
    legend_algebraic[13] = "sss in component I_Ka (dimensionless)"
    legend_algebraic[14] = "xss in component I_Ka (dimensionless)"
    legend_algebraic[32] = "stc in component I_Ka (msec)"
    legend_algebraic[33] = "xtc in component I_Ka (msec)"
    legend_states[16] = "s in component I_Ka (dimensionless)"
    legend_states[17] = "x in component I_Ka (dimensionless)"
    legend_algebraic[15] = "xass_z in component I_BKa (dimensionless)"
    legend_algebraic[34] = "xass_vh in component I_BKa (mV)"
    legend_constants[6] = "conversion in component I_BKa (mM_to_M)"
    legend_algebraic[38] = "xass in component I_BKa (dimensionless)"
    legend_algebraic[43] = "xatc in component I_BKa (msec)"
    legend_states[18] = "xa in component I_BKa (dimensionless)"
    legend_algebraic[16] = "xabss_z in component I_BKab (dimensionless)"
    legend_algebraic[35] = "xabss_vh in component I_BKab (mV)"
    legend_constants[7] = "conversion in component I_BKab (mM_to_M)"
    legend_algebraic[39] = "xabss in component I_BKab (dimensionless)"
    legend_algebraic[44] = "xabtc in component I_BKab (msec)"
    legend_states[19] = "xab in component I_BKab (dimensionless)"
    legend_algebraic[17] = "yss in component I_h (dimensionless)"
    legend_algebraic[45] = "ytc in component I_h (msec)"
    legend_algebraic[36] = "ya in component I_h (per_msec)"
    legend_algebraic[40] = "yb in component I_h (per_msec)"
    legend_states[20] = "y in component I_h (dimensionless)"
    legend_algebraic[48] = "css in component I_Cl (dimensionless)"
    legend_algebraic[50] = "ctc in component I_Cl (msec)"
    legend_algebraic[41] = "K1cl in component I_Cl (mM)"
    legend_algebraic[46] = "K2cl in component I_Cl (dimensionless)"
    legend_states[21] = "c in component I_Cl (dimensionless)"
    legend_constants[54] = "fmg in component I_ns (dimensionless)"
    legend_constants[61] = "gs_nao in component I_ns (dimensionless)"
    legend_constants[55] = "gs_cao in component I_ns (dimensionless)"
    legend_constants[59] = "gs_ko in component I_ns (dimensionless)"
    legend_constants[8] = "tinyamount in component I_ns (mM)"
    legend_algebraic[66] = "fnak in component I_NaK (dimensionless)"
    legend_constants[81] = "knak in component I_NaK (dimensionless)"
    legend_constants[82] = "nnak in component I_NaK (dimensionless)"
    legend_constants[9] = "inaca_sign in component I_NaCa (dimensionless)"
    legend_algebraic[68] = "f1naca in component J_NaCa (dimensionless)"
    legend_algebraic[69] = "f2naca in component J_NaCa (dimensionless)"
    legend_algebraic[70] = "fallo in component J_NaCa (dimensionless)"
    legend_algebraic[71] = "naca_Eup in component J_NaCa (mM4)"
    legend_algebraic[72] = "naca_Ed1 in component J_NaCa (dimensionless)"
    legend_algebraic[73] = "naca_Ed2 in component J_NaCa (mM4)"
    legend_algebraic[74] = "naca_Ed3 in component J_NaCa (mM4)"
    legend_constants[10] = "jnaca_sign in component J_NaCa (dimensionless)"
    legend_rates[0] = "d/dt v in component membrane_potential (mV)"
    legend_rates[1] = "d/dt cai in component Ca_Concentrations (mM)"
    legend_rates[2] = "d/dt w in component Ca_dependent_Force (dimensionless)"
    legend_rates[3] = "d/dt m in component I_Na (dimensionless)"
    legend_rates[4] = "d/dt h in component I_Na (dimensionless)"
    legend_rates[5] = "d/dt d in component I_CaL (dimensionless)"
    legend_rates[6] = "d/dt f1 in component I_CaL (dimensionless)"
    legend_rates[7] = "d/dt f2 in component I_CaL (dimensionless)"
    legend_rates[8] = "d/dt b in component I_CaT (dimensionless)"
    legend_rates[9] = "d/dt g in component I_CaT (dimensionless)"
    legend_rates[10] = "d/dt q in component I_K1 (dimensionless)"
    legend_rates[11] = "d/dt r1 in component I_K1 (dimensionless)"
    legend_rates[12] = "d/dt r2 in component I_K1 (dimensionless)"
    legend_rates[13] = "d/dt p in component I_K2 (dimensionless)"
    legend_rates[14] = "d/dt k1 in component I_K2 (dimensionless)"
    legend_rates[15] = "d/dt k2 in component I_K2 (dimensionless)"
    legend_rates[16] = "d/dt s in component I_Ka (dimensionless)"
    legend_rates[17] = "d/dt x in component I_Ka (dimensionless)"
    legend_rates[18] = "d/dt xa in component I_BKa (dimensionless)"
    legend_rates[19] = "d/dt xab in component I_BKab (dimensionless)"
    legend_rates[20] = "d/dt y in component I_h (dimensionless)"
    legend_rates[21] = "d/dt c in component I_Cl (dimensionless)"
    return (legend_states, legend_algebraic, legend_voi, legend_constants)


def init_consts():
    """Initialises the constants

    Args:

    Returns:
    states -- list[float], list of states.
    constants -- list[int], list of constants.

    """
    constants = [0.0] * sizeConstants
    states = [0.0] * sizeStates
    constants[0] = 1000
    constants[1] = 58000
    constants[2] = 10000
    constants[3] = -0.25
    states[0] = -53.90915441282156
    states[1] = 0.0001161881607214449
    constants[4] = 1000
    constants[5] = 1e-6
    states[2] = 0.2345238135343783
    states[3] = 0.1253518889572223
    states[4] = 0.404599170710196
    states[5] = 0.01036961357784695
    states[6] = 0.9065941499695301
    states[7] = 0.9065967263076083
    states[8] = 0.508117603077852
    states[9] = 0.03582573962705717
    states[10] = 0.2060363247740295
    states[11] = 0.1922244113609531
    states[12] = 0.1932803618375963
    states[13] = 0.1174074734567931
    states[14] = 0.9968385770271651
    states[15] = 0.9968408069904307
    states[16] = 0.0307583106982354
    states[17] = 0.08785242843398365
    constants[6] = 1000.0
    states[18] = 0.0003569126518797985
    constants[7] = 1000.0
    states[19] = 0.002220456569762898
    states[20] = 0.002604864867063448
    states[21] = 0.0003764413740731269
    constants[8] = 1e-8
    constants[9] = -1
    constants[10] = -1
    constants[11] = 140.000
    constants[12] = 2.50000
    constants[13] = 0.500000
    constants[14] = 1.00000
    constants[15] = 1.00000
    constants[16] = 0.00000
    constants[17] = 0.600000
    constants[18] = 45.0000
    constants[19] = 0.00100000
    constants[20] = 0.0580000
    constants[21] = 42.0000
    constants[22] = 0.800000
    constants[23] = 0.00400000
    constants[24] = 0.520000
    constants[25] = 0.0320000
    constants[26] = 0.200000
    constants[27] = 0.100000
    constants[28] = 0.160000
    constants[29] = 0.187500
    constants[30] = 0.0542000
    constants[31] = 0.0123000
    constants[32] = 1.30000
    constants[33] = 0.900000
    constants[34] = 0.890000
    constants[35] = 1.00000
    constants[36] = 0.500000
    constants[37] = 1.00000
    constants[38] = 1.19000
    constants[39] = 1.60000
    constants[40] = 3.50000e-07
    constants[41] = 0.000500000
    constants[42] = 2.00000
    constants[43] = 0.000300000
    constants[44] = 4.00000
    constants[45] = 30.0000
    constants[46] = 0.00700000
    constants[47] = 87.5000
    constants[48] = 1.30000
    constants[49] = 3.00000
    constants[50] = 161.301
    constants[51] = 3.60205
    constants[52] = 12.0000
    constants[53] = 4.00000
    constants[54] = 0.108043 + 0.903902 / (
        1.00000 + np.power(constants[13] / 0.281007, 1.29834)
    )
    constants[55] = ((1.00000 / 0.000525000) * 0.0300000) / (
        1.00000 + np.power(150.000 / (constants[12] + constants[8]), 2.00000)
    )
    constants[56] = 46.0000
    constants[57] = 6.00000
    constants[58] = 130.000
    constants[59] = ((1.00000 / 0.0123000) * 0.0300000) / (
        1.00000 + np.power(150.000 / (constants[57] + constants[8]), 2.00000)
    )
    constants[60] = 130.000
    constants[61] = ((1.00000 / 0.0123000) * 0.0300000) / (
        1.00000 + np.power(150.000 / (constants[58] + constants[8]), 2.00000)
    )
    constants[62] = 0.0150000
    constants[63] = 4.00000
    constants[64] = 2.00000
    constants[65] = 8314.00
    constants[66] = 96485.0
    constants[67] = 1.00000
    constants[68] = 308.000
    constants[69] = 1.70000
    constants[70] = 1.00000
    constants[71] = ((constants[65] * constants[68]) / constants[66]) * np.log(
        constants[58] / constants[53]
    )
    constants[72] = ((constants[65] * constants[68]) / constants[66]) * np.log(
        constants[57] / constants[11]
    )
    constants[73] = ((constants[65] * constants[68]) / constants[66]) * np.log(
        constants[56] / constants[60]
    )
    constants[74] = 2.00000
    constants[75] = 0.350000
    constants[76] = 22.0000
    constants[77] = ((constants[65] * constants[68]) / constants[66]) * np.log(
        (constants[57] + (constants[75] / constants[70]) * constants[58])
        / (constants[11] + (constants[75] / constants[70]) * constants[53])
    )
    constants[78] = 3.50000e-06
    constants[79] = 0.270000
    constants[80] = 0.350000
    constants[81] = 1.00000 / (
        1.00000 + np.power(constants[74] / constants[57], 1.50000)
    )
    constants[82] = 1.00000 / (
        1.00000 + np.power(constants[76] / constants[53], 2.00000)
    )
    return (states, constants)


def compute_rates(voi, states, constants):
    """Computes rates of the system

    Args:
    voi -- list[flaot], list of voi.
    states -- list[float], list of states.
    constants -- list[int], list of constant values.

    Returns:
    rates -- list[float], list of computed rates.

    """
    rates = [0.0] * sizeStates
    algebraic = [0.0] * sizeAlgebraic
    algebraic[6] = 1.00000 / (1.00000 + np.exp((states[0] + 38.0000) / 7.00000))
    rates[6] = (algebraic[6] - states[6]) / constants[52]
    algebraic[1] = 1.00000 / (
        1.00000 + np.power((constants[50] * constants[5]) / states[1], constants[51])
    )
    algebraic[19] = 4000.00 * (
        0.234845
        + (1.00000 - 0.234845)
        / (
            1.00000
            + np.power(states[1] / (constants[50] * constants[5]), constants[51])
        )
    )
    rates[2] = (algebraic[1] - states[2]) / algebraic[19]
    algebraic[3] = 1.00000 / (1.00000 + np.exp(-(states[0] + 35.9584) / 9.24013))
    algebraic[20] = 0.250000 + 7.00000 / (
        1.00000 + np.exp((states[0] + 38.0000) / 10.0000)
    )
    rates[3] = (algebraic[3] - states[3]) / algebraic[20]
    algebraic[4] = 1.00000 / (1.00000 + np.exp((states[0] + 57.0000) / 8.00000))
    algebraic[21] = 0.900000 + 1002.85 / (
        1.00000 + np.power((states[0] + 47.5000) / 1.50000, 2.00000)
    )
    rates[4] = (algebraic[4] - states[4]) / algebraic[21]
    algebraic[5] = 1.00000 / (1.00000 + np.exp(-(states[0] + 22.0000) / 7.00000))
    algebraic[22] = 2.29000 + 5.70000 / (
        1.00000 + np.power((states[0] + 29.9700) / 9.00000, 2.00000)
    )
    rates[5] = (algebraic[5] - states[5]) / algebraic[22]
    algebraic[23] = 90.9699 * (
        1.00000
        - 1.00000
        / (
            (1.00000 + np.exp((states[0] + 13.9629) / 45.3782))
            * (1.00000 + np.exp(-(states[0] + 9.49866) / 3.39450))
        )
    )
    rates[7] = (algebraic[6] - states[7]) / algebraic[23]
    algebraic[7] = 1.00000 / (1.00000 + np.exp(-(states[0] + 54.2300) / 9.88000))
    algebraic[24] = 0.450000 + 3.90000 / (
        1.00000 + np.power((states[0] + 66.0000) / 26.0000, 2.00000)
    )
    rates[8] = (algebraic[7] - states[8]) / algebraic[24]
    algebraic[8] = 0.0200000 + 0.980000 / (
        1.00000 + np.exp((states[0] + 72.9780) / 4.64000)
    )
    algebraic[25] = 150.000 * (
        1.00000
        - 1.00000
        / (
            (1.00000 + np.exp((states[0] - 417.430) / 203.180))
            * (1.00000 + np.exp(-(states[0] + 61.1100) / 8.07000))
        )
    )
    rates[9] = (algebraic[8] - states[9]) / algebraic[25]
    algebraic[9] = 0.978613 / (1.00000 + np.exp(-(states[0] + 18.6736) / 26.6606))
    algebraic[26] = 500.000 / (
        1.00000 + np.power((states[0] + 60.7100) / 15.7900, 2.00000)
    )
    rates[10] = (algebraic[9] - states[10]) / algebraic[26]
    algebraic[10] = 1.00000 / (1.00000 + np.exp((states[0] + 63.0000) / 6.30000))
    algebraic[27] = 5000.00 / (
        1.00000 + np.power((states[0] + 62.7133) / 35.8611, 2.00000)
    )
    rates[11] = (algebraic[10] - states[11]) / algebraic[27]
    algebraic[28] = 30000.0 + 220000.0 / (
        1.00000 + np.exp((states[0] + 22.0000) / 4.00000)
    )
    rates[12] = (algebraic[10] - states[12]) / algebraic[28]
    algebraic[11] = 0.948000 / (1.00000 + np.exp(-(states[0] + 17.9100) / 18.4000))
    algebraic[29] = 100.000 / (
        1.00000 + np.power((states[0] + 64.1000) / 28.6700, 2.00000)
    )
    rates[13] = (algebraic[11] - states[13]) / algebraic[29]
    algebraic[12] = 1.00000 / (1.00000 + np.exp((states[0] + 21.2000) / 5.70000))
    algebraic[30] = 1.00000e06 * (
        1.00000
        - 1.00000
        / (
            (1.00000 + np.exp((states[0] - 315.000) / 50.0000))
            * (1.00000 + np.exp(-(states[0] + 74.9000) / 8.00000))
        )
    )
    rates[14] = (algebraic[12] - states[14]) / algebraic[30]
    algebraic[31] = 2.50000e06 * (
        1.00000
        - 1.00000
        / (
            (1.00000 + np.exp((states[0] - 132.868) / 25.3992))
            * (1.00000 + np.exp(-(states[0] + 24.9203) / 2.67915))
        )
    )
    rates[15] = (algebraic[12] - states[15]) / algebraic[31]
    algebraic[13] = 1.00000 / (1.00000 + np.exp(-(states[0] + 27.7900) / 7.57000))
    algebraic[32] = 17.0000 / (
        1.00000 + np.power((states[0] + 20.5232) / 35.0000, 2.00000)
    )
    rates[16] = (algebraic[13] - states[16]) / algebraic[32]
    algebraic[14] = 0.0200000 + 0.980000 / (
        1.00000 + np.exp((states[0] + 69.5000) / 6.00000)
    )
    algebraic[33] = 7.50000 + 10.0000 / (
        1.00000 + np.power((states[0] + 34.1765) / 120.000, 2.00000)
    )
    rates[17] = (algebraic[14] - states[17]) / algebraic[33]
    algebraic[15] = -0.749234 / (
        1.00000 + np.power((states[1] * constants[6] - 0.0630535) / 0.161942, 2.00000)
    ) + 8.38384 / (
        1.00000 + np.power((states[1] * constants[6] + 1538.29) / 739.057, 2.00000)
    )
    algebraic[34] = (
        5011.47
        / (
            1.00000
            + np.power((states[1] * constants[6] + 0.237503) / 0.000239278, 0.422910)
        )
        - 37.5137
    )
    algebraic[38] = 1.00000 / (
        1.00000
        + np.exp(
            (-algebraic[15] * constants[66] * (states[0] - algebraic[34]))
            / (constants[65] * constants[68])
        )
    )
    algebraic[43] = 2.40914 / (
        1.00000 + np.power((states[0] - 158.779) / -52.1497, 2.00000)
    )
    rates[18] = (algebraic[38] - states[18]) / algebraic[43]
    algebraic[16] = -0.681249 / (
        1.00000 + np.power((states[1] * constants[7] - 0.218988) / 0.428335, 2.00000)
    ) + 1.40001 / (
        1.00000 + np.power((states[1] * constants[7] + 228.710) / 684.946, 2.00000)
    )
    algebraic[35] = (
        8540.23
        / (
            1.00000
            + np.power((states[1] * constants[7] + 0.401189) / 0.00399115, 0.668054)
        )
        - 109.275
    )
    algebraic[39] = 1.00000 / (
        1.00000
        + np.exp(
            (-algebraic[16] * constants[66] * (states[0] - algebraic[35]))
            / (constants[65] * constants[68])
        )
    )
    algebraic[44] = 13.8049 / (
        1.00000 + np.power((states[0] - 153.019) / 66.4952, 2.00000)
    )
    rates[19] = (algebraic[39] - states[19]) / algebraic[44]
    algebraic[17] = 1.00000 / (1.00000 + np.exp((states[0] + 105.390) / 8.65530))
    algebraic[36] = 3.50000e-06 * np.exp(-0.0497000 * states[0])
    algebraic[40] = 0.0400300 * np.exp(0.0521100 * states[0])
    algebraic[45] = 1.00000 / (algebraic[36] + algebraic[40])
    rates[20] = (algebraic[17] - states[20]) / algebraic[45]
    algebraic[18] = (states[0] * constants[66]) / (constants[65] * constants[68])
    algebraic[41] = 0.000600000 * np.exp(2.53000 * algebraic[18])
    algebraic[46] = 0.100000 * np.exp(-5.00000 * algebraic[18])
    algebraic[48] = 1.00000 / (
        1.00000
        + algebraic[46]
        * (
            np.power(algebraic[41] / states[1], 2.00000)
            + algebraic[41] / states[1]
            + 1.00000
        )
    )
    algebraic[50] = (
        -160.000
        + 210.000 / (1.00000 + np.exp((states[0] + 4.56000) / 11.6200))
        + 170.000 / (1.00000 + np.exp(-(states[0] + 25.5000) / 11.6200))
    )
    rates[21] = (algebraic[48] - states[21]) / algebraic[50]
    algebraic[0] = custom_piecewise(
        [
            np.less(voi, constants[0]),
            0.00000,
            np.less(voi % constants[1], constants[2]),
            constants[3],
            True,
            0.00000,
        ]
    )
    algebraic[42] = (
        constants[16]
        * states[3]
        * states[3]
        * states[3]
        * states[4]
        * (states[0] - constants[71])
    )
    algebraic[47] = 1.00000 / (1.00000 + np.power(states[1] / constants[19], 4.00000))
    algebraic[49] = (
        constants[17]
        * algebraic[47]
        * states[5]
        * states[5]
        * (0.800000 * states[6] + 0.200000 * states[7])
        * (states[0] - constants[18])
    )
    algebraic[51] = (
        constants[20] * states[8] * states[8] * states[9] * (states[0] - constants[21])
    )
    algebraic[52] = constants[23] * (states[0] - constants[72])
    algebraic[53] = (
        constants[24]
        * states[10]
        * states[10]
        * (0.380000 * states[11] + 0.630000 * states[12])
        * (states[0] - constants[72])
    )
    algebraic[54] = (
        constants[25]
        * states[13]
        * states[13]
        * (0.750000 * states[14] + 0.250000 * states[15])
        * (states[0] - constants[72])
    )
    algebraic[55] = (
        constants[28] * states[16] * states[17] * (states[0] - constants[72])
    )
    algebraic[56] = (
        constants[22] * constants[26] * states[18] * (states[0] - constants[72])
    )
    algebraic[57] = (
        constants[22] * constants[27] * states[19] * (states[0] - constants[72])
    )
    algebraic[58] = constants[30] * states[20] * (states[0] - constants[77])
    algebraic[59] = constants[29] * states[21] * (states[0] - constants[73])
    algebraic[37] = ((constants[65] * constants[68]) / constants[66]) * np.log(
        (
            constants[32] * constants[57]
            + constants[33] * constants[58]
            + (4.00000 * constants[34] * constants[12])
            / (1.00000 + np.exp(algebraic[18]))
        )
        / (
            constants[32] * constants[11]
            + constants[33] * constants[53]
            + (4.00000 * constants[34] * states[1]) / (1.00000 + np.exp(algebraic[18]))
        )
    )
    algebraic[63] = (
        constants[54]
        * constants[61]
        * constants[37]
        * constants[31]
        * (states[0] - algebraic[37])
    )
    algebraic[60] = (
        constants[54]
        * constants[55]
        * constants[36]
        * constants[31]
        * (states[0] - algebraic[37])
    )
    algebraic[65] = (
        constants[54]
        * constants[59]
        * constants[38]
        * constants[31]
        * (states[0] - algebraic[37])
    )
    algebraic[66] = 1.00000 / (
        1.00000
        + 0.124500 * np.exp(-0.100000 * algebraic[18])
        + 0.00219000
        * np.exp(constants[58] / 49.7100)
        * np.exp(-1.90000 * algebraic[18])
    )
    algebraic[67] = constants[69] * constants[81] * constants[82] * algebraic[66]
    algebraic[70] = 1.00000 / (
        1.00000 + np.power(constants[43] / states[1], constants[44])
    )
    algebraic[68] = np.exp((constants[80] - 1.00000) * algebraic[18])
    algebraic[69] = np.exp(constants[80] * algebraic[18])
    algebraic[71] = (np.power(constants[53], 3.00000)) * constants[12] * algebraic[
        69
    ] - (np.power(constants[58], 3.00000)) * states[1] * algebraic[68]
    algebraic[72] = 1.00000 + constants[79] * algebraic[68]
    algebraic[73] = (
        constants[48] * (np.power(constants[53], 3.00000))
        + (np.power(constants[47], 3.00000)) * states[1]
        + (np.power(constants[45], 3.00000))
        * constants[12]
        * (1.00000 + states[1] / constants[46])
    )
    algebraic[74] = (
        constants[12] * (np.power(constants[53], 3.00000))
        + (np.power(constants[58], 3.00000)) * states[1]
        + (np.power(constants[58], 3.00000))
        * constants[46]
        * (1.00000 + np.power(constants[53] / constants[45], 3.00000))
    )
    algebraic[75] = (constants[10] * constants[78] * algebraic[70] * algebraic[71]) / (
        algebraic[72] * (algebraic[73] + algebraic[74])
    )
    algebraic[76] = (
        (
            (0.500000 * constants[64] * constants[66])
            / (constants[63] * constants[67] * constants[62])
        )
        * constants[9]
        * algebraic[75]
    )
    algebraic[79] = (
        algebraic[42]
        + algebraic[58]
        + algebraic[76]
        + algebraic[67]
        + algebraic[49]
        + algebraic[51]
        + algebraic[59]
        + algebraic[53]
        + algebraic[54]
        + algebraic[55]
        + algebraic[56]
        + algebraic[57]
        + algebraic[63]
        + algebraic[65]
        + algebraic[60]
        + algebraic[52]
    )
    rates[0] = -(algebraic[79] + algebraic[0])
    algebraic[61] = algebraic[49] + algebraic[51] + algebraic[60]
    algebraic[62] = (
        (constants[63] * constants[67] * constants[62])
        / (constants[64] * constants[66])
    ) * algebraic[61]
    algebraic[77] = constants[40] / (
        1.00000 + np.power(constants[41] / states[1], constants[42])
    )
    algebraic[80] = algebraic[62] + algebraic[75] + algebraic[77]
    rates[1] = -algebraic[80]
    return rates


def compute_algebraic(constants, states, voi):
    """Computes algebraics of the system

    Args:
    constants -- list[int], list of constant values.
    states -- list[float], list of states.
    voi -- list[float], list of voi.

    Returns:
    algebraic -- np.array[float], list of computed algebraics.

    """
    algebraic = np.array([[0.0] * len(voi)] * sizeAlgebraic)
    states = np.array(states)
    voi = np.array(voi)
    algebraic[6] = 1.00000 / (1.00000 + np.exp((states[0] + 38.0000) / 7.00000))
    algebraic[1] = 1.00000 / (
        1.00000 + np.power((constants[50] * constants[5]) / states[1], constants[51])
    )
    algebraic[19] = 4000.00 * (
        0.234845
        + (1.00000 - 0.234845)
        / (
            1.00000
            + np.power(states[1] / (constants[50] * constants[5]), constants[51])
        )
    )
    algebraic[3] = 1.00000 / (1.00000 + np.exp(-(states[0] + 35.9584) / 9.24013))
    algebraic[20] = 0.250000 + 7.00000 / (
        1.00000 + np.exp((states[0] + 38.0000) / 10.0000)
    )
    algebraic[4] = 1.00000 / (1.00000 + np.exp((states[0] + 57.0000) / 8.00000))
    algebraic[21] = 0.900000 + 1002.85 / (
        1.00000 + np.power((states[0] + 47.5000) / 1.50000, 2.00000)
    )
    algebraic[5] = 1.00000 / (1.00000 + np.exp(-(states[0] + 22.0000) / 7.00000))
    algebraic[22] = 2.29000 + 5.70000 / (
        1.00000 + np.power((states[0] + 29.9700) / 9.00000, 2.00000)
    )
    algebraic[23] = 90.9699 * (
        1.00000
        - 1.00000
        / (
            (1.00000 + np.exp((states[0] + 13.9629) / 45.3782))
            * (1.00000 + np.exp(-(states[0] + 9.49866) / 3.39450))
        )
    )
    algebraic[7] = 1.00000 / (1.00000 + np.exp(-(states[0] + 54.2300) / 9.88000))
    algebraic[24] = 0.450000 + 3.90000 / (
        1.00000 + np.power((states[0] + 66.0000) / 26.0000, 2.00000)
    )
    algebraic[8] = 0.0200000 + 0.980000 / (
        1.00000 + np.exp((states[0] + 72.9780) / 4.64000)
    )
    algebraic[25] = 150.000 * (
        1.00000
        - 1.00000
        / (
            (1.00000 + np.exp((states[0] - 417.430) / 203.180))
            * (1.00000 + np.exp(-(states[0] + 61.1100) / 8.07000))
        )
    )
    algebraic[9] = 0.978613 / (1.00000 + np.exp(-(states[0] + 18.6736) / 26.6606))
    algebraic[26] = 500.000 / (
        1.00000 + np.power((states[0] + 60.7100) / 15.7900, 2.00000)
    )
    algebraic[10] = 1.00000 / (1.00000 + np.exp((states[0] + 63.0000) / 6.30000))
    algebraic[27] = 5000.00 / (
        1.00000 + np.power((states[0] + 62.7133) / 35.8611, 2.00000)
    )
    algebraic[28] = 30000.0 + 220000.0 / (
        1.00000 + np.exp((states[0] + 22.0000) / 4.00000)
    )
    algebraic[11] = 0.948000 / (1.00000 + np.exp(-(states[0] + 17.9100) / 18.4000))
    algebraic[29] = 100.000 / (
        1.00000 + np.power((states[0] + 64.1000) / 28.6700, 2.00000)
    )
    algebraic[12] = 1.00000 / (1.00000 + np.exp((states[0] + 21.2000) / 5.70000))
    algebraic[30] = 1.00000e06 * (
        1.00000
        - 1.00000
        / (
            (1.00000 + np.exp((states[0] - 315.000) / 50.0000))
            * (1.00000 + np.exp(-(states[0] + 74.9000) / 8.00000))
        )
    )
    algebraic[31] = 2.50000e06 * (
        1.00000
        - 1.00000
        / (
            (1.00000 + np.exp((states[0] - 132.868) / 25.3992))
            * (1.00000 + np.exp(-(states[0] + 24.9203) / 2.67915))
        )
    )
    algebraic[13] = 1.00000 / (1.00000 + np.exp(-(states[0] + 27.7900) / 7.57000))
    algebraic[32] = 17.0000 / (
        1.00000 + np.power((states[0] + 20.5232) / 35.0000, 2.00000)
    )
    algebraic[14] = 0.0200000 + 0.980000 / (
        1.00000 + np.exp((states[0] + 69.5000) / 6.00000)
    )
    algebraic[33] = 7.50000 + 10.0000 / (
        1.00000 + np.power((states[0] + 34.1765) / 120.000, 2.00000)
    )
    algebraic[15] = -0.749234 / (
        1.00000 + np.power((states[1] * constants[6] - 0.0630535) / 0.161942, 2.00000)
    ) + 8.38384 / (
        1.00000 + np.power((states[1] * constants[6] + 1538.29) / 739.057, 2.00000)
    )
    algebraic[34] = (
        5011.47
        / (
            1.00000
            + np.power((states[1] * constants[6] + 0.237503) / 0.000239278, 0.422910)
        )
        - 37.5137
    )
    algebraic[38] = 1.00000 / (
        1.00000
        + np.exp(
            (-algebraic[15] * constants[66] * (states[0] - algebraic[34]))
            / (constants[65] * constants[68])
        )
    )
    algebraic[43] = 2.40914 / (
        1.00000 + np.power((states[0] - 158.779) / -52.1497, 2.00000)
    )
    algebraic[16] = -0.681249 / (
        1.00000 + np.power((states[1] * constants[7] - 0.218988) / 0.428335, 2.00000)
    ) + 1.40001 / (
        1.00000 + np.power((states[1] * constants[7] + 228.710) / 684.946, 2.00000)
    )
    algebraic[35] = (
        8540.23
        / (
            1.00000
            + np.power((states[1] * constants[7] + 0.401189) / 0.00399115, 0.668054)
        )
        - 109.275
    )
    algebraic[39] = 1.00000 / (
        1.00000
        + np.exp(
            (-algebraic[16] * constants[66] * (states[0] - algebraic[35]))
            / (constants[65] * constants[68])
        )
    )
    algebraic[44] = 13.8049 / (
        1.00000 + np.power((states[0] - 153.019) / 66.4952, 2.00000)
    )
    algebraic[17] = 1.00000 / (1.00000 + np.exp((states[0] + 105.390) / 8.65530))
    algebraic[36] = 3.50000e-06 * np.exp(-0.0497000 * states[0])
    algebraic[40] = 0.0400300 * np.exp(0.0521100 * states[0])
    algebraic[45] = 1.00000 / (algebraic[36] + algebraic[40])
    algebraic[18] = (states[0] * constants[66]) / (constants[65] * constants[68])
    algebraic[41] = 0.000600000 * np.exp(2.53000 * algebraic[18])
    algebraic[46] = 0.100000 * np.exp(-5.00000 * algebraic[18])
    algebraic[48] = 1.00000 / (
        1.00000
        + algebraic[46]
        * (
            np.power(algebraic[41] / states[1], 2.00000)
            + algebraic[41] / states[1]
            + 1.00000
        )
    )
    algebraic[50] = (
        -160.000
        + 210.000 / (1.00000 + np.exp((states[0] + 4.56000) / 11.6200))
        + 170.000 / (1.00000 + np.exp(-(states[0] + 25.5000) / 11.6200))
    )
    algebraic[0] = custom_piecewise(
        [
            np.less(voi, constants[0]),
            0.00000,
            np.less(voi % constants[1], constants[2]),
            constants[3],
            True,
            0.00000,
        ]
    )
    algebraic[42] = (
        constants[16]
        * states[3]
        * states[3]
        * states[3]
        * states[4]
        * (states[0] - constants[71])
    )
    algebraic[47] = 1.00000 / (1.00000 + np.power(states[1] / constants[19], 4.00000))
    algebraic[49] = (
        constants[17]
        * algebraic[47]
        * states[5]
        * states[5]
        * (0.800000 * states[6] + 0.200000 * states[7])
        * (states[0] - constants[18])
    )
    algebraic[51] = (
        constants[20] * states[8] * states[8] * states[9] * (states[0] - constants[21])
    )
    algebraic[52] = constants[23] * (states[0] - constants[72])
    algebraic[53] = (
        constants[24]
        * states[10]
        * states[10]
        * (0.380000 * states[11] + 0.630000 * states[12])
        * (states[0] - constants[72])
    )
    algebraic[54] = (
        constants[25]
        * states[13]
        * states[13]
        * (0.750000 * states[14] + 0.250000 * states[15])
        * (states[0] - constants[72])
    )
    algebraic[55] = (
        constants[28] * states[16] * states[17] * (states[0] - constants[72])
    )
    algebraic[56] = (
        constants[22] * constants[26] * states[18] * (states[0] - constants[72])
    )
    algebraic[57] = (
        constants[22] * constants[27] * states[19] * (states[0] - constants[72])
    )
    algebraic[58] = constants[30] * states[20] * (states[0] - constants[77])
    algebraic[59] = constants[29] * states[21] * (states[0] - constants[73])
    algebraic[37] = ((constants[65] * constants[68]) / constants[66]) * np.log(
        (
            constants[32] * constants[57]
            + constants[33] * constants[58]
            + (4.00000 * constants[34] * constants[12])
            / (1.00000 + np.exp(algebraic[18]))
        )
        / (
            constants[32] * constants[11]
            + constants[33] * constants[53]
            + (4.00000 * constants[34] * states[1]) / (1.00000 + np.exp(algebraic[18]))
        )
    )
    algebraic[63] = (
        constants[54]
        * constants[61]
        * constants[37]
        * constants[31]
        * (states[0] - algebraic[37])
    )
    algebraic[60] = (
        constants[54]
        * constants[55]
        * constants[36]
        * constants[31]
        * (states[0] - algebraic[37])
    )
    algebraic[65] = (
        constants[54]
        * constants[59]
        * constants[38]
        * constants[31]
        * (states[0] - algebraic[37])
    )
    algebraic[66] = 1.00000 / (
        1.00000
        + 0.124500 * np.exp(-0.100000 * algebraic[18])
        + 0.00219000
        * np.exp(constants[58] / 49.7100)
        * np.exp(-1.90000 * algebraic[18])
    )
    algebraic[67] = constants[69] * constants[81] * constants[82] * algebraic[66]
    algebraic[70] = 1.00000 / (
        1.00000 + np.power(constants[43] / states[1], constants[44])
    )
    algebraic[68] = np.exp((constants[80] - 1.00000) * algebraic[18])
    algebraic[69] = np.exp(constants[80] * algebraic[18])
    algebraic[71] = (np.power(constants[53], 3.00000)) * constants[12] * algebraic[
        69
    ] - (np.power(constants[58], 3.00000)) * states[1] * algebraic[68]
    algebraic[72] = 1.00000 + constants[79] * algebraic[68]
    algebraic[73] = (
        constants[48] * (np.power(constants[53], 3.00000))
        + (np.power(constants[47], 3.00000)) * states[1]
        + (np.power(constants[45], 3.00000))
        * constants[12]
        * (1.00000 + states[1] / constants[46])
    )
    algebraic[74] = (
        constants[12] * (np.power(constants[53], 3.00000))
        + (np.power(constants[58], 3.00000)) * states[1]
        + (np.power(constants[58], 3.00000))
        * constants[46]
        * (1.00000 + np.power(constants[53] / constants[45], 3.00000))
    )
    algebraic[75] = (constants[10] * constants[78] * algebraic[70] * algebraic[71]) / (
        algebraic[72] * (algebraic[73] + algebraic[74])
    )
    algebraic[76] = (
        (
            (0.500000 * constants[64] * constants[66])
            / (constants[63] * constants[67] * constants[62])
        )
        * constants[9]
        * algebraic[75]
    )
    algebraic[79] = (
        algebraic[42]
        + algebraic[58]
        + algebraic[76]
        + algebraic[67]
        + algebraic[49]
        + algebraic[51]
        + algebraic[59]
        + algebraic[53]
        + algebraic[54]
        + algebraic[55]
        + algebraic[56]
        + algebraic[57]
        + algebraic[63]
        + algebraic[65]
        + algebraic[60]
        + algebraic[52]
    )
    algebraic[61] = algebraic[49] + algebraic[51] + algebraic[60]
    algebraic[62] = (
        (constants[63] * constants[67] * constants[62])
        / (constants[64] * constants[66])
    ) * algebraic[61]
    algebraic[77] = constants[40] / (
        1.00000 + np.power(constants[41] / states[1], constants[42])
    )
    algebraic[80] = algebraic[62] + algebraic[75] + algebraic[77]
    algebraic[2] = constants[49] * (states[2] - 0.234500)
    algebraic[64] = algebraic[62] * constants[4]
    algebraic[78] = algebraic[75] * constants[4]
    algebraic[81] = algebraic[77] * constants[4]
    return algebraic


def custom_piecewise(cases):
    """Compute result of a piecewise function

    Args:
    cases -- list, list of piece cases.

    Returns:

    """
    return np.select(cases[0::2], cases[1::2])


def solve_model(init_states, constants, start=0, end=15000, nb_steps=100000):
    """Solve model with ODE solver

    Args:
    init_states -- list[float], list of initial states.
    constants -- list[int], list of constant values.
    start -- float, start time in ms for the simulation, default value 0.
    end -- float, end time in ms for the simulation, default value 15000.
    nb_steps -- int, number of steps in the simulation, default value 100000.

    Returns:

    """
    # Set timespan to solve over
    voi = np.linspace(start, end, nb_steps)

    # Construct ODE object to solve
    r = ode(compute_rates)
    r.set_integrator(
        SOLVER,
        method=METHOD,
        atol=ATOL,
        rtol=RTOL,
        max_step=MAX_STEP,
    )
    r.set_initial_value(init_states, voi[0])
    r.set_f_params(constants)

    # Solve model
    states = np.array([[0.0] * len(voi)] * sizeStates)
    states[:, 0] = init_states
    for i, t in enumerate(voi[1:]):
        if r.successful():
            r.integrate(t)
            states[:, i + 1] = r.y
        else:
            break

    # Compute algebraic variables
    algebraic = compute_algebraic(constants, states, voi)
    return (voi, states, algebraic)
