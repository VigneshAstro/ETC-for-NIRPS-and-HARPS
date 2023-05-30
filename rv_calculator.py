import math
import numpy as np
from scipy.optimize import newton

#calculating K_s and K_p of the star and planet.
def ks_kp(M_s,M_p,a,ecc,inc):

    m_p = M_p * 1898.13 * 10**24 # from Jup mass to kgs
    m_s = M_s * 1988500 * 10**24 # from Solar mass to kgs

    inc = math.radians(inc) #inclination in degrees to radians
    a = a * 1.495978707 * 10**8 # semi-major axis from AU to kms
    G = 6.67430 * 10**(-20) # Newton Gravitational constant in units of blah-blah but instead of m in kms
    
    k_s = np.sqrt(G / ((m_s + m_p) * a * (1 - ecc**2))) * m_p * np.sin(inc)

    def K_p(k_star,m_star,m_planet):
        return np.float(k_star)*(np.float(m_star)+np.float(m_planet))/(np.float(m_planet))

    k_p = K_p(k_s,m_s,m_p)
    
    return k_s, k_p

#calculation of Keplerian
def Keplerian(K_star,time,time_ref,period,ecc,omega):
    omega_bar=np.radians(omega)
    if (ecc<1e-4):
        v_rad=-K_star*np.sin(2*np.pi*(time-time_ref)/period)
    else:
        true_anomaly=True_anom_calc(ecc,time_to_phase(time,time_ref,period),omega_bar)[0]
        v_rad=K_star*(np.cos(true_anomaly+omega_bar)+ecc*np.cos(omega_bar))
    #print 'omega_bar : ', omega_bar
    return v_rad

def Kepler_func(Ecc_anom,Mean_anom,ecc):
    
    #Ecc_anom =np.radians(Ecc_anom)
    #Mean_anom =np.radians(Mean_anom)
    """
    Find the Eccentric anomaly using the mean anomaly and eccentricity 
        - M = E - e sin(E)
    """
    delta=Ecc_anom-ecc*np.sin(Ecc_anom)-Mean_anom
    return delta 

#calculation of true anamoly
def True_anom_calc(ecc,phase,omega_bar):
    
    #ecc=np.radians(ecc)
    #omega_bar= np.radians(omega_bar)
    
    #Circular orbit
    #  - 1e-4 instead of 0 to avoid loosing too much time with really low tested values of ecc    
    if (ecc<1e-4):

        #True anomaly
        True_anom=2.*np.pi*phase
        
        #Eccentric anomaly
        Ecc_anom=None
                                
    #--------------------------------------------------------------------------------------------------------------------
    #Eccentric orbit   
    #  - by definition the ascending node is where the object goes toward the observer through the plane of sky
    #  - omega_bar is the angle between the ascending node and the periastron, in the orbital plane (>0 counterclockwise)                       
    else:

        #True anomaly of the planet at mid-transit (in rad):
        #    - angle counted from 0 at the periastron, to the star/Earth LOS
        #    - >0 counterclockwise, possibly modulo 2pi
        #    - with omega_bar counted from ascending node to periastron
        True_anom_TR=(np.pi/2.)-omega_bar
    
        #Mean anomaly at the time of the transit
        #    - corresponds to 'dt_transit' (in years), time from periapsis to transit center 
        #    - atan(X) is in -pi/2 ; pi/2 
        Ecc_anom_TR=2.*np.arctan( np.tan(True_anom_TR/2.)*np.sqrt((1.-ecc)/(1.+ecc)) )
        Mean_anom_TR=Ecc_anom_TR-ecc*np.sin(Ecc_anom_TR)
        if (Mean_anom_TR<0.):Mean_anom_TR=Mean_anom_TR+2.*np.pi
        
        #Mean anomaly
        #  - time origin of t_mean at the periapsis (t_mean=0 <-> M=0 <-> E=0)
        #  - M(t_mean)=M(dt_transit)+M(t_simu) 
        Mean_anom=2.*np.pi*phase+Mean_anom_TR
     
        #Eccentric anomaly : 
        #  - M = E - e sin(E)
        #    - >0 counterclockwise
        #  - angle, with origin at the ellipse center, between the major axis toward the periapsis and the 
        #line crossing the circle with radius 'a_Rs' at its intersection with the perpendicular to 
        #the major axis through the planet position
        Ecc_anom=newton(Kepler_func,Mean_anom,args=(Mean_anom,ecc,))

        #True anomaly of the planet at current time
        True_anom=2.*np.arctan(np.sqrt((1.+ecc)/(1.-ecc))*np.tan(Ecc_anom/2.))
        #print 'true anomaly : ', True_anom
        #print 'ecc anomaly  : ', Ecc_anom
        #print ' 2 pi phase  : ', 2.*np.pi*phase
        #print 'Mean_anom    : ', Mean_anom
                
    return True_anom,Ecc_anom
