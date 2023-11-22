import subprocess
import numpy as np
import os
from read_input_file import read_input_file

def etc_estimate(exp, tim, magband, mag):
    variables = read_input_file('input_file.txt')
    T = variables.get('T')
    log_g = variables.get('log_g')
    #magband = variables.get('magband')
    #Vmag = variables.get('Vmag')
    Imag = variables.get('Imag')
    #Ymag = variables.get('Ymag')
    #Jmag = variables.get('Jmag')
    #Hmag = variables.get('Hmag')
    airmass = variables.get('airmass')
    pwv = variables.get('pwv')
    see = variables.get('see')
    harps = variables.get('harps')
    nirps = variables.get('nirps')
    T_marcs = variables.get('T_marcs')
    log_g_marcs = variables.get('log_g_marcs')

    with open("etc-form.json",'r') as f:
        get_all=f.readlines()

    with open("etc-form.json",'w') as f:
        for i, line in enumerate(get_all,1):         
            if i == 18:                              
                f.writelines(f'          "spectype": "p{T_marcs}:g+{log_g_marcs}:m0.0:t02:st:z+0.00:a+0.00:c+0.00:n+0.00:o+0.00"\n')
            elif i == 25:
                f.writelines(f'        "magband": "{magband}",\n')
            elif i == 26:
                f.writelines(f'        "mag": {mag},\n')
            elif i == 34:
                f.writelines(f'      "turbulence_category": {see},\n')
            elif i == 35:
                f.writelines(f'      "gsmag": {Imag}\n')
            elif i == 41:
                f.writelines(f'    "DET1.WIN1.UIT1": {tim},\n')
            elif i == 45:
                f.writelines(f'    "airmass": {airmass},\n')
            elif i == 47:
                f.writelines(f'    "pwv": {pwv}\n')
            elif i == 51:
                f.writelines(f'      "mode": "{harps}",\n')
            elif i == 59:
                f.writelines(f'      "mode": "{nirps}",\n')
            else:
                f.writelines(line)

    if magband == 'V':
        args_h = ['python', 'etc_cli.py', 'harps', 'etc-form.json', '-o', 'output1.json']
        output_h = subprocess.check_output(args_h)
        
        args_h2 = ['python', 'etc_json2ascii.py', 'output1.json']  # Remove the '# -v' part
        output_h2 = subprocess.check_output(args_h2)
        
        band = np.loadtxt('output1.json_order:111_det:1_snr_snr.ascii')
        
    elif magband in ('Y', 'J', 'H'):
        args_n = ['python', 'etc_cli.py', 'nirps', 'etc-form.json', '-o', 'output2.json']
        output_n = subprocess.check_output(args_n)
        
        args_n2 = ['python', 'etc_json2ascii.py', 'output2.json']  # Remove the '# -v' part
        output_n2 = subprocess.check_output(args_n2)
        
        if magband == 'Y':
            band = np.loadtxt('output2.json_order:134_det:1_snr_snr.ascii')
        elif magband == 'J':
            band = np.loadtxt('output2.json_order:119_det:1_snr_snr.ascii')
        elif magband == 'H':
            band = np.loadtxt('output2.json_order:89_det:1_snr_snr.ascii')
    else:
        print("Invalid magband value")

    #args_h = ['python', 'etc_cli.py', 'harps', 'etc-form.json', '-o', f'output1.json']
    #output_h = subprocess.check_output(args_h)

    #args_n = ['python', 'etc_cli.py', 'nirps', 'etc-form.json', '-o', f'output2.json']
    #output_n = subprocess.check_output(args_n)

    #args_h2 = ['python', 'etc_json2ascii.py', f'output1.json']#, '-v']
    #output_h2 = subprocess.check_output(args_h2)

    #args_n2 = ['python', 'etc_json2ascii.py', f'output2.json']#, '-v']
    #output_n2 = subprocess.check_output(args_n2)

    #y_band = np.loadtxt(f'output2.json_order:134_det:1_snr_snr.ascii')
    #J_band = np.loadtxt(f'output2.json_order:119_det:1_snr_snr.ascii')
    #H_band = np.loadtxt(f'output2.json_order:89_det:1_snr_snr.ascii')

    #harps550_band = np.loadtxt(f'output1.json_order:111_det:1_snr_snr.ascii')

    band_max = band.max()
    
    my_dir = os.getcwd()
    for fname in os.listdir(my_dir):
        if fname.startswith(f"output2"):
            os.remove(os.path.join(my_dir, fname))

    for fname in os.listdir(my_dir):
        if fname.startswith(f"output1"):
            os.remove(os.path.join(my_dir, fname))

    return band_max
