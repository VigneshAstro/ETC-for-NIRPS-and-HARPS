import math
import numpy as np
from read_input_file import read_input_file
from exofile.archive import ExoFile
from rv_calculator import ks_kp, Keplerian, Kepler_func, True_anom_calc, time_to_phase

#def blur(exp, y_list, J_list, H_list, harps550_list):
def blur(exp, y_list, H_list, harps550_list):

    variables = read_input_file('input_file.txt')
    pl_name = variables.get('name')
    R_p = variables.get('R_p')
    M_p = variables.get('M_p')
    R_s = variables.get('R_s')
    R_rat = variables.get('R_rat')
    M_s = variables.get('M_s')
    Vsys = variables.get('Vsys')
    inc = variables.get('inc')
    mpsini = variables.get('mpsini')
    w = variables.get('w')
    P = variables.get('P')
    a = variables.get('a')
    ecc = variables.get('ecc')
    b = variables.get('b')
    T0 = variables.get('T0')

    r_p = R_p * 69911
    if R_s == 0:
        if R_rat == 0:
            r_s = 1 * 696340 #assuming stellar radius is 1 solar radius (in kms)
            print("Stellar radius is unknown. Assumed as 1 solar radius.")
        else:
            r_s = r_p / R_rat
    else:
        r_s = R_s * 696340 # star radius in kms
    
    inc_rad = math.radians(inc)
    p = P * 24 * 3600
    k = r_p / r_s
    
    data = ExoFile.load()
    tdur = float(data.by_pl_name(pl_name)['pl_trandur'])  # transit duration in hours
    tdur = 0 if np.isnan(tdur) else tdur
    if tdur == 0:
        tdur = (p / np.pi) * np.arcsin((r_s / (a * 1.495978707 * 10**8)) * ((np.sqrt(((1 + k)**2) - (b**2))) / (np.sin(inc_rad))))
    else:
        tdur = tdur * 60 * 60  # converting to seconds.

    T_1 = T0 - (tdur / (2 * 24 * 3600))
    T_4 = T0 + (tdur / (2 * 24 * 3600))

    if M_p == 0:
        k_s, k_p = ks_kp(M_s, mpsini, a, ecc, inc)
    else:
        k_s, k_p = ks_kp(M_s, M_p, a, ecc, inc)

    RV_1 = -Keplerian(k_p, T_1, T0, P, ecc, w)
    RV_4 = -Keplerian(k_p, T_4, T0, P, ecc, w)

    PB = ((RV_4 - RV_1) / tdur) * exp
    PB = np.abs(PB)

    transit_frames_NIRPS = tdur // (exp + (0.2 * 60))  # Max NIRPS frames during Transit, with overhead time between frames (0.2 min)
    transit_frames_HARPS = tdur // (exp + (0.53 * 60))  # Max HARPS frames during Transit, with overhead time between frames (0.53 min)

    tran_max_SNR_y = y_list * np.sqrt(transit_frames_NIRPS)
    #tran_max_SNR_J = J_list * np.sqrt(transit_frames_NIRPS)
    tran_max_SNR_H = H_list * np.sqrt(transit_frames_NIRPS)
    tran_max_SNR_harps550 = harps550_list * np.sqrt(transit_frames_HARPS)
    
    #return PB, tran_max_SNR_y, tran_max_SNR_J, tran_max_SNR_H, tran_max_SNR_harps550
    return PB, tran_max_SNR_y, tran_max_SNR_H, tran_max_SNR_harps550

