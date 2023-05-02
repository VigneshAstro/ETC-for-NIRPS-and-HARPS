def fill_params_no_pb():
    import os
    import numpy as np
    from exofile.archive import ExoFile
    while True:
        input_filled = input("Are the input parameters filled? (Y/N): ")
        if input_filled == 'Y':
            del np, os, ExoFile, data
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
            mag = float(data.by_pl_name(star_name)['sy_jmag'])            
            Vsys = float(data.by_pl_name(star_name)['st_radv'])

            # set NaN values to 0
            T = 0 if np.isnan(T) else T
            mag = 0 if np.isnan(mag) else mag
            Vsys = 0 if np.isnan(Vsys) else Vsys

            # with open('input_file.txt', 'w') as f:
            with open(os.path.join(os.path.dirname(__file__), 'input_file.txt'), 'w') as f:
                f.write(f"name = '{star_name}'\n")
                f.write(f"T = {T}\n")
                f.write("magband = 'J'\n")
                f.write(f"mag = {mag}\n")
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
