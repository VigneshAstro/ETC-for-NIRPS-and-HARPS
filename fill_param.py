from exofile.archive import ExoFile
import numpy as np

def fill_params():
    while True:
        input_filled = input("Are the input parameters filled? (Y/N): ")
        if input_filled == 'Y':
            break
        elif input_filled == 'N':
            planet_name = input("Please enter the planet's name: ")
            nirps_mode = input("Please enter NIRPS mode HA/HE (eg: he): ")
            harps_mode = input("Please enter HARPS mode ham/eggs (eg: ham): ")
            am = input("Please enter airmass (between 1 - 2.9): ")
            pw = input("Please enter precipitable water vapour in mm (between 0.05 - 30): ")
            data = ExoFile.load()
            name = str(data.by_pl_name(planet_name)['pl_name']).strip()
            T = float(data.by_pl_name(planet_name)['st_teff'])
            mag = float(data.by_pl_name(planet_name)['sy_jmag'])
            # R_s = float(data.by_pl_name(planet_name)['st_rad'])
            R_rat = float(data.by_pl_name(planet_name)['pl_ratror'])
            M_s = float(data.by_pl_name(planet_name)['st_mass'])
            Vsys = float(data.by_pl_name(planet_name)['st_radv'])
            R_p = float(data.by_pl_name(planet_name)['pl_radj'])
            M_p = float(data.by_pl_name(planet_name)['pl_bmassj'])
            inc = float(data.by_pl_name(planet_name)['pl_orbincl'])
            mpsini = float(data.by_pl_name(planet_name)['pl_bmassj'])
            W = float(data.by_pl_name(planet_name)['pl_orblper'])
            w = np.radians(W) # converting to radians
            P = float(data.by_pl_name(planet_name)['pl_orbper'])
            a = float(data.by_pl_name(planet_name)['pl_orbsmax'])
            ecc = float(data.by_pl_name(planet_name)['pl_orbeccen'])
            b = float(data.by_pl_name(planet_name)['pl_imppar'])
            T0 = float(data.by_pl_name(planet_name)['pl_tranmid'])
            # set NaN values to 0
            T = 0 if np.isnan(T) else T
            mag = 0 if np.isnan(mag) else mag
            R_rat = 0 if np.isnan(R_rat) else R_rat
            M_s = 0 if np.isnan(M_s) else M_s
            Vsys = 0 if np.isnan(Vsys) else Vsys
            R_p = 0 if np.isnan(R_p) else R_p
            M_p = 0 if np.isnan(M_p) else M_p
            inc = 0 if np.isnan(inc) else inc
            mpsini = 0 if np.isnan(mpsini) else mpsini
            w = 0 if np.isnan(w) else w
            P = 0 if np.isnan(P) else P
            a = 0 if np.isnan(a) else a
            ecc = 0 if np.isnan(ecc) else ecc
            b = 0 if np.isnan(b) else b
            T0 = 0 if np.isnan(T0) else T0
            with open('input_file.py', 'w') as f:
                f.write(f"name = '{planet_name}'\n")
                f.write(f"T = {T}\n")
                f.write("magband = 'J'\n")
                f.write(f"mag = {mag}\n")
                f.write(f"airmass = {am}\n")
                f.write(f"pwv = {pw}\n")
                f.write(f"harps = '{harps_mode}'\n")
                f.write(f"nirps = '{nirps_mode}'\n")
                f.write(f"R_rat = {R_rat}\n")
                f.write(f"M_s = {M_s}\n")
                f.write(f"Vsys = {Vsys}\n")
                f.write(f"R_p = {R_p}\n")
                f.write(f"M_p = {M_p}\n")
                f.write(f"inc = {inc}\n")
                f.write(f"mpsini = {mpsini}\n")
                f.write(f"w = {w}\n")
                f.write(f"P = {P}\n")
                f.write(f"a = {a}\n")
                f.write(f"ecc = {ecc}\n")
                f.write(f"b = {b}\n")
                f.write(f"T0 = {T0}\n")
            break
        else:
            print("Invalid input.")
