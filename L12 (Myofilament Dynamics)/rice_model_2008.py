# Gotran generated code for the  "rice_model_2008" model
from __future__ import division

def init_state_values(**values):
    """
    Initialize state values
    """
    # Imports
    import numpy as np
    from modelparameters.utils import Range

    init_values = np.array([1.89999811516, -4.51134525104e-06,\
        0.130660965615, 0.0147730085064, 0.99999783454, 0.999999959256,\
        4.07437173989e-08, 1.81017564384e-06, 3.049496488e-07,\
        0.00700005394874, 3.41212828972e-08], dtype=np.float_)

    # State indices and limit checker
    state_ind = dict([("SL",(0, Range())), ("intf",(1, Range())),\
        ("TRPNCaH",(2, Range())), ("TRPNCaL",(3, Range())), ("N",(4,\
        Range())), ("N_NoXB",(5, Range())), ("P_NoXB",(6, Range())),\
        ("XBpostr",(7, Range())), ("XBprer",(8, Range())), ("xXBpostr",(9,\
        Range())), ("xXBprer",(10, Range()))])

    for state_name, value in values.items():
        if state_name not in state_ind:
            raise ValueError("{0} is not a state.".format(state_name))
        ind, range = state_ind[state_name]
        if value not in range:
            raise ValueError("While setting '{0}' {1}".format(state_name,\
                range.format_not_in(value)))

        # Assign value
        init_values[ind] = value

    return init_values

def init_parameter_values(**values):
    """
    Initialize parameter values
    """
    # Imports
    import numpy as np
    from modelparameters.utils import Range

    # Param values
    # Qfapp=6.25, Qgapp=2.5, Qgxb=6.25, Qhb=6.25, Qhf=6.25, fapp=0.5,
    # gapp=0.07, gslmod=6, gxb=0.07, hb=0.4, hbmdc=0, hf=2,
    # hfmdc=5, sigman=1, sigmap=8, xbmodsp=1, KSE=1, PCon_c=0.02,
    # PCon_t=0.002, PExp_c=70, PExp_t=10, SEon=1, SL_c=2.25,
    # SLmax=2.4, SLmin=1.4, SLrest=1.85, SLset=1.9, fixed_afterload=0,
    # kxb_normalised=120, massf=50, visc=3, Ca_amplitude=1.45,
    # Ca_diastolic=0.09, start_time=5, tau1=20, tau2=110, TmpC=24,
    # len_hbare=0.1, len_thick=1.65, len_thin=1.2, x_0=0.007,
    # Qkn_p=1.6, Qkoff=1.3, Qkon=1.5, Qkp_n=1.6, kn_p=0.5,
    # koffH=0.025, koffL=0.25, koffmod=1, kon=0.05, kp_n=0.05,
    # nperm=15, perm50=0.5, xPsi=2, Trop_conc=70, kxb=120
    init_values = np.array([6.25, 2.5, 6.25, 6.25, 6.25, 0.5, 0.07, 6, 0.07,\
        0.4, 0, 2, 5, 1, 8, 1, 1, 0.02, 0.002, 70, 10, 1, 2.25, 2.4, 1.4,\
        1.85, 1.9, 0, 120, 50, 3, 1.45, 0.09, 5, 20, 110, 24, 0.1, 1.65, 1.2,\
        0.007, 1.6, 1.3, 1.5, 1.6, 0.5, 0.025, 0.25, 1, 0.05, 0.05, 15, 0.5,\
        2, 70, 120], dtype=np.float_)

    # Parameter indices and limit checker
    param_ind = dict([("Qfapp", (0, Range())), ("Qgapp", (1, Range())),\
        ("Qgxb", (2, Range())), ("Qhb", (3, Range())), ("Qhf", (4, Range())),\
        ("fapp", (5, Range())), ("gapp", (6, Range())), ("gslmod", (7,\
        Range())), ("gxb", (8, Range())), ("hb", (9, Range())), ("hbmdc",\
        (10, Range())), ("hf", (11, Range())), ("hfmdc", (12, Range())),\
        ("sigman", (13, Range())), ("sigmap", (14, Range())), ("xbmodsp",\
        (15, Range())), ("KSE", (16, Range())), ("PCon_c", (17, Range())),\
        ("PCon_t", (18, Range())), ("PExp_c", (19, Range())), ("PExp_t", (20,\
        Range())), ("SEon", (21, Range())), ("SL_c", (22, Range())),\
        ("SLmax", (23, Range())), ("SLmin", (24, Range())), ("SLrest", (25,\
        Range())), ("SLset", (26, Range())), ("fixed_afterload", (27,\
        Range())), ("kxb_normalised", (28, Range())), ("massf", (29,\
        Range())), ("visc", (30, Range())), ("Ca_amplitude", (31, Range())),\
        ("Ca_diastolic", (32, Range())), ("start_time", (33, Range())),\
        ("tau1", (34, Range())), ("tau2", (35, Range())), ("TmpC", (36,\
        Range())), ("len_hbare", (37, Range())), ("len_thick", (38,\
        Range())), ("len_thin", (39, Range())), ("x_0", (40, Range())),\
        ("Qkn_p", (41, Range())), ("Qkoff", (42, Range())), ("Qkon", (43,\
        Range())), ("Qkp_n", (44, Range())), ("kn_p", (45, Range())),\
        ("koffH", (46, Range())), ("koffL", (47, Range())), ("koffmod", (48,\
        Range())), ("kon", (49, Range())), ("kp_n", (50, Range())), ("nperm",\
        (51, Range())), ("perm50", (52, Range())), ("xPsi", (53, Range())),\
        ("Trop_conc", (54, Range())), ("kxb", (55, Range()))])

    for param_name, value in values.items():
        if param_name not in param_ind:
            raise ValueError("{0} is not a parameter.".format(param_name))
        ind, range = param_ind[param_name]
        if value not in range:
            raise ValueError("While setting '{0}' {1}".format(param_name,\
                range.format_not_in(value)))

        # Assign value
        init_values[ind] = value

    return init_values

def state_indices(*states):
    """
    State indices
    """
    state_inds = dict([("SL", 0), ("intf", 1), ("TRPNCaH", 2), ("TRPNCaL",\
        3), ("N", 4), ("N_NoXB", 5), ("P_NoXB", 6), ("XBpostr", 7),\
        ("XBprer", 8), ("xXBpostr", 9), ("xXBprer", 10)])

    indices = []
    for state in states:
        if state not in state_inds:
            raise ValueError("Unknown state: '{0}'".format(state))
        indices.append(state_inds[state])
    if len(indices)>1:
        return indices
    else:
        return indices[0]

def parameter_indices(**params):
    """
    Parameter indices
    """
    param_inds = dict(("Qfapp", 0), ("Qgapp", 1), ("Qgxb", 2), ("Qhb", 3),\
        ("Qhf", 4), ("fapp", 5), ("gapp", 6), ("gslmod", 7), ("gxb", 8),\
        ("hb", 9), ("hbmdc", 10), ("hf", 11), ("hfmdc", 12), ("sigman", 13),\
        ("sigmap", 14), ("xbmodsp", 15), ("KSE", 16), ("PCon_c", 17),\
        ("PCon_t", 18), ("PExp_c", 19), ("PExp_t", 20), ("SEon", 21),\
        ("SL_c", 22), ("SLmax", 23), ("SLmin", 24), ("SLrest", 25), ("SLset",\
        26), ("fixed_afterload", 27), ("kxb_normalised", 28), ("massf", 29),\
        ("visc", 30), ("Ca_amplitude", 31), ("Ca_diastolic", 32),\
        ("start_time", 33), ("tau1", 34), ("tau2", 35), ("TmpC", 36),\
        ("len_hbare", 37), ("len_thick", 38), ("len_thin", 39), ("x_0", 40),\
        ("Qkn_p", 41), ("Qkoff", 42), ("Qkon", 43), ("Qkp_n", 44), ("kn_p",\
        45), ("koffH", 46), ("koffL", 47), ("koffmod", 48), ("kon", 49),\
        ("kp_n", 50), ("nperm", 51), ("perm50", 52), ("xPsi", 53),\
        ("Trop_conc", 54), ("kxb", 55))

    indices = []
    for param in params:
        if param not in param_inds:
            raise ValueError("Unknown param: '{0}'".format(param))
        indices.append(param_inds[param])
    if len(indices)>1:
        return indices
    else:
        return indices[0]

def monitor_indices(*monitored):
    """
    Monitor indices
    """
    monitor_inds = dict([("fappT", 0), ("gapslmd", 1), ("gappT", 2), ("hfmd",\
        3), ("hbmd", 4), ("hfT", 5), ("hbT", 6), ("gxbmd", 7), ("gxbT", 8),\
        ("SSXBprer", 9), ("SSXBpostr", 10), ("Fnordv", 11), ("force", 12),\
        ("active", 13), ("ppforce_t", 14), ("ppforce_c", 15), ("ppforce",\
        16), ("preload", 17), ("afterload", 18), ("dSL", 19), ("beta", 20),\
        ("Cai", 21), ("konT", 22), ("koffLT", 23), ("koffHT", 24),\
        ("dTRPNCaL", 25), ("dTRPNCaH", 26), ("Tropreg", 27), ("permtot", 28),\
        ("inprmt", 29), ("kn_pT", 30), ("kp_nT", 31), ("dXBpostr", 32), ("P",\
        33), ("dXBprer", 34), ("dutyprer", 35), ("dutypostr", 36),\
        ("dxXBprer", 37), ("dxXBpostr", 38), ("FrSBXB", 39), ("dFrSBXB", 40),\
        ("dsovr_ze", 41), ("dsovr_cle", 42), ("dlen_sovr", 43), ("dSOVFThin",\
        44), ("dSOVFThick", 45), ("TropTot", 46), ("dTropTot", 47),\
        ("dforce", 48), ("sovr_ze", 49), ("sovr_cle", 50), ("len_sovr", 51),\
        ("SOVFThick", 52), ("SOVFThin", 53), ("dSL_dt", 54), ("dintf_dt",\
        55), ("dTRPNCaH_dt", 56), ("dTRPNCaL_dt", 57), ("dN_dt", 58),\
        ("dN_NoXB_dt", 59), ("dP_NoXB_dt", 60), ("dXBpostr_dt", 61),\
        ("dXBprer_dt", 62), ("dxXBpostr_dt", 63), ("dxXBprer_dt", 64)])

    indices = []
    for monitor in monitored:
        if monitor not in monitor_inds:
            raise ValueError("Unknown monitored: '{0}'".format(monitor))
        indices.append(monitor_inds[monitor])
    if len(indices)>1:
        return indices
    else:
        return indices[0]

def rhs(states, t, parameters, values=None):
    """
    Compute the right hand side of the rice_model_2008 ODE
    """
    # Imports
    import numpy as np
    import math

    # Assign states
    assert(len(states) == 11)
    SL, intf, TRPNCaH, TRPNCaL, N, N_NoXB, P_NoXB, XBpostr, XBprer, xXBpostr,\
        xXBprer = states

    # Assign parameters
    assert(len(parameters) == 56)
    Qfapp=parameters[0]; Qgapp=parameters[1]; Qgxb=parameters[2];\
        Qhb=parameters[3]; Qhf=parameters[4]; fapp=parameters[5];\
        gapp=parameters[6]; gslmod=parameters[7]; gxb=parameters[8];\
        hb=parameters[9]; hbmdc=parameters[10]; hf=parameters[11];\
        hfmdc=parameters[12]; sigman=parameters[13]; sigmap=parameters[14];\
        xbmodsp=parameters[15]; KSE=parameters[16]; PCon_c=parameters[17];\
        PCon_t=parameters[18]; PExp_c=parameters[19]; PExp_t=parameters[20];\
        SEon=parameters[21]; SL_c=parameters[22]; SLmax=parameters[23];\
        SLmin=parameters[24]; SLrest=parameters[25]; SLset=parameters[26];\
        fixed_afterload=parameters[27]; kxb_normalised=parameters[28];\
        massf=parameters[29]; visc=parameters[30];\
        Ca_amplitude=parameters[31]; Ca_diastolic=parameters[32];\
        start_time=parameters[33]; tau1=parameters[34]; tau2=parameters[35];\
        TmpC=parameters[36]; len_hbare=parameters[37];\
        len_thick=parameters[38]; len_thin=parameters[39];\
        x_0=parameters[40]; Qkn_p=parameters[41]; Qkoff=parameters[42];\
        Qkon=parameters[43]; Qkp_n=parameters[44]; kn_p=parameters[45];\
        koffH=parameters[46]; koffL=parameters[47]; koffmod=parameters[48];\
        kon=parameters[49]; kp_n=parameters[50]; nperm=parameters[51];\
        perm50=parameters[52]; xPsi=parameters[53]

    # Init return args
    if values is None:
        values = np.zeros((11,), dtype=np.float_)
    else:
        assert isinstance(values, np.ndarray) and values.shape == (11,)

    # Expressions for the Sarcomere geometry component
    sovr_ze = (len_thick/2 if len_thick/2 < SL/2 else SL/2)
    sovr_cle = (-SL/2 + len_thin if -SL/2 + len_thin > len_hbare/2 else\
        len_hbare/2)
    len_sovr = -sovr_cle + sovr_ze
    SOVFThick = 2*len_sovr/(-len_hbare + len_thick)
    SOVFThin = len_sovr/len_thin

    # Expressions for the Thin filament regulation and crossbridge cycling
    # rates component
    fappT = fapp*xbmodsp*math.pow(Qfapp, -37/10 + TmpC/10)
    gapslmd = 1 + gslmod*(1 - SOVFThick)
    gappT = gapp*xbmodsp*math.pow(Qgapp, -37/10 + TmpC/10)*gapslmd
    hfmd = math.exp(-hfmdc*(xXBprer*xXBprer)*math.copysign(1.0,\
        xXBprer)/(x_0*x_0))
    hbmd = math.exp(hbmdc*((xXBpostr - x_0)*(xXBpostr -\
        x_0))*math.copysign(1.0, xXBpostr - x_0)/(x_0*x_0))
    hfT = hf*xbmodsp*math.pow(Qhf, -37/10 + TmpC/10)*hfmd
    hbT = hb*xbmodsp*math.pow(Qhb, -37/10 + TmpC/10)*hbmd
    gxbmd = (math.exp(sigmap*((-xXBpostr + x_0)*(-xXBpostr + x_0))/(x_0*x_0))\
        if xXBpostr < x_0 else math.exp(sigman*((xXBpostr - x_0)*(xXBpostr -\
        x_0))/(x_0*x_0)))
    gxbT = gxb*xbmodsp*math.pow(Qgxb, -37/10 + TmpC/10)*gxbmd

    # Expressions for the Normalised active and passive force component
    SSXBpostr = fapp*hf/(gapp*hb + gapp*gxb + fapp*hb + gxb*hf + fapp*gxb +\
        fapp*hf)
    Fnordv = kxb_normalised*x_0*SSXBpostr
    force = kxb_normalised*(XBprer*xXBprer + XBpostr*xXBpostr)*SOVFThick
    active = force/Fnordv
    ppforce_t = PCon_t*(-1 + math.exp(PExp_t*math.fabs(-SLrest +\
        SL)))*math.copysign(1.0, -SLrest + SL)
    ppforce_c = (PCon_c*(-1 + math.exp(PExp_c*math.fabs(-SL_c + SL))) if SL >\
        SL_c else 0)
    ppforce = ppforce_t + ppforce_c
    preload = PCon_t*(-1 + math.exp(PExp_t*math.fabs(-SLrest +\
        SLset)))*math.copysign(1.0, -SLrest + SLset)
    afterload = (KSE*(SLset - SL) if SEon == 1 else fixed_afterload)
    dSL = ((visc*(SLset - SL) + intf)/massf if SL > SLmin and SL <= SLmax\
        else 0)
    values[1] = -active + afterload - ppforce + preload
    values[0] = dSL

    # Expressions for the Equation for simulated calcium transient component
    beta = -math.pow(tau1/tau2, -1/(1 - tau2/tau1)) + math.pow(tau1/tau2,\
        -1/(-1 + tau1/tau2))
    Cai = ((-Ca_diastolic + Ca_amplitude)*(math.exp((start_time - t)/tau1) -\
        math.exp((start_time - t)/tau2))/beta + Ca_diastolic if t >\
        start_time else Ca_diastolic)

    # Expressions for the Ca binding to troponin to thin filament regulation
    # component
    konT = kon*math.pow(Qkon, -37/10 + TmpC/10)
    koffLT = koffL*koffmod*math.pow(Qkoff, -37/10 + TmpC/10)
    koffHT = koffH*koffmod*math.pow(Qkoff, -37/10 + TmpC/10)
    dTRPNCaL = (1 - TRPNCaL)*Cai*konT - TRPNCaL*koffLT
    dTRPNCaH = (1 - TRPNCaH)*Cai*konT - TRPNCaH*koffHT
    Tropreg = (1 - SOVFThin)*TRPNCaL + SOVFThin*TRPNCaH
    permtot = math.sqrt(math.fabs(1.0/(1 + math.pow(perm50/Tropreg, nperm))))
    inprmt = (1.0/permtot if 1.0/permtot < 100 else 100)
    values[3] = dTRPNCaL
    values[2] = dTRPNCaH
    kn_pT = kn_p*math.pow(Qkn_p, -37/10 + TmpC/10)*permtot
    kp_nT = kp_n*math.pow(Qkp_n, -37/10 + TmpC/10)*inprmt

    # Expressions for the Regulation and crossbridge cycling state equations
    # component
    values[5] = P_NoXB*kp_nT - N_NoXB*kn_pT
    values[6] = N_NoXB*kn_pT - P_NoXB*kp_nT
    dXBpostr = -XBpostr*gxbT + XBprer*hfT - XBpostr*hbT
    P = 1 - XBprer - XBpostr - N
    values[4] = -N*kn_pT + P*kp_nT
    dXBprer = -XBprer*hfT + XBpostr*hbT - XBprer*gappT + P*fappT
    values[7] = dXBpostr
    values[8] = dXBprer

    # Expressions for the Mean strain of strongly bound states component
    dutyprer = (fappT*gxbT + fappT*hbT)/(fappT*gxbT + fappT*hbT + fappT*hfT +\
        gappT*gxbT + gappT*hbT + gxbT*hfT)
    dutypostr = fappT*hfT/(fappT*gxbT + fappT*hbT + fappT*hfT + gappT*gxbT +\
        gappT*hbT + gxbT*hfT)
    dxXBprer = dSL/2 + xPsi*((-xXBprer + xXBpostr - x_0)*hbT -\
        fappT*xXBprer)/dutyprer
    dxXBpostr = dSL/2 + xPsi*(-xXBpostr + xXBprer + x_0)*hfT/dutypostr
    values[10] = dxXBprer
    values[9] = dxXBpostr

    # Return results
    return values

def monitor(states, t, parameters, monitored=None):
    """
    Computes monitored expressions of the rice_model_2008 ODE
    """
    # Imports
    import numpy as np
    import math

    # Assign states
    assert(len(states) == 11)
    SL, intf, TRPNCaH, TRPNCaL, N, N_NoXB, P_NoXB, XBpostr, XBprer, xXBpostr,\
        xXBprer = states

    # Assign parameters
    assert(len(parameters) == 56)
    Qfapp, Qgapp, Qgxb, Qhb, Qhf, fapp, gapp, gslmod, gxb, hb, hbmdc, hf,\
        hfmdc, sigman, sigmap, xbmodsp, KSE, PCon_c, PCon_t, PExp_c, PExp_t,\
        SEon, SL_c, SLmax, SLmin, SLrest, SLset, fixed_afterload,\
        kxb_normalised, massf, visc, Ca_amplitude, Ca_diastolic, start_time,\
        tau1, tau2, TmpC, len_hbare, len_thick, len_thin, x_0, Qkn_p, Qkoff,\
        Qkon, Qkp_n, kn_p, koffH, koffL, koffmod, kon, kp_n, nperm, perm50,\
        xPsi, Trop_conc, kxb = parameters

    # Init return args
    if monitored is None:
        monitored = np.zeros((65,), dtype=np.float_)
    else:
        assert isinstance(monitored, np.ndarray) and monitored.shape == (65,)

    # Expressions for the Sarcomere geometry component
    monitored[49] = (len_thick/2 if len_thick/2 < SL/2 else SL/2)
    monitored[50] = (-SL/2 + len_thin if -SL/2 + len_thin > len_hbare/2 else\
        len_hbare/2)
    monitored[51] = monitored[49] - monitored[50]
    monitored[52] = 2*monitored[51]/(-len_hbare + len_thick)
    monitored[53] = monitored[51]/len_thin

    # Expressions for the Thin filament regulation and crossbridge cycling
    # rates component
    monitored[0] = fapp*xbmodsp*math.pow(Qfapp, -37/10 + TmpC/10)
    monitored[1] = 1 + gslmod*(1 - monitored[52])
    monitored[2] = gapp*xbmodsp*math.pow(Qgapp, -37/10 + TmpC/10)*monitored[1]
    monitored[3] = math.exp(-hfmdc*(xXBprer*xXBprer)*math.copysign(1.0,\
        xXBprer)/(x_0*x_0))
    monitored[4] = math.exp(hbmdc*((xXBpostr - x_0)*(xXBpostr -\
        x_0))*math.copysign(1.0, xXBpostr - x_0)/(x_0*x_0))
    monitored[5] = hf*xbmodsp*math.pow(Qhf, -37/10 + TmpC/10)*monitored[3]
    monitored[6] = hb*xbmodsp*math.pow(Qhb, -37/10 + TmpC/10)*monitored[4]
    monitored[7] = (math.exp(sigmap*((-xXBpostr + x_0)*(-xXBpostr +\
        x_0))/(x_0*x_0)) if xXBpostr < x_0 else math.exp(sigman*((xXBpostr -\
        x_0)*(xXBpostr - x_0))/(x_0*x_0)))
    monitored[8] = gxb*xbmodsp*math.pow(Qgxb, -37/10 + TmpC/10)*monitored[7]

    # Expressions for the Normalised active and passive force component
    monitored[9] = (fapp*hb + fapp*gxb)/(gapp*hb + gapp*gxb + fapp*hb +\
        gxb*hf + fapp*gxb + fapp*hf)
    monitored[10] = fapp*hf/(gapp*hb + gapp*gxb + fapp*hb + gxb*hf + fapp*gxb\
        + fapp*hf)
    monitored[11] = kxb_normalised*x_0*monitored[10]
    monitored[12] = kxb_normalised*(XBprer*xXBprer +\
        XBpostr*xXBpostr)*monitored[52]
    monitored[13] = monitored[12]/monitored[11]
    monitored[14] = PCon_t*(-1 + math.exp(PExp_t*math.fabs(-SLrest +\
        SL)))*math.copysign(1.0, -SLrest + SL)
    monitored[15] = (PCon_c*(-1 + math.exp(PExp_c*math.fabs(-SL_c + SL))) if\
        SL > SL_c else 0)
    monitored[16] = monitored[14] + monitored[15]
    monitored[17] = PCon_t*(-1 + math.exp(PExp_t*math.fabs(-SLrest +\
        SLset)))*math.copysign(1.0, -SLrest + SLset)
    monitored[18] = (KSE*(SLset - SL) if SEon == 1 else fixed_afterload)
    monitored[19] = ((visc*(SLset - SL) + intf)/massf if SL > SLmin and SL <=\
        SLmax else 0)
    monitored[55] = monitored[17] + monitored[18] - monitored[13] -\
        monitored[16]
    monitored[54] = monitored[19]

    # Expressions for the Equation for simulated calcium transient component
    monitored[20] = -math.pow(tau1/tau2, -1/(1 - tau2/tau1)) +\
        math.pow(tau1/tau2, -1/(-1 + tau1/tau2))
    monitored[21] = (Ca_diastolic + (-Ca_diastolic +\
        Ca_amplitude)*(math.exp((start_time - t)/tau1) - math.exp((start_time\
        - t)/tau2))/monitored[20] if t > start_time else Ca_diastolic)

    # Expressions for the Ca binding to troponin to thin filament regulation
    # component
    monitored[22] = kon*math.pow(Qkon, -37/10 + TmpC/10)
    monitored[23] = koffL*koffmod*math.pow(Qkoff, -37/10 + TmpC/10)
    monitored[24] = koffH*koffmod*math.pow(Qkoff, -37/10 + TmpC/10)
    monitored[25] = -TRPNCaL*monitored[23] + (1 -\
        TRPNCaL)*monitored[21]*monitored[22]
    monitored[26] = -TRPNCaH*monitored[24] + (1 -\
        TRPNCaH)*monitored[21]*monitored[22]
    monitored[27] = (1 - monitored[53])*TRPNCaL + TRPNCaH*monitored[53]
    monitored[28] = math.sqrt(math.fabs(1.0/(1 +\
        math.pow(perm50/monitored[27], nperm))))
    monitored[29] = (1.0/monitored[28] if 1.0/monitored[28] < 100 else 100)
    monitored[57] = monitored[25]
    monitored[56] = monitored[26]
    monitored[30] = kn_p*math.pow(Qkn_p, -37/10 + TmpC/10)*monitored[28]
    monitored[31] = kp_n*math.pow(Qkp_n, -37/10 + TmpC/10)*monitored[29]

    # Expressions for the Regulation and crossbridge cycling state equations
    # component
    monitored[59] = P_NoXB*monitored[31] - N_NoXB*monitored[30]
    monitored[60] = -P_NoXB*monitored[31] + N_NoXB*monitored[30]
    monitored[32] = -XBpostr*monitored[6] - XBpostr*monitored[8] +\
        XBprer*monitored[5]
    monitored[33] = 1 - XBprer - XBpostr - N
    monitored[58] = -N*monitored[30] + monitored[31]*monitored[33]
    monitored[34] = monitored[0]*monitored[33] + XBpostr*monitored[6] -\
        XBprer*monitored[5] - XBprer*monitored[2]
    monitored[61] = monitored[32]
    monitored[62] = monitored[34]

    # Expressions for the Mean strain of strongly bound states component
    monitored[35] = (monitored[0]*monitored[6] +\
        monitored[0]*monitored[8])/(monitored[0]*monitored[5] +\
        monitored[2]*monitored[8] + monitored[0]*monitored[6] +\
        monitored[5]*monitored[8] + monitored[2]*monitored[6] +\
        monitored[0]*monitored[8])
    monitored[36] = monitored[0]*monitored[5]/(monitored[0]*monitored[5] +\
        monitored[2]*monitored[8] + monitored[0]*monitored[6] +\
        monitored[5]*monitored[8] + monitored[2]*monitored[6] +\
        monitored[0]*monitored[8])
    monitored[37] = monitored[19]/2 + xPsi*(-monitored[0]*xXBprer + (-xXBprer\
        + xXBpostr - x_0)*monitored[6])/monitored[35]
    monitored[38] = monitored[19]/2 + xPsi*(-xXBpostr + xXBprer +\
        x_0)*monitored[5]/monitored[36]
    monitored[64] = monitored[37]
    monitored[63] = monitored[38]

    # Expressions for the Calculation of micromolar per millisecondes of Ca
    # for apparent Ca binding component
    monitored[39] = (XBprer + XBpostr)/(monitored[9] + monitored[10])
    monitored[40] = (monitored[32] + monitored[34])/(monitored[9] +\
        monitored[10])
    monitored[41] = (-0.5*monitored[19] if SL < len_thick else 0)
    monitored[42] = (-0.5*monitored[19] if -SL + 2*len_thin > len_hbare else 0)
    monitored[43] = -monitored[42] + monitored[41]
    monitored[44] = monitored[43]/len_thin
    monitored[45] = 2*monitored[43]/(-len_hbare + len_thick)
    monitored[46] = Trop_conc*((1 - monitored[53])*TRPNCaL + ((1 -\
        monitored[39])*TRPNCaL + TRPNCaH*monitored[39])*monitored[53])
    monitored[47] = Trop_conc*((1 - monitored[53])*monitored[25] +\
        (-TRPNCaL*monitored[40] + monitored[26]*monitored[39] +\
        TRPNCaH*monitored[40] + (1 -\
        monitored[39])*monitored[25])*monitored[53] - TRPNCaL*monitored[44] +\
        ((1 - monitored[39])*TRPNCaL + TRPNCaH*monitored[39])*monitored[44])
    monitored[48] = kxb*(XBprer*xXBprer + XBpostr*xXBpostr)*monitored[45] +\
        kxb*(XBpostr*monitored[38] + monitored[34]*xXBprer +\
        monitored[32]*xXBpostr + XBprer*monitored[37])*monitored[52]

    # Return results
    return monitored
