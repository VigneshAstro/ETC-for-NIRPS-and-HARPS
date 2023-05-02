import subprocess
import numpy as np
import os
from read_input_file import read_input_file

def etc_estimate(exp, tim):
    variables = read_input_file('input_file.txt')
    T = variables.get('T')
    magband = variables.get('magband')
    mag = variables.get('mag')
    airmass = variables.get('airmass')
    pwv = variables.get('pwv')
    see = variables.get('see')
    harps = variables.get('harps')
    nirps = variables.get('nirps')

    with open("etc-form.json",'r') as f:
        get_all=f.readlines()

    with open("etc-form.json",'w') as f:
        for i, line in enumerate(get_all,1):         
            if i == 16:                              
                f.writelines(f'          "temperature": {T}\n')
            elif i == 23:
                f.writelines(f'        "magband": "{magband}",\n')
            elif i == 24:
                f.writelines(f'        "mag": {mag},\n')
            elif i == 32:
                f.writelines(f'      "turbulence_category": {see},\n')
            elif i == 39:
                f.writelines(f'    "DET1.WIN1.UIT1": {tim},\n')
            elif i == 43:
                f.writelines(f'    "airmass": {airmass},\n')
            elif i == 46:
                f.writelines(f'    "pwv": {pwv}\n')
            elif i == 50:
                f.writelines(f'      "mode": "{harps}",\n')
            elif i == 127:
                f.writelines(f'      "mode": "{nirps}",\n')
            else:
                f.writelines(line)

    args_h = ['python', 'etc_cli.py', 'harps', 'etc-form.json', '-o', f'output1_{i}.json']
    output_h = subprocess.check_output(args_h)

    args_n = ['python', 'etc_cli.py', 'nirps', 'etc-form.json', '-o', f'output2_{i}.json']
    output_n = subprocess.check_output(args_n)

    args_h2 = ['python', 'etc_json2ascii.py', f'output1_{i}.json', '-v']
    output_h2 = subprocess.check_output(args_h2)

    args_n2 = ['python', 'etc_json2ascii.py', f'output2_{i}.json', '-v']
    output_n2 = subprocess.check_output(args_n2)

    y_band = np.loadtxt(f'output2_{i}.json_order:142_det:1_snr_snr.ascii')
    J_band = np.loadtxt(f'output2_{i}.json_order:119_det:1_snr_snr.ascii')
    H_band = np.loadtxt(f'output2_{i}.json_order:89_det:1_snr_snr.ascii')

    harps550_band = np.loadtxt(f'output1_{i}.json_order:111_det:1_snr_snr.ascii')

    y = y_band.max()
    J = J_band.max()
    H = H_band.max()

    harps550 = harps550_band.max()

    my_dir = os.getcwd()
    for fname in os.listdir(my_dir):
        if fname.startswith(f"output2_{i}"):
            os.remove(os.path.join(my_dir, fname))

    for fname in os.listdir(my_dir):
        if fname.startswith(f"output1_{i}"):
            os.remove(os.path.join(my_dir, fname))

    return y, J, H, harps550
