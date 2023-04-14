from calculations import etc_estimate
import input_file
import numpy as np
import matplotlib.pyplot as plt
import time
import os
import math

start_time = time.time()

exp = np.arange(10, 1500, 30)

y_list = []
J_list = []
H_list = []
harps550_list = []

for tim in exp:
    y, J, H, harps550 = etc_estimate(exp, tim)
    y_list.append(y)
    J_list.append(J)
    H_list.append(H)
    harps550_list.append(harps550)

name = input_file.name #planet name


R_s = input_file.R_s # in solar radii
M_s = input_file.M_s # in solar mass
Vsys = input_file.Vsys # in km/s


R_p = input_file.R_p # in Jupiter radii
M_p = input_file.M_p # in Jupiter mass
inc = input_file.inc # in in degree
mpsini = input_file.mpsini # in Jupiter mass

w = input_file.w # in argument of periastron
P = input_file.P # in days
a = input_file.a # in AU
ecc = input_file.ecc # eccentricity
b = input_file.b # impact parameter in star radii

r_p = R_p * 69911 # in kms
r_s = R_s * 695700 # in kms
m_p = M_p * 1898.13 * 10**24 # in kgs
m_s = M_s * 1988500 * 10**24 # in kgs
mpsini = mpsini * 1898.13 * 10**24 # in kgs

inc = math.radians(inc) # converting to radians
p = P * 24 * 3600 # period in seconds
a = a * 1.495978707 * 10**8 # in kms
k = r_p / r_s # radius ratio
G = 6.67430 * 10**(-20) # G in km^3 kg_1 s-2

tdur = (p/math.pi) * np.arcsin((r_s/a) * ((np.sqrt(((1+k)**2)-(b**2)))/(np.sin(inc)))) # transit duration assuming circular orbit

phi_1 = (-(tdur/2)/p) # beginning of transit
phi_4 = ((tdur/2)/p) # end of transit

if m_p == 0:
    k_p = np.sqrt(G / (m_s * a * (1 - ecc**2))) * mpsini
else:
    k_p = np.sqrt(G / ((m_s + m_p) * a * (1 - ecc**2))) * m_p * np.sin(inc)

M1 = 2.0 * np.pi * phi_1 / (1.0 - ecc**2) + w
M4 = 2.0 * np.pi * phi_4 / (1.0 - ecc**2) + w

# Solve for eccentric anomaly for each mean anomaly
E1 = M1
E4 = M4
for i in range(10):
    E1 = E1 - (E1 - ecc * np.sin(E1) - M1) / (1 - ecc * np.cos(E1))
    E4 = E4 - (E4 - ecc * np.sin(E4) - M4) / (1 - ecc * np.cos(E4))

# Calculate true anomaly for each eccentric anomaly
f1 = 2.0 * np.arctan2(np.sqrt(1.0 + ecc) * np.sin(E1 / 2.0), np.sqrt(1.0 - ecc) * np.cos(E1 / 2.0))
f4 = 2.0 * np.arctan2(np.sqrt(1.0 + ecc) * np.sin(E4 / 2.0), np.sqrt(1.0 - ecc) * np.cos(E4 / 2.0))

# Calculate radial velocity for each true anomaly
RV_1 = k_p * (np.sin(f1 + w) + ecc * np.sin(w))
RV_4 = k_p * (np.sin(f4 + w) + ecc * np.sin(w))


PB = ((RV_4 - RV_1) / tdur) * exp

# create a folder for outputs
if not os.path.exists('outputs'):
    os.makedirs('outputs')

output_folder = os.path.join('outputs', name)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# save the arrays to a text file
output_file = os.path.join(output_folder, f'{name}.txt')
np.savetxt(output_file, np.column_stack((exp, harps550_list, y_list, J_list, H_list, PB)), fmt='%1.8f', header='Exp. Time (s)\tharps550\ty\tJ\tH\tPB (km/s/pixel)')



fig, ax1 = plt.subplots()

# plot harps550_list, y_list, J_list, and H_list on the left y-axis
ax1.plot(exp, harps550_list, color='blue', label='HARPS @ 550nm')
ax1.plot(exp, y_list, color='green', label='y - band')
ax1.plot(exp, J_list, color='orange', label='J - band')
ax1.plot(exp, H_list, color='red', label='H - band')
ax1.set_xlabel('Exp. Time (s)')
ax1.set_ylabel('SNR')
ax1.tick_params(axis='y', labelcolor='black')
ax1.legend(loc='upper left')

# create a second y-axis on the right side of the plot for PB
ax2 = ax1.twinx()
ax2.plot(exp, PB, color='black', label='PB')
ax2.set_ylabel('Planetary Blur (km/s)')
ax2.tick_params(axis='y', labelcolor='black')
ax2.legend(loc='lower right')

plt.title(f'{name}: SNR and Planetary Blur Variation with Exposure Time')
plt.savefig(os.path.join(output_folder, f'{name}.png'), dpi=300)
# plt.show()


print("--- %s seconds ---" % (time.time() - start_time))