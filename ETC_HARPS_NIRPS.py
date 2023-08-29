import numpy as np
import os
import matplotlib.pyplot as plt
from read_input_file import read_input_file
from fill_param_no_pb import fill_params_no_pb
import time
from calculations import etc_estimate
import shutil


# Store the original working directory
original_working_dir = os.getcwd()

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

exp = np.arange(0, 1500, 500)

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
    
if calc_pb.upper() == "Y":
    # Calculate the planetary blur
    from blur_cal import blur
    PB, comb_SNR_y, comb_SNR_J, comb_SNR_H, comb_SNR_harps550 = blur(exp, y_list, J_list, H_list, harps550_list) # PB in km/s
else:
    # Set PB and combined SNR to None so it is not included in output
    PB = None
    comb_SNR_y = None
    comb_SNR_J = None
    comb_SNR_H = None
    comb_SNR_harps550 = None

# Ask user for custom output folder path
custom_path = input("Do you want to specify a custom path for storing the outputs? (y/n): ")

if custom_path.lower() == 'y':
    output_folder = input("Enter the custom output folder path: \n It should be something like: /Users/name/Desktop \n")
else:
    output_folder = 'outputs'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    
# Define the base output folder and name
base_output_folder = output_folder

# Find the next available sub-folder name
folder_suffix = 1
output_folder = os.path.join(base_output_folder, f'{name}_{folder_suffix}')
while os.path.exists(output_folder):
    folder_suffix += 1
    output_folder = os.path.join(base_output_folder, f'{name}_{folder_suffix}')
    
# Create the output folder
os.makedirs(output_folder)

# save the arrays to a text file
if PB is not None:
    np.savetxt(os.path.join(output_folder, f'{name}.txt'), np.column_stack((exp, harps550_list, y_list, J_list, H_list, PB, comb_SNR_y, comb_SNR_J, comb_SNR_H, comb_SNR_harps550)), fmt='%1.8f', header='Exp. Time (s)\tharps550\ty\tJ\tH\tPB (km/s/pixel)\tSNR_y_tran\tSNR_J_tran\tSNR_H_tran\tSNR_harps550_tran')
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

plt.savefig(os.path.join(output_folder, f'{name}_1.png'), dpi=300)
# plt.show()

if PB is not None:
    fig, ax = plt.subplots()
    ax.plot(exp, comb_SNR_y, color='green', label='y - band')
    ax.plot(exp, comb_SNR_H, color='red', label='H - band')
    ax.plot(exp, comb_SNR_harps550, color='blue', label='HARPS @ 550nm')
    ax.set_xlabel('Exp. Time (s)')
    ax.set_ylabel('SNR')
    ax.tick_params(axis='y', labelcolor='black')
    ax.legend(loc='upper left')
    ax.grid()
    plt.title(f'{name}: Combined SNR during transit')
    plt.tight_layout()
    
    plt.savefig(os.path.join(output_folder, f'{name}_2.png'), dpi=300)


# Get the path of the input file
input_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input_file.txt')

# Copy the input file to the output folder
input_file_name = os.path.basename(input_file_path)
output_input_file_path = os.path.join(output_folder, input_file_name)
shutil.copyfile(input_file_path, output_input_file_path)

print("-----------------------------------------------------------")
print(f"Outputs are stored in {os.path.abspath(output_folder)}\n")

print("It took %s seconds to compute this." % (time.time() - start_time))

os.chdir(original_working_dir)
