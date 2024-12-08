#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tong2014.py

Tong2014 cell model Python version
Author: Mathias Roesler
Date: 11/24
"""

import numpy as np

from scipy.integrate import ode
from conversion.constants import SOLVER, METHOD, ATOL, RTOL, MAX_STEP


# Size of variable np.arrays:
sizeAlgebraic = 107
sizeStates = 35
sizeConstants = 89


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
    legend_algebraic[104] = "I_tot in component membrane_potential (pA_per_pF)"
    legend_algebraic[86] = "I_Ca_tot in component membrane_potential (pA_per_pF)"
    legend_states[0] = "v in component membrane_potential (mV)"
    legend_constants[73] = "Cm in component parameters (uF_per_cm2)"
    legend_algebraic[63] = "ina in component I_Na (pA_per_pF)"
    legend_algebraic[70] = "ical in component I_CaL (pA_per_pF)"
    legend_algebraic[72] = "icat in component I_CaT (pA_per_pF)"
    legend_algebraic[73] = "ib in component I_b (pA_per_pF)"
    legend_algebraic[74] = "iherg in component I_HERG (pA_per_pF)"
    legend_algebraic[75] = "ikcnq1 in component I_KCNQ1 (pA_per_pF)"
    legend_algebraic[76] = "ikcnq4 in component I_KCNQ4 (pA_per_pF)"
    legend_algebraic[77] = "ikcnq5 in component I_KCNQ5 (pA_per_pF)"
    legend_algebraic[78] = "ik1 in component I_K1 (pA_per_pF)"
    legend_algebraic[79] = "ik2 in component I_K2 (pA_per_pF)"
    legend_algebraic[80] = "ika in component I_Ka (pA_per_pF)"
    legend_algebraic[81] = "iBKa in component I_BKa (pA_per_pF)"
    legend_algebraic[82] = "iBKab in component I_BKab (pA_per_pF)"
    legend_algebraic[83] = "ih in component I_h (pA_per_pF)"
    legend_algebraic[84] = "icl in component I_Cl (pA_per_pF)"
    legend_algebraic[88] = "insna in component I_ns (pA_per_pF)"
    legend_algebraic[85] = "insca in component I_ns (pA_per_pF)"
    legend_algebraic[90] = "insk in component I_ns (pA_per_pF)"
    legend_algebraic[92] = "inak in component I_NaK (pA_per_pF)"
    legend_algebraic[101] = "inaca in component I_NaCa (pA_per_pF)"
    legend_algebraic[105] = "J_tot in component Ca_Concentrations (mM_per_msec)"
    legend_algebraic[87] = "J_Ca_mem in component Ca_Concentrations (mM_per_msec)"
    legend_states[1] = "cai in component Ca_Concentrations (mM)"
    legend_algebraic[100] = "jnaca in component J_NaCa (mM_per_msec)"
    legend_algebraic[102] = "jpmca in component J_PMCA (mM_per_msec)"
    legend_constants[68] = "buff in component parameters (dimensionless)"
    legend_constants[69] = "AV in component parameters (cm2_per_uL)"
    legend_constants[70] = "zca in component parameters (dimensionless)"
    legend_constants[72] = "frdy in component parameters (coulomb_per_mole)"
    legend_algebraic[89] = "jcamem_plot in component Ca_Concentrations (M_per_msec)"
    legend_algebraic[106] = "jpmca_plot in component Ca_Concentrations (M_per_msec)"
    legend_algebraic[103] = "jnaca_plot in component Ca_Concentrations (M_per_msec)"
    legend_constants[4] = "conversion in component Ca_Concentrations (mM_to_M)"
    legend_constants[11] = "ki in component parameters (mM)"
    legend_constants[59] = "nai in component parameters (mM)"
    legend_constants[62] = "cli in component parameters (mM)"
    legend_constants[63] = "ko in component parameters (mM)"
    legend_constants[12] = "cao in component parameters (mM)"
    legend_constants[64] = "nao in component parameters (mM)"
    legend_constants[66] = "clo in component parameters (mM)"
    legend_constants[13] = "mgo in component parameters (mM)"
    legend_constants[14] = "zna in component parameters (dimensionless)"
    legend_constants[15] = "zk in component parameters (dimensionless)"
    legend_constants[71] = "R in component parameters (joule_per_kelvin_per_kilomole)"
    legend_constants[74] = "temp in component parameters (kelvin)"
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
    legend_constants[29] = "gkq1 in component parameters (nS_per_pF)"
    legend_constants[30] = "gkq4 in component parameters (nS_per_pF)"
    legend_constants[31] = "gkq5 in component parameters (nS_per_pF)"
    legend_constants[32] = "gherg in component parameters (nS_per_pF)"
    legend_constants[33] = "gcl in component parameters (nS_per_pF)"
    legend_constants[34] = "gh in component parameters (nS_per_pF)"
    legend_constants[35] = "gns in component parameters (nS_per_pF)"
    legend_constants[36] = "PnsK in component parameters (dimensionless)"
    legend_constants[37] = "PnsNa in component parameters (dimensionless)"
    legend_constants[38] = "PnsCa in component parameters (dimensionless)"
    legend_constants[39] = "PnsCs in component parameters (dimensionless)"
    legend_constants[40] = "gnsCa in component parameters (dimensionless)"
    legend_constants[41] = "gnsNa in component parameters (dimensionless)"
    legend_constants[42] = "gnsK in component parameters (dimensionless)"
    legend_constants[43] = "gnsCs in component parameters (dimensionless)"
    legend_constants[75] = "ginak in component parameters (pA_per_pF)"
    legend_constants[80] = "nakKmko in component parameters (mM)"
    legend_constants[82] = "nakKmnai in component parameters (mM)"
    legend_constants[76] = "PK in component parameters (dimensionless)"
    legend_constants[81] = "PNa in component parameters (dimensionless)"
    legend_constants[44] = "Jpmca in component parameters (mM_per_msec)"
    legend_constants[45] = "Kmpmca in component parameters (mM)"
    legend_constants[46] = "npmca in component parameters (dimensionless)"
    legend_constants[84] = "Jnaca in component parameters (mM_per_msec)"
    legend_constants[47] = "Kmallo in component parameters (mM)"
    legend_constants[48] = "nallo in component parameters (dimensionless)"
    legend_constants[85] = "ksat in component parameters (dimensionless)"
    legend_constants[86] = "xgamma in component parameters (dimensionless)"
    legend_constants[49] = "Kmnai in component parameters (mM)"
    legend_constants[50] = "Kmcai in component parameters (mM)"
    legend_constants[51] = "Kmnao in component parameters (mM)"
    legend_constants[52] = "Kmcao in component parameters (mM)"
    legend_constants[53] = "Fmax in component parameters (uN)"
    legend_constants[54] = "FKm in component parameters (nM)"
    legend_constants[55] = "Fn in component parameters (dimensionless)"
    legend_algebraic[28] = "vFRT in component parameters (dimensionless)"
    legend_constants[77] = "ena in component parameters (mV)"
    legend_constants[78] = "ek in component parameters (mV)"
    legend_constants[83] = "eh in component parameters (mV)"
    legend_constants[79] = "ecl in component parameters (mV)"
    legend_algebraic[58] = "enscc in component parameters (mV)"
    legend_algebraic[1] = "wss in component Ca_dependent_Force (dimensionless)"
    legend_algebraic[29] = "wtc in component Ca_dependent_Force (msec)"
    legend_constants[5] = "conversion in component Ca_dependent_Force (nM_to_mM)"
    legend_algebraic[2] = "Force in component Ca_dependent_Force (uN)"
    legend_states[2] = "w in component Ca_dependent_Force (dimensionless)"
    legend_algebraic[3] = "mss in component I_Na (dimensionless)"
    legend_algebraic[4] = "hss in component I_Na (dimensionless)"
    legend_algebraic[30] = "mtc in component I_Na (msec)"
    legend_algebraic[31] = "htc in component I_Na (msec)"
    legend_states[3] = "m in component I_Na (dimensionless)"
    legend_states[4] = "h in component I_Na (dimensionless)"
    legend_algebraic[5] = "dss in component I_CaL (dimensionless)"
    legend_algebraic[6] = "fss in component I_CaL (dimensionless)"
    legend_algebraic[68] = "fca in component I_CaL (dimensionless)"
    legend_algebraic[32] = "dtc in component I_CaL (msec)"
    legend_constants[56] = "f1tc in component I_CaL (msec)"
    legend_algebraic[33] = "f2tc in component I_CaL (msec)"
    legend_states[5] = "d in component I_CaL (dimensionless)"
    legend_states[6] = "f1 in component I_CaL (dimensionless)"
    legend_states[7] = "f2 in component I_CaL (dimensionless)"
    legend_algebraic[7] = "bss in component I_CaT (dimensionless)"
    legend_algebraic[8] = "gss in component I_CaT (dimensionless)"
    legend_algebraic[34] = "btc in component I_CaT (msec)"
    legend_algebraic[35] = "gtc in component I_CaT (msec)"
    legend_states[8] = "b in component I_CaT (dimensionless)"
    legend_states[9] = "g in component I_CaT (dimensionless)"
    legend_algebraic[9] = "hnss in component I_HERG (dimensionless)"
    legend_algebraic[10] = "hsss in component I_HERG (dimensionless)"
    legend_algebraic[36] = "hn1tc in component I_HERG (msec)"
    legend_algebraic[37] = "hn2tc in component I_HERG (msec)"
    legend_algebraic[38] = "hstc in component I_HERG (msec)"
    legend_states[10] = "hn1 in component I_HERG (dimensionless)"
    legend_states[11] = "hn2 in component I_HERG (dimensionless)"
    legend_states[12] = "hs in component I_HERG (dimensionless)"
    legend_algebraic[11] = "nq1ss in component I_KCNQ1 (dimensionless)"
    legend_algebraic[12] = "wq1ss in component I_KCNQ1 (dimensionless)"
    legend_algebraic[13] = "sq1ss in component I_KCNQ1 (dimensionless)"
    legend_algebraic[39] = "nq1ftc in component I_KCNQ1 (msec)"
    legend_algebraic[40] = "nq1stc in component I_KCNQ1 (msec)"
    legend_algebraic[41] = "wq1tc in component I_KCNQ1 (msec)"
    legend_constants[57] = "sq1tc in component I_KCNQ1 (msec)"
    legend_states[13] = "nq1f in component I_KCNQ1 (dimensionless)"
    legend_states[14] = "nq1s in component I_KCNQ1 (dimensionless)"
    legend_states[15] = "wq1 in component I_KCNQ1 (dimensionless)"
    legend_states[16] = "sq1 in component I_KCNQ1 (dimensionless)"
    legend_algebraic[14] = "nq4ss in component I_KCNQ4 (dimensionless)"
    legend_algebraic[15] = "sq4ss in component I_KCNQ4 (dimensionless)"
    legend_algebraic[42] = "nq4tc in component I_KCNQ4 (msec)"
    legend_algebraic[43] = "sq4tc in component I_KCNQ4 (msec)"
    legend_states[17] = "nq4 in component I_KCNQ4 (dimensionless)"
    legend_states[18] = "sq4 in component I_KCNQ4 (dimensionless)"
    legend_algebraic[16] = "nq5ss in component I_KCNQ5 (dimensionless)"
    legend_algebraic[17] = "wq5ss in component I_KCNQ5 (dimensionless)"
    legend_algebraic[18] = "sq5ss in component I_KCNQ5 (dimensionless)"
    legend_algebraic[44] = "nq5ftc in component I_KCNQ5 (msec)"
    legend_constants[58] = "nq5stc in component I_KCNQ5 (msec)"
    legend_algebraic[45] = "wq5tc in component I_KCNQ5 (msec)"
    legend_algebraic[46] = "sq5tc in component I_KCNQ5 (msec)"
    legend_states[19] = "nq5f in component I_KCNQ5 (dimensionless)"
    legend_states[20] = "nq5s in component I_KCNQ5 (dimensionless)"
    legend_states[21] = "wq5 in component I_KCNQ5 (dimensionless)"
    legend_states[22] = "sq5 in component I_KCNQ5 (dimensionless)"
    legend_algebraic[19] = "qss in component I_K1 (dimensionless)"
    legend_algebraic[20] = "rss in component I_K1 (dimensionless)"
    legend_algebraic[47] = "qtc in component I_K1 (msec)"
    legend_algebraic[48] = "r1tc in component I_K1 (msec)"
    legend_algebraic[49] = "r2tc in component I_K1 (msec)"
    legend_states[23] = "q in component I_K1 (dimensionless)"
    legend_states[24] = "r1 in component I_K1 (dimensionless)"
    legend_states[25] = "r2 in component I_K1 (dimensionless)"
    legend_algebraic[21] = "pss in component I_K2 (dimensionless)"
    legend_algebraic[22] = "kss in component I_K2 (dimensionless)"
    legend_algebraic[50] = "ptc in component I_K2 (msec)"
    legend_algebraic[51] = "k1tc in component I_K2 (msec)"
    legend_algebraic[52] = "k2tc in component I_K2 (msec)"
    legend_states[26] = "p in component I_K2 (dimensionless)"
    legend_states[27] = "k1 in component I_K2 (dimensionless)"
    legend_states[28] = "k2 in component I_K2 (dimensionless)"
    legend_algebraic[23] = "sss in component I_Ka (dimensionless)"
    legend_algebraic[24] = "xss in component I_Ka (dimensionless)"
    legend_algebraic[53] = "stc in component I_Ka (msec)"
    legend_algebraic[54] = "xtc in component I_Ka (msec)"
    legend_states[29] = "s in component I_Ka (dimensionless)"
    legend_states[30] = "x in component I_Ka (dimensionless)"
    legend_algebraic[25] = "xass_z in component I_BKa (dimensionless)"
    legend_algebraic[55] = "xass_vh in component I_BKa (mV)"
    legend_constants[6] = "conversion in component I_BKa (mM_to_M)"
    legend_algebraic[59] = "xass in component I_BKa (dimensionless)"
    legend_algebraic[64] = "xatc in component I_BKa (msec)"
    legend_states[31] = "xa in component I_BKa (dimensionless)"
    legend_algebraic[26] = "xabss_z in component I_BKab (dimensionless)"
    legend_algebraic[56] = "xabss_vh in component I_BKab (mV)"
    legend_constants[7] = "conversion in component I_BKab (mM_to_M)"
    legend_algebraic[60] = "xabss in component I_BKab (dimensionless)"
    legend_algebraic[65] = "xabtc in component I_BKab (msec)"
    legend_states[32] = "xab in component I_BKab (dimensionless)"
    legend_algebraic[27] = "yss in component I_h (dimensionless)"
    legend_algebraic[66] = "ytc in component I_h (msec)"
    legend_algebraic[57] = "ya in component I_h (per_msec)"
    legend_algebraic[61] = "yb in component I_h (per_msec)"
    legend_states[33] = "y in component I_h (dimensionless)"
    legend_algebraic[69] = "css in component I_Cl (dimensionless)"
    legend_algebraic[71] = "ctc in component I_Cl (msec)"
    legend_algebraic[62] = "K1cl in component I_Cl (mM)"
    legend_algebraic[67] = "K2cl in component I_Cl (dimensionless)"
    legend_states[34] = "c in component I_Cl (dimensionless)"
    legend_constants[60] = "fmg in component I_ns (dimensionless)"
    legend_constants[67] = "gs_nao in component I_ns (dimensionless)"
    legend_constants[61] = "gs_cao in component I_ns (dimensionless)"
    legend_constants[65] = "gs_ko in component I_ns (dimensionless)"
    legend_constants[8] = "tinyamount in component I_ns (mM)"
    legend_algebraic[91] = "fnak in component I_NaK (dimensionless)"
    legend_constants[87] = "knak in component I_NaK (dimensionless)"
    legend_constants[88] = "nnak in component I_NaK (dimensionless)"
    legend_constants[9] = "inaca_sign in component I_NaCa (dimensionless)"
    legend_algebraic[93] = "f1naca in component J_NaCa (dimensionless)"
    legend_algebraic[94] = "f2naca in component J_NaCa (dimensionless)"
    legend_algebraic[95] = "fallo in component J_NaCa (dimensionless)"
    legend_algebraic[96] = "naca_Eup in component J_NaCa (mM4)"
    legend_algebraic[97] = "naca_Ed1 in component J_NaCa (dimensionless)"
    legend_algebraic[98] = "naca_Ed2 in component J_NaCa (mM4)"
    legend_algebraic[99] = "naca_Ed3 in component J_NaCa (mM4)"
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
    legend_rates[10] = "d/dt hn1 in component I_HERG (dimensionless)"
    legend_rates[11] = "d/dt hn2 in component I_HERG (dimensionless)"
    legend_rates[12] = "d/dt hs in component I_HERG (dimensionless)"
    legend_rates[13] = "d/dt nq1f in component I_KCNQ1 (dimensionless)"
    legend_rates[14] = "d/dt nq1s in component I_KCNQ1 (dimensionless)"
    legend_rates[15] = "d/dt wq1 in component I_KCNQ1 (dimensionless)"
    legend_rates[16] = "d/dt sq1 in component I_KCNQ1 (dimensionless)"
    legend_rates[17] = "d/dt nq4 in component I_KCNQ4 (dimensionless)"
    legend_rates[18] = "d/dt sq4 in component I_KCNQ4 (dimensionless)"
    legend_rates[19] = "d/dt nq5f in component I_KCNQ5 (dimensionless)"
    legend_rates[20] = "d/dt nq5s in component I_KCNQ5 (dimensionless)"
    legend_rates[21] = "d/dt wq5 in component I_KCNQ5 (dimensionless)"
    legend_rates[22] = "d/dt sq5 in component I_KCNQ5 (dimensionless)"
    legend_rates[23] = "d/dt q in component I_K1 (dimensionless)"
    legend_rates[24] = "d/dt r1 in component I_K1 (dimensionless)"
    legend_rates[25] = "d/dt r2 in component I_K1 (dimensionless)"
    legend_rates[26] = "d/dt p in component I_K2 (dimensionless)"
    legend_rates[27] = "d/dt k1 in component I_K2 (dimensionless)"
    legend_rates[28] = "d/dt k2 in component I_K2 (dimensionless)"
    legend_rates[29] = "d/dt s in component I_Ka (dimensionless)"
    legend_rates[30] = "d/dt x in component I_Ka (dimensionless)"
    legend_rates[31] = "d/dt xa in component I_BKa (dimensionless)"
    legend_rates[32] = "d/dt xab in component I_BKab (dimensionless)"
    legend_rates[33] = "d/dt y in component I_h (dimensionless)"
    legend_rates[34] = "d/dt c in component I_Cl (dimensionless)"
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
    states[0] = -50.80774403486136
    states[1] = 0.0001235555354004079
    constants[4] = 1000
    constants[5] = 1e-6
    states[2] = 0.2768302028689621
    states[3] = 0.166998688814229
    states[4] = 0.3156075507278521
    states[5] = 0.01605749091924106
    states[6] = 0.861723329545759
    states[7] = 0.8617233295451014
    states[8] = 0.5857399935992883
    states[9] = 0.02817518341064734
    states[10] = 0.02498997383730429
    states[11] = 0.02498997383730429
    states[12] = 0.5292140214748325
    states[13] = 0.09043683263784785
    states[14] = 0.09043683263784785
    states[15] = 0.9230513956601629
    states[16] = 0.7426740827665872
    states[17] = 0.1081102112425531
    states[18] = 0.6280622663818354
    states[19] = 0.2618890409031491
    states[20] = 0.2618890409031491
    states[21] = 0.9230513956601629
    states[22] = 0.6280622663818354
    states[23] = 0.22560249352574
    states[24] = 0.1261674553968813
    states[25] = 0.1261674420211442
    states[26] = 0.1358747732875166
    states[27] = 0.9944827384537837
    states[28] = 0.9944827384537837
    states[29] = 0.04562272513582834
    states[30] = 0.06162789823439722
    constants[6] = 1000.0
    states[31] = 0.0003575122973592095
    constants[7] = 1000.0
    states[32] = 0.002673927875795617
    states[33] = 0.001821587846781853
    states[34] = 0.0006695090454068198
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
    constants[23] = 0.00000
    constants[24] = 0.240000
    constants[25] = 0.0320000
    constants[26] = 0.200000
    constants[27] = 0.100000
    constants[28] = 0.160000
    constants[29] = 0.00320000
    constants[30] = 0.0240000
    constants[31] = 0.0160000
    constants[32] = 0.0800000
    constants[33] = 0.187500
    constants[34] = 0.0542000
    constants[35] = 0.0123000
    constants[36] = 1.30000
    constants[37] = 0.900000
    constants[38] = 0.890000
    constants[39] = 1.00000
    constants[40] = 0.500000
    constants[41] = 1.00000
    constants[42] = 1.19000
    constants[43] = 1.60000
    constants[44] = 3.50000e-07
    constants[45] = 0.000500000
    constants[46] = 2.00000
    constants[47] = 0.000300000
    constants[48] = 4.00000
    constants[49] = 30.0000
    constants[50] = 0.00700000
    constants[51] = 87.5000
    constants[52] = 1.30000
    constants[53] = 3.00000
    constants[54] = 161.301
    constants[55] = 3.60205
    constants[56] = 12.0000
    constants[57] = 50000.0
    constants[58] = 1000.00
    constants[59] = 4.00000
    constants[60] = 0.108043 + 0.903902 / (
        1.00000 + np.power(constants[13] / 0.281007, 1.29834)
    )
    constants[61] = ((1.00000 / 0.000525000) * 0.0300000) / (
        1.00000 + np.power(150.000 / (constants[12] + constants[8]), 2.00000)
    )
    constants[62] = 46.0000
    constants[63] = 6.00000
    constants[64] = 130.000
    constants[65] = ((1.00000 / 0.0123000) * 0.0300000) / (
        1.00000 + np.power(150.000 / (constants[63] + constants[8]), 2.00000)
    )
    constants[66] = 130.000
    constants[67] = ((1.00000 / 0.0123000) * 0.0300000) / (
        1.00000 + np.power(150.000 / (constants[64] + constants[8]), 2.00000)
    )
    constants[68] = 0.0150000
    constants[69] = 4.00000
    constants[70] = 2.00000
    constants[71] = 8314.00
    constants[72] = 96485.0
    constants[73] = 1.00000
    constants[74] = 308.000
    constants[75] = 1.70000
    constants[76] = 1.00000
    constants[77] = ((constants[71] * constants[74]) / constants[72]) * np.log(
        constants[64] / constants[59]
    )
    constants[78] = ((constants[71] * constants[74]) / constants[72]) * np.log(
        constants[63] / constants[11]
    )
    constants[79] = ((constants[71] * constants[74]) / constants[72]) * np.log(
        constants[62] / constants[66]
    )
    constants[80] = 2.00000
    constants[81] = 0.350000
    constants[82] = 22.0000
    constants[83] = ((constants[71] * constants[74]) / constants[72]) * np.log(
        (constants[63] + (constants[81] / constants[76]) * constants[64])
        / (constants[11] + (constants[81] / constants[76]) * constants[59])
    )
    constants[84] = 3.50000e-06
    constants[85] = 0.270000
    constants[86] = 0.350000
    constants[87] = 1.00000 / (
        1.00000 + np.power(constants[80] / constants[63], 1.50000)
    )
    constants[88] = 1.00000 / (
        1.00000 + np.power(constants[82] / constants[59], 2.00000)
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
    algebraic[6] = 1.00000 / \
        (1.00000 + np.exp((states[0] + 38.0000) / 7.00000))
    rates[6] = (algebraic[6] - states[6]) / constants[56]
    algebraic[13] = 0.340000 + 0.660000 / (
        1.00000 + np.exp((states[0] + 45.3000) / 12.3000)
    )
    rates[16] = (algebraic[13] - states[16]) / constants[57]
    algebraic[16] = 1.00000 / \
        (1.00000 + np.exp(-(states[0] + 36.5500) / 13.7600))
    rates[20] = (algebraic[16] - states[20]) / constants[58]
    algebraic[1] = 1.00000 / (
        1.00000 +
        np.power((constants[54] * constants[5]) / states[1], constants[55])
    )
    algebraic[29] = 4000.00 * (
        0.234845
        + (1.00000 - 0.234845)
        / (
            1.00000
            + np.power(states[1] / (constants[54] *
                       constants[5]), constants[55])
        )
    )
    rates[2] = (algebraic[1] - states[2]) / algebraic[29]
    algebraic[3] = 1.00000 / \
        (1.00000 + np.exp(-(states[0] + 35.9584) / 9.24013))
    algebraic[30] = 0.250000 + 7.00000 / (
        1.00000 + np.exp((states[0] + 38.0000) / 10.0000)
    )
    rates[3] = (algebraic[3] - states[3]) / algebraic[30]
    algebraic[4] = 1.00000 / \
        (1.00000 + np.exp((states[0] + 57.0000) / 8.00000))
    algebraic[31] = 0.900000 + 1002.85 / (
        1.00000 + np.power((states[0] + 47.5000) / 1.50000, 2.00000)
    )
    rates[4] = (algebraic[4] - states[4]) / algebraic[31]
    algebraic[5] = 1.00000 / \
        (1.00000 + np.exp(-(states[0] + 22.0000) / 7.00000))
    algebraic[32] = 2.29000 + 5.70000 / (
        1.00000 + np.power((states[0] + 29.9700) / 9.00000, 2.00000)
    )
    rates[5] = (algebraic[5] - states[5]) / algebraic[32]
    algebraic[33] = 90.9699 * (
        1.00000
        - 1.00000
        / (
            (1.00000 + np.exp((states[0] + 13.9629) / 45.3782))
            * (1.00000 + np.exp(-(states[0] + 9.49866) / 3.39450))
        )
    )
    rates[7] = (algebraic[6] - states[7]) / algebraic[33]
    algebraic[7] = 1.00000 / \
        (1.00000 + np.exp(-(states[0] + 54.2300) / 9.88000))
    algebraic[34] = 0.450000 + 3.90000 / (
        1.00000 + np.power((states[0] + 66.0000) / 26.0000, 2.00000)
    )
    rates[8] = (algebraic[7] - states[8]) / algebraic[34]
    algebraic[8] = 0.0200000 + 0.980000 / (
        1.00000 + np.exp((states[0] + 72.9780) / 4.64000)
    )
    algebraic[35] = 150.000 * (
        1.00000
        - 1.00000
        / (
            (1.00000 + np.exp((states[0] - 417.430) / 203.180))
            * (1.00000 + np.exp(-(states[0] + 61.1100) / 8.07000))
        )
    )
    rates[9] = (algebraic[8] - states[9]) / algebraic[35]
    algebraic[9] = 1.00000 / \
        (1.00000 + np.exp(-(states[0] + 16.0000) / 9.50000))
    algebraic[36] = 46.0999 + 1685.76 / (
        (1.00000 + np.exp(-(states[0] + 40.8489) / 13.7802))
        * (1.00000 + np.exp((states[0] + 20.6372) / 15.1113))
    )
    rates[10] = (algebraic[9] - states[10]) / algebraic[36]
    algebraic[37] = 475.667 + 16321.6 / (
        (1.00000 + np.exp(-(states[0] + 41.8328) / 6.96673))
        * (1.00000 + np.exp((states[0] + 23.2432) / 21.2949))
    )
    rates[11] = (algebraic[9] - states[11]) / algebraic[37]
    algebraic[10] = 1.00000 / \
        (1.00000 + np.exp((states[0] + 48.0000) / 24.0000))
    algebraic[38] = (
        19.7864 /
        (1.00000 + np.power((states[0] + 20.7136) / 44.2868, 2.00000))
        - 0.378843
    )
    rates[12] = (algebraic[10] - states[12]) / algebraic[38]
    algebraic[11] = 1.00000 / \
        (1.00000 + np.exp(-(states[0] + 22.0000) / 12.4800))
    algebraic[39] = 395.300 / (
        1.00000 + np.power((states[0] + 38.1000) / 33.5900, 2.00000)
    )
    rates[13] = (algebraic[11] - states[13]) / algebraic[39]
    algebraic[40] = (
        5503.00
        + 5345.40 / (1.00000 + np.power(10.0000,
                     (-23.9000 - states[0]) * -0.0282700))
    ) - 4590.60 / (1.00000 + np.power(10.0000, (states[0] + 14.1500) * -0.0357000))
    rates[14] = (algebraic[11] - states[14]) / algebraic[40]
    algebraic[12] = 0.490000 + 0.510000 / (
        1.00000 + np.exp((states[0] + 1.08400) / 28.7800)
    )
    algebraic[41] = 5.44000 + 29.2000 / (
        1.00000 + np.power((states[0] + 48.0900) / 48.8300, 2.00000)
    )
    rates[15] = (algebraic[12] - states[15]) / algebraic[41]
    algebraic[14] = 1.00000 / \
        (1.00000 + np.exp(-(states[0] + 15.0400) / 16.9500))
    algebraic[42] = 10.0000 + 895.900 / (
        1.00000 + np.exp((-18.0100 - states[0]) / 31.0400)
    )
    rates[17] = (algebraic[14] - states[17]) / algebraic[42]
    algebraic[15] = 0.405800 / (
        1.00000 + np.exp((states[0] + 86.8400) / 15.0500)
    ) + 0.594200 / (1.00000 + np.exp((states[0] - 70.1300) / 13.3700))
    algebraic[43] = 1077.00 + 185845.0 / (
        1.00000 + np.power((states[0] - 39.4400) / 7.34400, 2.00000)
    )
    rates[18] = (algebraic[15] - states[18]) / algebraic[43]
    algebraic[44] = 37.5100 + 539.000 / (
        1.00000 + np.power((states[0] + 40.2400) / 17.7200, 2.00000)
    )
    rates[19] = (algebraic[16] - states[19]) / algebraic[44]
    algebraic[17] = 0.490000 + 0.510000 / (
        1.00000 + np.exp((states[0] + 1.08400) / 28.7800)
    )
    algebraic[45] = 5.44000 + 29.2000 / (
        1.00000 + np.power((states[0] + 48.0900) / 48.8300, 2.00000)
    )
    rates[21] = (algebraic[17] - states[21]) / algebraic[45]
    algebraic[18] = 0.405800 / (
        1.00000 + np.exp((states[0] + 86.8400) / 15.0500)
    ) + 0.594200 / (1.00000 + np.exp((states[0] - 70.1300) / 13.3700))
    algebraic[46] = 1077.00 + 185845.0 / (
        1.00000 + np.power((states[0] - 39.4400) / 7.34400, 2.00000)
    )
    rates[22] = (algebraic[18] - states[22]) / algebraic[46]
    algebraic[19] = 0.978613 / \
        (1.00000 + np.exp(-(states[0] + 18.6736) / 26.6606))
    algebraic[47] = 500.000 / (
        1.00000 + np.power((states[0] + 60.7100) / 15.7900, 2.00000)
    )
    rates[23] = (algebraic[19] - states[23]) / algebraic[47]
    algebraic[20] = 1.00000 / \
        (1.00000 + np.exp((states[0] + 63.0000) / 6.30000))
    algebraic[48] = 5000.00 / (
        1.00000 + np.power((states[0] + 62.7133) / 35.8611, 2.00000)
    )
    rates[24] = (algebraic[20] - states[24]) / algebraic[48]
    algebraic[49] = 30000.0 + 220000.0 / (
        1.00000 + np.exp((states[0] + 22.0000) / 4.00000)
    )
    rates[25] = (algebraic[20] - states[25]) / algebraic[49]
    algebraic[21] = 0.948000 / \
        (1.00000 + np.exp(-(states[0] + 17.9100) / 18.4000))
    algebraic[50] = 100.000 / (
        1.00000 + np.power((states[0] + 64.1000) / 28.6700, 2.00000)
    )
    rates[26] = (algebraic[21] - states[26]) / algebraic[50]
    algebraic[22] = 1.00000 / \
        (1.00000 + np.exp((states[0] + 21.2000) / 5.70000))
    algebraic[51] = 1.00000e06 * (
        1.00000
        - 1.00000
        / (
            (1.00000 + np.exp((states[0] - 315.000) / 50.0000))
            * (1.00000 + np.exp(-(states[0] + 74.9000) / 8.00000))
        )
    )
    rates[27] = (algebraic[22] - states[27]) / algebraic[51]
    algebraic[52] = 2.50000e06 * (
        1.00000
        - 1.00000
        / (
            (1.00000 + np.exp((states[0] - 132.868) / 25.3992))
            * (1.00000 + np.exp(-(states[0] + 24.9203) / 2.67915))
        )
    )
    rates[28] = (algebraic[22] - states[28]) / algebraic[52]
    algebraic[23] = 1.00000 / \
        (1.00000 + np.exp(-(states[0] + 27.7900) / 7.57000))
    algebraic[53] = 17.0000 / (
        1.00000 + np.power((states[0] + 20.5232) / 35.0000, 2.00000)
    )
    rates[29] = (algebraic[23] - states[29]) / algebraic[53]
    algebraic[24] = 0.0200000 + 0.980000 / (
        1.00000 + np.exp((states[0] + 69.5000) / 6.00000)
    )
    algebraic[54] = 7.50000 + 10.0000 / (
        1.00000 + np.power((states[0] + 34.1765) / 120.000, 2.00000)
    )
    rates[30] = (algebraic[24] - states[30]) / algebraic[54]
    algebraic[25] = -0.749234 / (
        1.00000 + np.power((states[1] * constants[6] -
                           0.0630535) / 0.161942, 2.00000)
    ) + 8.38384 / (
        1.00000 + np.power((states[1] * constants[6] +
                           1538.29) / 739.057, 2.00000)
    )
    algebraic[55] = (
        5011.47
        / (
            1.00000
            + np.power((states[1] * constants[6] +
                       0.237503) / 0.000239278, 0.422910)
        )
        - 37.5137
    )
    algebraic[59] = 1.00000 / (
        1.00000
        + np.exp(
            (-algebraic[25] * constants[72] * (states[0] - algebraic[55]))
            / (constants[71] * constants[74])
        )
    )
    algebraic[64] = 2.40914 / (
        1.00000 + np.power((states[0] - 158.779) / -52.1497, 2.00000)
    )
    rates[31] = (algebraic[59] - states[31]) / algebraic[64]
    algebraic[26] = -0.681249 / (
        1.00000 + np.power((states[1] * constants[7] -
                           0.218988) / 0.428335, 2.00000)
    ) + 1.40001 / (
        1.00000 + np.power((states[1] * constants[7] +
                           228.710) / 684.946, 2.00000)
    )
    algebraic[56] = (
        8540.23
        / (
            1.00000
            + np.power((states[1] * constants[7] +
                       0.401189) / 0.00399115, 0.668054)
        )
        - 109.275
    )
    algebraic[60] = 1.00000 / (
        1.00000
        + np.exp(
            (-algebraic[26] * constants[72] * (states[0] - algebraic[56]))
            / (constants[71] * constants[74])
        )
    )
    algebraic[65] = 13.8049 / (
        1.00000 + np.power((states[0] - 153.019) / 66.4952, 2.00000)
    )
    rates[32] = (algebraic[60] - states[32]) / algebraic[65]
    algebraic[27] = 1.00000 / \
        (1.00000 + np.exp((states[0] + 105.390) / 8.65530))
    algebraic[57] = 3.50000e-06 * np.exp(-0.0497000 * states[0])
    algebraic[61] = 0.0400300 * np.exp(0.0521100 * states[0])
    algebraic[66] = 1.00000 / (algebraic[57] + algebraic[61])
    rates[33] = (algebraic[27] - states[33]) / algebraic[66]
    algebraic[28] = (states[0] * constants[72]) / \
        (constants[71] * constants[74])
    algebraic[62] = 0.000600000 * np.exp(2.53000 * algebraic[28])
    algebraic[67] = 0.100000 * np.exp(-5.00000 * algebraic[28])
    algebraic[69] = 1.00000 / (
        1.00000
        + algebraic[67]
        * (
            np.power(algebraic[62] / states[1], 2.00000)
            + algebraic[62] / states[1]
            + 1.00000
        )
    )
    algebraic[71] = (
        -160.000
        + 210.000 / (1.00000 + np.exp((states[0] + 4.56000) / 11.6200))
        + 170.000 / (1.00000 + np.exp(-(states[0] + 25.5000) / 11.6200))
    )
    rates[34] = (algebraic[69] - states[34]) / algebraic[71]
    algebraic[0] = custom_piecewise(
        [
            np.less(voi, constants[0]),
            0.00000,
            np.less(voi - (constants[0] + constants[2]), 0.00000),
            constants[3],
            np.less(voi % constants[1] + constants[2], constants[2]),
            constants[3],
            True,
            0.00000,
        ]
    )
    algebraic[63] = (
        constants[16]
        * states[3]
        * states[3]
        * states[3]
        * states[4]
        * (states[0] - constants[77])
    )
    algebraic[68] = 1.00000 / \
        (1.00000 + np.power(states[1] / constants[19], 4.00000))
    algebraic[70] = (
        constants[17]
        * algebraic[68]
        * states[5]
        * states[5]
        * (0.800000 * states[6] + 0.200000 * states[7])
        * (states[0] - constants[18])
    )
    algebraic[72] = (
        constants[20] * states[8] * states[8] *
        states[9] * (states[0] - constants[21])
    )
    algebraic[73] = constants[23] * (states[0] - constants[78])
    algebraic[74] = (
        constants[32]
        * (0.800000 * states[10] + 0.200000 * states[11])
        * states[12]
        * (states[0] - constants[78])
    )
    algebraic[75] = (
        constants[29]
        * (0.300000 * states[13] + 0.700000 * states[14])
        * states[15]
        * states[16]
        * (states[0] - constants[78])
    )
    algebraic[76] = (
        constants[30] * states[17] * states[18] * (states[0] - constants[78])
    )
    algebraic[77] = (
        constants[31]
        * (0.200000 * states[19] + 0.800000 * states[20])
        * states[21]
        * states[22]
        * (states[0] - constants[78])
    )
    algebraic[78] = (
        constants[24]
        * states[23]
        * states[23]
        * (0.380000 * states[24] + 0.630000 * states[25])
        * (states[0] - constants[78])
    )
    algebraic[79] = (
        constants[25]
        * states[26]
        * states[26]
        * (0.750000 * states[27] + 0.250000 * states[28])
        * (states[0] - constants[78])
    )
    algebraic[80] = (
        constants[28] * states[29] * states[30] * (states[0] - constants[78])
    )
    algebraic[81] = (
        constants[22] * constants[26] *
        states[31] * (states[0] - constants[78])
    )
    algebraic[82] = (
        constants[22] * constants[27] *
        states[32] * (states[0] - constants[78])
    )
    algebraic[83] = constants[34] * states[33] * (states[0] - constants[83])
    algebraic[84] = constants[33] * states[34] * (states[0] - constants[79])
    algebraic[58] = ((constants[71] * constants[74]) / constants[72]) * np.log(
        (
            constants[36] * constants[63]
            + constants[37] * constants[64]
            + (4.00000 * constants[38] * constants[12])
            / (1.00000 + np.exp(algebraic[28]))
        )
        / (
            constants[36] * constants[11]
            + constants[37] * constants[59]
            + (4.00000 * constants[38] * states[1]) /
            (1.00000 + np.exp(algebraic[28]))
        )
    )
    algebraic[88] = (
        constants[60]
        * constants[67]
        * constants[41]
        * constants[35]
        * (states[0] - algebraic[58])
    )
    algebraic[85] = (
        constants[60]
        * constants[61]
        * constants[40]
        * constants[35]
        * (states[0] - algebraic[58])
    )
    algebraic[90] = (
        constants[60]
        * constants[65]
        * constants[42]
        * constants[35]
        * (states[0] - algebraic[58])
    )
    algebraic[91] = 1.00000 / (
        1.00000
        + 0.124500 * np.exp(-0.100000 * algebraic[28])
        + 0.00219000
        * np.exp(constants[64] / 49.7100)
        * np.exp(-1.90000 * algebraic[28])
    )
    algebraic[92] = constants[75] * \
        constants[87] * constants[88] * algebraic[91]
    algebraic[95] = 1.00000 / (
        1.00000 + np.power(constants[47] / states[1], constants[48])
    )
    algebraic[93] = np.exp((constants[86] - 1.00000) * algebraic[28])
    algebraic[94] = np.exp(constants[86] * algebraic[28])
    algebraic[96] = (np.power(constants[59], 3.00000)) * constants[12] * algebraic[
        94
    ] - (np.power(constants[64], 3.00000)) * states[1] * algebraic[93]
    algebraic[97] = 1.00000 + constants[85] * algebraic[93]
    algebraic[98] = (
        constants[52] * (np.power(constants[59], 3.00000))
        + (np.power(constants[51], 3.00000)) * states[1]
        + (np.power(constants[49], 3.00000))
        * constants[12]
        * (1.00000 + states[1] / constants[50])
    )
    algebraic[99] = (
        constants[12] * (np.power(constants[59], 3.00000))
        + (np.power(constants[64], 3.00000)) * states[1]
        + (np.power(constants[64], 3.00000))
        * constants[50]
        * (1.00000 + np.power(constants[59] / constants[49], 3.00000))
    )
    algebraic[100] = (constants[10] * constants[84] * algebraic[95] * algebraic[96]) / (
        algebraic[97] * (algebraic[98] + algebraic[99])
    )
    algebraic[101] = (
        (
            (0.500000 * constants[70] * constants[72])
            / (constants[69] * constants[73] * constants[68])
        )
        * constants[9]
        * algebraic[100]
    )
    algebraic[104] = (
        algebraic[63]
        + algebraic[83]
        + algebraic[101]
        + algebraic[92]
        + algebraic[70]
        + algebraic[72]
        + algebraic[84]
        + algebraic[74]
        + algebraic[75]
        + algebraic[76]
        + algebraic[77]
        + algebraic[78]
        + algebraic[79]
        + algebraic[80]
        + algebraic[81]
        + algebraic[82]
        + algebraic[88]
        + algebraic[90]
        + algebraic[85]
        + algebraic[73]
    )
    rates[0] = -(algebraic[104] + algebraic[0])
    algebraic[86] = algebraic[70] + algebraic[72] + algebraic[85]
    algebraic[87] = (
        (constants[69] * constants[73] * constants[68])
        / (constants[70] * constants[72])
    ) * algebraic[86]
    algebraic[102] = constants[44] / (
        1.00000 + np.power(constants[45] / states[1], constants[46])
    )
    algebraic[105] = algebraic[87] + algebraic[100] + algebraic[102]
    rates[1] = -algebraic[105]
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
    algebraic[6] = 1.00000 / \
        (1.00000 + np.exp((states[0] + 38.0000) / 7.00000))
    algebraic[13] = 0.340000 + 0.660000 / (
        1.00000 + np.exp((states[0] + 45.3000) / 12.3000)
    )
    algebraic[16] = 1.00000 / \
        (1.00000 + np.exp(-(states[0] + 36.5500) / 13.7600))
    algebraic[1] = 1.00000 / (
        1.00000 +
        np.power((constants[54] * constants[5]) / states[1], constants[55])
    )
    algebraic[29] = 4000.00 * (
        0.234845
        + (1.00000 - 0.234845)
        / (
            1.00000
            + np.power(states[1] / (constants[54] *
                       constants[5]), constants[55])
        )
    )
    algebraic[3] = 1.00000 / \
        (1.00000 + np.exp(-(states[0] + 35.9584) / 9.24013))
    algebraic[30] = 0.250000 + 7.00000 / (
        1.00000 + np.exp((states[0] + 38.0000) / 10.0000)
    )
    algebraic[4] = 1.00000 / \
        (1.00000 + np.exp((states[0] + 57.0000) / 8.00000))
    algebraic[31] = 0.900000 + 1002.85 / (
        1.00000 + np.power((states[0] + 47.5000) / 1.50000, 2.00000)
    )
    algebraic[5] = 1.00000 / \
        (1.00000 + np.exp(-(states[0] + 22.0000) / 7.00000))
    algebraic[32] = 2.29000 + 5.70000 / (
        1.00000 + np.power((states[0] + 29.9700) / 9.00000, 2.00000)
    )
    algebraic[33] = 90.9699 * (
        1.00000
        - 1.00000
        / (
            (1.00000 + np.exp((states[0] + 13.9629) / 45.3782))
            * (1.00000 + np.exp(-(states[0] + 9.49866) / 3.39450))
        )
    )
    algebraic[7] = 1.00000 / \
        (1.00000 + np.exp(-(states[0] + 54.2300) / 9.88000))
    algebraic[34] = 0.450000 + 3.90000 / (
        1.00000 + np.power((states[0] + 66.0000) / 26.0000, 2.00000)
    )
    algebraic[8] = 0.0200000 + 0.980000 / (
        1.00000 + np.exp((states[0] + 72.9780) / 4.64000)
    )
    algebraic[35] = 150.000 * (
        1.00000
        - 1.00000
        / (
            (1.00000 + np.exp((states[0] - 417.430) / 203.180))
            * (1.00000 + np.exp(-(states[0] + 61.1100) / 8.07000))
        )
    )
    algebraic[9] = 1.00000 / \
        (1.00000 + np.exp(-(states[0] + 16.0000) / 9.50000))
    algebraic[36] = 46.0999 + 1685.76 / (
        (1.00000 + np.exp(-(states[0] + 40.8489) / 13.7802))
        * (1.00000 + np.exp((states[0] + 20.6372) / 15.1113))
    )
    algebraic[37] = 475.667 + 16321.6 / (
        (1.00000 + np.exp(-(states[0] + 41.8328) / 6.96673))
        * (1.00000 + np.exp((states[0] + 23.2432) / 21.2949))
    )
    algebraic[10] = 1.00000 / \
        (1.00000 + np.exp((states[0] + 48.0000) / 24.0000))
    algebraic[38] = (
        19.7864 /
        (1.00000 + np.power((states[0] + 20.7136) / 44.2868, 2.00000))
        - 0.378843
    )
    algebraic[11] = 1.00000 / \
        (1.00000 + np.exp(-(states[0] + 22.0000) / 12.4800))
    algebraic[39] = 395.300 / (
        1.00000 + np.power((states[0] + 38.1000) / 33.5900, 2.00000)
    )
    algebraic[40] = (
        5503.00
        + 5345.40 / (1.00000 + np.power(10.0000,
                     (-23.9000 - states[0]) * -0.0282700))
    ) - 4590.60 / (1.00000 + np.power(10.0000, (states[0] + 14.1500) * -0.0357000))
    algebraic[12] = 0.490000 + 0.510000 / (
        1.00000 + np.exp((states[0] + 1.08400) / 28.7800)
    )
    algebraic[41] = 5.44000 + 29.2000 / (
        1.00000 + np.power((states[0] + 48.0900) / 48.8300, 2.00000)
    )
    algebraic[14] = 1.00000 / \
        (1.00000 + np.exp(-(states[0] + 15.0400) / 16.9500))
    algebraic[42] = 10.0000 + 895.900 / (
        1.00000 + np.exp((-18.0100 - states[0]) / 31.0400)
    )
    algebraic[15] = 0.405800 / (
        1.00000 + np.exp((states[0] + 86.8400) / 15.0500)
    ) + 0.594200 / (1.00000 + np.exp((states[0] - 70.1300) / 13.3700))
    algebraic[43] = 1077.00 + 185845.0 / (
        1.00000 + np.power((states[0] - 39.4400) / 7.34400, 2.00000)
    )
    algebraic[44] = 37.5100 + 539.000 / (
        1.00000 + np.power((states[0] + 40.2400) / 17.7200, 2.00000)
    )
    algebraic[17] = 0.490000 + 0.510000 / (
        1.00000 + np.exp((states[0] + 1.08400) / 28.7800)
    )
    algebraic[45] = 5.44000 + 29.2000 / (
        1.00000 + np.power((states[0] + 48.0900) / 48.8300, 2.00000)
    )
    algebraic[18] = 0.405800 / (
        1.00000 + np.exp((states[0] + 86.8400) / 15.0500)
    ) + 0.594200 / (1.00000 + np.exp((states[0] - 70.1300) / 13.3700))
    algebraic[46] = 1077.00 + 185845.0 / (
        1.00000 + np.power((states[0] - 39.4400) / 7.34400, 2.00000)
    )
    algebraic[19] = 0.978613 / \
        (1.00000 + np.exp(-(states[0] + 18.6736) / 26.6606))
    algebraic[47] = 500.000 / (
        1.00000 + np.power((states[0] + 60.7100) / 15.7900, 2.00000)
    )
    algebraic[20] = 1.00000 / \
        (1.00000 + np.exp((states[0] + 63.0000) / 6.30000))
    algebraic[48] = 5000.00 / (
        1.00000 + np.power((states[0] + 62.7133) / 35.8611, 2.00000)
    )
    algebraic[49] = 30000.0 + 220000.0 / (
        1.00000 + np.exp((states[0] + 22.0000) / 4.00000)
    )
    algebraic[21] = 0.948000 / \
        (1.00000 + np.exp(-(states[0] + 17.9100) / 18.4000))
    algebraic[50] = 100.000 / (
        1.00000 + np.power((states[0] + 64.1000) / 28.6700, 2.00000)
    )
    algebraic[22] = 1.00000 / \
        (1.00000 + np.exp((states[0] + 21.2000) / 5.70000))
    algebraic[51] = 1.00000e06 * (
        1.00000
        - 1.00000
        / (
            (1.00000 + np.exp((states[0] - 315.000) / 50.0000))
            * (1.00000 + np.exp(-(states[0] + 74.9000) / 8.00000))
        )
    )
    algebraic[52] = 2.50000e06 * (
        1.00000
        - 1.00000
        / (
            (1.00000 + np.exp((states[0] - 132.868) / 25.3992))
            * (1.00000 + np.exp(-(states[0] + 24.9203) / 2.67915))
        )
    )
    algebraic[23] = 1.00000 / \
        (1.00000 + np.exp(-(states[0] + 27.7900) / 7.57000))
    algebraic[53] = 17.0000 / (
        1.00000 + np.power((states[0] + 20.5232) / 35.0000, 2.00000)
    )
    algebraic[24] = 0.0200000 + 0.980000 / (
        1.00000 + np.exp((states[0] + 69.5000) / 6.00000)
    )
    algebraic[54] = 7.50000 + 10.0000 / (
        1.00000 + np.power((states[0] + 34.1765) / 120.000, 2.00000)
    )
    algebraic[25] = -0.749234 / (
        1.00000 + np.power((states[1] * constants[6] -
                           0.0630535) / 0.161942, 2.00000)
    ) + 8.38384 / (
        1.00000 + np.power((states[1] * constants[6] +
                           1538.29) / 739.057, 2.00000)
    )
    algebraic[55] = (
        5011.47
        / (
            1.00000
            + np.power((states[1] * constants[6] +
                       0.237503) / 0.000239278, 0.422910)
        )
        - 37.5137
    )
    algebraic[59] = 1.00000 / (
        1.00000
        + np.exp(
            (-algebraic[25] * constants[72] * (states[0] - algebraic[55]))
            / (constants[71] * constants[74])
        )
    )
    algebraic[64] = 2.40914 / (
        1.00000 + np.power((states[0] - 158.779) / -52.1497, 2.00000)
    )
    algebraic[26] = -0.681249 / (
        1.00000 + np.power((states[1] * constants[7] -
                           0.218988) / 0.428335, 2.00000)
    ) + 1.40001 / (
        1.00000 + np.power((states[1] * constants[7] +
                           228.710) / 684.946, 2.00000)
    )
    algebraic[56] = (
        8540.23
        / (
            1.00000
            + np.power((states[1] * constants[7] +
                       0.401189) / 0.00399115, 0.668054)
        )
        - 109.275
    )
    algebraic[60] = 1.00000 / (
        1.00000
        + np.exp(
            (-algebraic[26] * constants[72] * (states[0] - algebraic[56]))
            / (constants[71] * constants[74])
        )
    )
    algebraic[65] = 13.8049 / (
        1.00000 + np.power((states[0] - 153.019) / 66.4952, 2.00000)
    )
    algebraic[27] = 1.00000 / \
        (1.00000 + np.exp((states[0] + 105.390) / 8.65530))
    algebraic[57] = 3.50000e-06 * np.exp(-0.0497000 * states[0])
    algebraic[61] = 0.0400300 * np.exp(0.0521100 * states[0])
    algebraic[66] = 1.00000 / (algebraic[57] + algebraic[61])
    algebraic[28] = (states[0] * constants[72]) / \
        (constants[71] * constants[74])
    algebraic[62] = 0.000600000 * np.exp(2.53000 * algebraic[28])
    algebraic[67] = 0.100000 * np.exp(-5.00000 * algebraic[28])
    algebraic[69] = 1.00000 / (
        1.00000
        + algebraic[67]
        * (
            np.power(algebraic[62] / states[1], 2.00000)
            + algebraic[62] / states[1]
            + 1.00000
        )
    )
    algebraic[71] = (
        -160.000
        + 210.000 / (1.00000 + np.exp((states[0] + 4.56000) / 11.6200))
        + 170.000 / (1.00000 + np.exp(-(states[0] + 25.5000) / 11.6200))
    )
    algebraic[0] = custom_piecewise(
        [
            np.less(voi, constants[0]),
            0.00000,
            np.less(voi - (constants[0] + constants[2]), 0.00000),
            constants[3],
            np.less(voi % constants[1] + constants[2], constants[2]),
            constants[3],
            True,
            0.00000,
        ]
    )
    algebraic[63] = (
        constants[16]
        * states[3]
        * states[3]
        * states[3]
        * states[4]
        * (states[0] - constants[77])
    )
    algebraic[68] = 1.00000 / \
        (1.00000 + np.power(states[1] / constants[19], 4.00000))
    algebraic[70] = (
        constants[17]
        * algebraic[68]
        * states[5]
        * states[5]
        * (0.800000 * states[6] + 0.200000 * states[7])
        * (states[0] - constants[18])
    )
    algebraic[72] = (
        constants[20] * states[8] * states[8] *
        states[9] * (states[0] - constants[21])
    )
    algebraic[73] = constants[23] * (states[0] - constants[78])
    algebraic[74] = (
        constants[32]
        * (0.800000 * states[10] + 0.200000 * states[11])
        * states[12]
        * (states[0] - constants[78])
    )
    algebraic[75] = (
        constants[29]
        * (0.300000 * states[13] + 0.700000 * states[14])
        * states[15]
        * states[16]
        * (states[0] - constants[78])
    )
    algebraic[76] = (
        constants[30] * states[17] * states[18] * (states[0] - constants[78])
    )
    algebraic[77] = (
        constants[31]
        * (0.200000 * states[19] + 0.800000 * states[20])
        * states[21]
        * states[22]
        * (states[0] - constants[78])
    )
    algebraic[78] = (
        constants[24]
        * states[23]
        * states[23]
        * (0.380000 * states[24] + 0.630000 * states[25])
        * (states[0] - constants[78])
    )
    algebraic[79] = (
        constants[25]
        * states[26]
        * states[26]
        * (0.750000 * states[27] + 0.250000 * states[28])
        * (states[0] - constants[78])
    )
    algebraic[80] = (
        constants[28] * states[29] * states[30] * (states[0] - constants[78])
    )
    algebraic[81] = (
        constants[22] * constants[26] *
        states[31] * (states[0] - constants[78])
    )
    algebraic[82] = (
        constants[22] * constants[27] *
        states[32] * (states[0] - constants[78])
    )
    algebraic[83] = constants[34] * states[33] * (states[0] - constants[83])
    algebraic[84] = constants[33] * states[34] * (states[0] - constants[79])
    algebraic[58] = ((constants[71] * constants[74]) / constants[72]) * np.log(
        (
            constants[36] * constants[63]
            + constants[37] * constants[64]
            + (4.00000 * constants[38] * constants[12])
            / (1.00000 + np.exp(algebraic[28]))
        )
        / (
            constants[36] * constants[11]
            + constants[37] * constants[59]
            + (4.00000 * constants[38] * states[1]) /
            (1.00000 + np.exp(algebraic[28]))
        )
    )
    algebraic[88] = (
        constants[60]
        * constants[67]
        * constants[41]
        * constants[35]
        * (states[0] - algebraic[58])
    )
    algebraic[85] = (
        constants[60]
        * constants[61]
        * constants[40]
        * constants[35]
        * (states[0] - algebraic[58])
    )
    algebraic[90] = (
        constants[60]
        * constants[65]
        * constants[42]
        * constants[35]
        * (states[0] - algebraic[58])
    )
    algebraic[91] = 1.00000 / (
        1.00000
        + 0.124500 * np.exp(-0.100000 * algebraic[28])
        + 0.00219000
        * np.exp(constants[64] / 49.7100)
        * np.exp(-1.90000 * algebraic[28])
    )
    algebraic[92] = constants[75] * \
        constants[87] * constants[88] * algebraic[91]
    algebraic[95] = 1.00000 / (
        1.00000 + np.power(constants[47] / states[1], constants[48])
    )
    algebraic[93] = np.exp((constants[86] - 1.00000) * algebraic[28])
    algebraic[94] = np.exp(constants[86] * algebraic[28])
    algebraic[96] = (np.power(constants[59], 3.00000)) * constants[12] * algebraic[
        94
    ] - (np.power(constants[64], 3.00000)) * states[1] * algebraic[93]
    algebraic[97] = 1.00000 + constants[85] * algebraic[93]
    algebraic[98] = (
        constants[52] * (np.power(constants[59], 3.00000))
        + (np.power(constants[51], 3.00000)) * states[1]
        + (np.power(constants[49], 3.00000))
        * constants[12]
        * (1.00000 + states[1] / constants[50])
    )
    algebraic[99] = (
        constants[12] * (np.power(constants[59], 3.00000))
        + (np.power(constants[64], 3.00000)) * states[1]
        + (np.power(constants[64], 3.00000))
        * constants[50]
        * (1.00000 + np.power(constants[59] / constants[49], 3.00000))
    )
    algebraic[100] = (constants[10] * constants[84] * algebraic[95] * algebraic[96]) / (
        algebraic[97] * (algebraic[98] + algebraic[99])
    )
    algebraic[101] = (
        (
            (0.500000 * constants[70] * constants[72])
            / (constants[69] * constants[73] * constants[68])
        )
        * constants[9]
        * algebraic[100]
    )
    algebraic[104] = (
        algebraic[63]
        + algebraic[83]
        + algebraic[101]
        + algebraic[92]
        + algebraic[70]
        + algebraic[72]
        + algebraic[84]
        + algebraic[74]
        + algebraic[75]
        + algebraic[76]
        + algebraic[77]
        + algebraic[78]
        + algebraic[79]
        + algebraic[80]
        + algebraic[81]
        + algebraic[82]
        + algebraic[88]
        + algebraic[90]
        + algebraic[85]
        + algebraic[73]
    )
    algebraic[86] = algebraic[70] + algebraic[72] + algebraic[85]
    algebraic[87] = (
        (constants[69] * constants[73] * constants[68])
        / (constants[70] * constants[72])
    ) * algebraic[86]
    algebraic[102] = constants[44] / (
        1.00000 + np.power(constants[45] / states[1], constants[46])
    )
    algebraic[105] = algebraic[87] + algebraic[100] + algebraic[102]
    algebraic[2] = constants[53] * (states[2] - 0.234500)
    algebraic[89] = algebraic[87] * constants[4]
    algebraic[103] = algebraic[100] * constants[4]
    algebraic[106] = algebraic[102] * constants[4]
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
