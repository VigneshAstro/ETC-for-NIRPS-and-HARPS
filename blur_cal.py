import math
import numpy as np
from read_input_file import read_input_file

def blur(exp):

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
    m_p = M_p * 1898.13 * 10**24
    m_s = M_s * 1988500 * 10**24
    mpsini = mpsini * 1898.13 * 10**24

    inc = math.radians(inc)
    p = P * 24 * 3600
    a = a * 1.495978707 * 10**8
    k = r_p / r_s
    G = 6.67430 * 10**(-20)

    tdur = (p/math.pi) * np.arcsin((r_s/a) * ((np.sqrt(((1+k)**2)-(b**2)))/(np.sin(inc))))

    if m_p == 0:
        k_s = np.sqrt(G / (m_s * a * (1 - ecc**2))) * mpsini
    else:
        k_s = np.sqrt(G / ((m_s + m_p) * a * (1 - ecc**2))) * m_p * np.sin(inc)

    def K_p(k_star,m_star,m_planet):
        return np.float(k_star)*(np.float(m_star)+np.float(m_planet))/(np.float(m_planet))

    if m_p == 0: 
        k_p = K_p(k_s,m_s,mpsini)
    else:
        k_p = K_p(k_s,m_s,m_p)

    # Calculate the time of periastron passage
    Tp = T0 + (P / (2 * np.pi)) * (w + np.pi)

    # time at ingress (1) and egress (4)
    T_1 = T0 - (tdur/(2 * 24 * 3600))
    T_4 = T0 + (tdur/(2 * 24 * 3600))

    M_1 = 2 * np.pi * (T_1 - Tp) / P
    E_1 = M_1.copy()

    M_4 = 2 * np.pi * (T_4 - Tp) / P
    E_4 = M_4.copy()
    
    M_0 = 2 * np.pi * (T0 - Tp) / P
    # print(M_0)
    E_0 = M_0

    for j in range(10):
        E_1 = M_1 + ecc * np.sin(E_1)
        E_4 = M_4 + ecc * np.sin(E_4)
        E_0 = M_0 + ecc * np.sin(E_0)
        # print (E_1, E_0, E_4)
    theta_1 = 2 * np.arctan(np.sqrt((1+ecc)/(1-ecc)) * np.tan(E_1/2))
    theta_4 = 2 * np.arctan(np.sqrt((1+ecc)/(1-ecc)) * np.tan(E_4/2))
    theta_0 = 2 * np.arctan(np.sqrt((1+ecc)/(1-ecc)) * np.tan(E_0/2))

    RV_1 = k_p * (np.cos(theta_1 + w) + ecc * np.cos(w))
    RV_4 = k_p * (np.cos(theta_4 + w) + ecc * np.cos(w))
    RV_0 = k_p * (np.cos(theta_0 + w) + ecc * np.cos(w))

    # print (k_s,k_p,tdur, T_1, T_4, Tp, M_1, theta_1, M_4, theta_4, M_0, theta_0, RV_1, RV_4, RV_0)

    PB = -(2 * (RV_0 - RV_1) / tdur) * exp
    
    return PB
