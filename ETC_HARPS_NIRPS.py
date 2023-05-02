import numpy as np
import os
import matplotlib.pyplot as plt
from read_input_file import read_input_file
from fill_param_no_pb import fill_params_no_pb
import time
from calculations import etc_estimate

# Ask the user if the planetary blur should be calculated
calc_pb = input("Calculate Planetary Blur? (Y/N): ")

if calc_pb.upper() == "Y":
    # Calculate the planetary blur using fill_params()
    from fill_param import fill_params
    fill_params()
else:
    # Calculate parameters without planetary blur using fill_params_no_pb()
    fill_params_no_pb()

variables = read_input_file('input_file.txt')
name = variables.get('name')
#print(name)

start_time = time.time()

exp = np.arange(0, 1500, 60)

y_list = []
J_list = []
H_list = []
harps550_list = []

if calc_pb.upper() == "Y":
    # Calculate the planetary blur
    from blur_cal import blur
    PB = blur(exp) # PB in km/s/pixel
else:
    # Set PB to None so it is not included in output
    PB = None

for tim in exp:
    y, J, H, harps550 = etc_estimate(exp, tim)
    y_list.append(y)
    J_list.append(J)
    H_list.append(H)
    harps550_list.append(harps550)

# create a folder for outputs
if not os.path.exists('outputs'):
    os.makedirs('outputs')

output_folder = os.path.join('outputs', name)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# save the arrays to a text file
if PB is not None:
    np.savetxt(os.path.join(output_folder, f'{name}.txt'), np.column_stack((exp, harps550_list, y_list, J_list, H_list, PB)), fmt='%1.8f', header='Exp. Time (s)\tharps550\ty\tJ\tH\tPB (km/s/pixel)')
else:
    np.savetxt(os.path.join(output_folder, f'{name}.txt'), np.column_stack((exp, harps550_list, y_list, J_list, H_list)), fmt='%1.8f', header='Exp. Time (s)\tharps550\ty\tJ\tH')

fig, ax1 = plt.subplots()

# plot harps550_list, y_list, J_list, and H_list on the left y-axis
ax1.plot(exp, harps550_list, color='blue', label='HARPS @ 550nm')
ax1.plot(exp, y_list, color='green', label='y - band')
# ax1.plot(exp, J_list, color='orange', label='J - band')
ax1.plot(exp, H_list, color='red', label='H - band')
ax1.set_xlabel('Exp. Time (s)')
ax1.set_ylabel('SNR')
ax1.tick_params(axis='y', labelcolor='black')
ax1.legend(loc='upper left')
ax1.grid()

# add PB to the plot if it was calculated
if PB is not None:
    # create a second y-axis on the right side of the plot for PB
    ax2 = ax1.twinx()
    ax2.plot(exp, PB, color='black', label='PB')
    ax2.set_ylabel('Planetary Blur (km/s)')
    ax2.tick_params(axis='y', labelcolor='black')
    ax2.legend(loc='lower right')

plt.title(f'{name}: SNR and Planetary Blur Variation with Exposure Time')
# adjust the layout to fit the plot elements in the available space
plt.tight_layout()

plt.savefig(os.path.join(output_folder, f'{name}.png'), dpi=300)
# plt.show()

print("--- %s seconds ---" % (time.time() - start_time))
