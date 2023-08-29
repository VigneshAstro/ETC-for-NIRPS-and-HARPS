def fill_params_no_pb():
    import os
    import numpy as np
    from exofile.archive import ExoFile
    import warnings
    warnings.filterwarnings("ignore")
    while True:
        input_filled = input("Are the input parameters filled? (Y/N): ")
        if input_filled == 'Y':
            del np, os, ExoFile
            for var in list(locals()):
                del locals()[var]
            for var in list(globals()):
                del globals()[var]    
            break
        elif input_filled == 'N':
            star_name = input("Please enter the star's name: ")
            nirps_mode = input("Please enter NIRPS mode HA/HE (eg: he): ")
            harps_mode = input("Please enter HARPS mode ham/eggs (eg: ham): ")
            am = input("Please enter airmass (between 1 - 2.9): ")
            pw = input("Please enter precipitable water vapour in mm (between 0.05 - 30): ")
            see = input("Please enter the turbulent condition[TC] \n(10% (i.e. seeing<=0.5 arcsec), 20% (<=0.6), 30% (<=0.7), 50% (<=0.8), 70% (<=1.0), 85% (<=1.3), 100% (<=2)) \n(eg: 70): ")
            data = ExoFile.load()
            name = str(data.by_pl_name(star_name)['pl_name']).strip()
            T = float(data.by_pl_name(star_name)['st_teff'])
            log_g = float(data.by_pl_name(star_name)['st_logg'])
            mag = float(data.by_pl_name(star_name)['sy_jmag']) 
            Vmag = float(data.by_pl_name(star_name)['sy_vmag'])
            Vsys = float(data.by_pl_name(star_name)['st_radv'])

            # set NaN values to 0
            T = 0 if np.isnan(T) else T
            log_g = 0 if np.isnan(log_g) else log_g
            mag = 0 if np.isnan(mag) else mag
            Vmag = 0 if np.isnan(Vmag) else Vmag
            Vsys = 0 if np.isnan(Vsys) else Vsys
            
            def calculate_VIc(t):
                p = [-2.83075664025470e-29, 3.92667558174934e-24, -2.24230251111333e-19, 6.80719949189014e-15, -1.18352878068551e-10, 1.17969134650677e-06, -0.00631161664369208, 14.2773745300312]
                VIc = sum(p[i] * (t ** (7 - i)) for i in range(len(p)))
                return VIc
            VI = calculate_VIc(T) #This calculated the V-Ic mag from https://www.pas.rochester.edu/~emamajek/EEM_dwarf_UBVIJHK_colors_Teff.txt
            Imag = round(Vmag - VI, 2) # we calculate the Imag from Vmag and V-Ic
            
            def find_closest_value(target, value_list):
                closest_value = min(value_list, key=lambda x: abs(x - target))
                return closest_value

            def main(T, log_g):
                T_range = [3000, 3100, 3200, 3300, 3400, 3500, 3600, 3700, 3800, 3900, 4000, 4250, 4500, 4750, 5000, 5250, 5500, 5750, 6000, 6250, 6500, 6750, 7000, 7250, 7500, 7750, 8000]
                log_g_range = [3.0, 3.5, 4.0, 4.5, 5.0]
    
                T_marcs = find_closest_value(T, T_range)
                log_g_marcs = find_closest_value(log_g, log_g_range)
    
                if log_g == 0:
                    log_g_marcs = 4.0
    
                return T_marcs, log_g_marcs

            T_marcs, log_g_marcs = main(T, log_g)

            # with open('input_file.txt', 'w') as f:
            with open(os.path.join(os.path.dirname(__file__), 'input_file.txt'), 'w') as f:
                f.write(f"name = '{star_name}'\n")
                f.write(f"T = {T}\n")
                f.write(f"T_marcs = {T_marcs}\n")
                f.write(f"log_g = {log_g}\n")
                f.write(f"log_g_marcs = {log_g_marcs}\n")
                f.write("magband = 'J'\n")
                f.write(f"mag = {mag}\n")
                f.write(f"Vmag = {Vmag}\n")
                f.write(f"Imag = {Imag}\n")
                f.write(f"airmass = {am}\n")
                f.write(f"pwv = {pw}\n")
                f.write(f"see = {see}\n")
                f.write(f"harps = '{harps_mode}'\n")
                f.write(f"nirps = '{nirps_mode}'\n")
                f.write(f"Vsys = {Vsys}\n")
                f.write(f"calc_pb = 'N'\n")

            del np, os, ExoFile, data
            for var in list(locals()):
                del locals()[var]
            for var in list(globals()):
                del globals()[var]    
            break
        else:
            print("Invalid input.")
    return
