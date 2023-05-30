import math
import numpy as np
from read_input_file import read_input_file

from rv_calculator import ks_kp
from rv_calculator import Keplerian
from rv_calculator import Kepler_func
from rv_calculator import True_anom_calc

def blur(exp, y_list, J_list, H_list, harps550_list):

    variables = read_input_file('input_file.txt')
    R_p = variables.get('R_p')
    M_p = variables.get('M_p')
    
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
    r_s = r_p / R_rat
    # print(r_s)
   

    inc_rad = math.radians(inc)
    p = P * 24 * 3600
    k = r_p / r_s

    tdur = (p/math.pi) * np.arcsin((r_s/(a* 1.495978707 * 10**8)) * ((np.sqrt(((1+k)**2)-(b**2)))/(np.sin(inc_rad))))
    #print(tdur)
    # time at ingress (1) and egress (4)
    T_1 = T0 - (tdur/(2 * 24 * 3600))
    T_4 = T0 + (tdur/(2 * 24 * 3600))
    #print(T_1, T_4)

    if M_p == 0:
        k_s, k_p = ks_kp(M_s,mpsini,a,ecc,inc)
    else:
        k_s, k_p = ks_kp(M_s,M_p,a,ecc,inc)
    #print(k_p,k_s)
    RV_1= -Keplerian(k_p,T_1,T0,P,ecc,w)
    RV_4= -Keplerian(k_p,T_4,T0,P,ecc,w)
    #print(RV_1, RV_4)

    PB = ((RV_4 - RV_1) / tdur) * exp
    PB = np.abs(PB)
    
    #calculating the TOTAL SNR during transit
    transit_frames_NIRPS = tdur // (exp + (0.2 * 60))#Max NIRPS frames during Transit, with overgead time between frames(0.2 min)
    transit_frames_HARPS = tdur // (exp + (0.53 * 60))#Max HARPS frames during Transit, with overgead time between frames(0.53min)
    
    #Calculating the maximum SNR in each band, by combining the number of frames during the transit.
    tran_max_SNR_y = y_list * np.sqrt(transit_frames_NIRPS)
    tran_max_SNR_J = J_list * np.sqrt(transit_frames_NIRPS)
    tran_max_SNR_H = H_list * np.sqrt(transit_frames_NIRPS)
    tran_max_SNR_harps550 = harps550_list * np.sqrt(transit_frames_HARPS)
    
    return PB, tran_max_SNR_y, tran_max_SNR_J, tran_max_SNR_H, tran_max_SNR_harps550
