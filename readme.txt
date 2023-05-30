Requirements:

Files in this folder
Python 3.0 or higher
Exofile package (Antoine Farveau GitHub)
Steps: 

To run the simulation, follow the following steps:

1. First we need to install ExoFile from Antoine Darveau's GitHub: https://github.com/AntoineDarveau/exofile in the same folder (working directory) where you are downloading these files. 

That folder in this working directory should be named exofile. 

We will be using this to obtain the exoplanet's parameters from the NASA Exoplanet Archive (https://exoplanetarchive.ipac.caltech.edu/).

2. Download all the files from this GitHub: 

Running the code: 

In terminal:
python ETC_HARPS_NIRPS.py 

Using iPython 
run ETC_HARPS_NIRPS.py 

The code asks few parameters from the user:
Example:

(A). Calculate Planetary Blur? (Y/N): 

Press Y, if the planetary blur needs to be calculated.
Press N, if the radius is not known or planetary blur is not needed.

(B). Are the input parameters filled? (Y/N): 

If you have already filled the input parameter file (input_file.txt) enter Y here.
If not enter N.

(C). Please enter the planet's name: or Please enter the star's name:

Please enter the planet name in the standard form:  example WASP-121 b (or) TRAPPIST-1 b (or) HD 209548 b. Or Star name like WASP-121 (or) TRAPPIST-1 (or) HD 209548.

(D). Please enter NIRPS mode HA/HE (eg: he): 
(E). Please enter HARPS mode ham/eggs (eg: ham): 

Please enter which mode you want to observe in HARPS and NIRPS.

(F). Please enter airmass (between 1 - 2.9): 
(G). Please enter precipitable water vapour in mm (between 0.05 - 30): 
(H). Please enter the turbulent condition[TC] (10% (i.e. seeing<=0.5 arcsec), 20% (<=0.6), 30% (<=0.7), 50% (<=0.8), 70% (<=1.0), 85% (<=1.3), 100% (<=2)) :

Please enter the atmospheric conditions as requested. Example, if the seeing condition you want to observe in is around 1 arcsec, then please enter 70.

After entering this, the code uses fill_param.py or fill_param_no_pb.py to fill the input_file.txt
Alternatively, you can fill this file manually. The details of the input file are below.

name = 'name of the planet'
T = star temperature in K
magband = 'Magnitude band name: Eg: J' Here J band is fixed as it is ideal in NIR (For NIRPS)
mag = magnitude value of J band
Vmag = V-band Magnitude value
Imag = I-band magnitude, computed from V-Ic relation (link: https://www.pas.rochester.edu/~emamajek/EEM_dwarf_UBVIJHK_colors_Teff.txt)
airmass = airmass from 1 to 2.9 
pwv = precipitable water vapour in mm. Choose one of the following [0.05, 0.10, 0.25, 0.50, 1.00, 1.50, 2.00, 2.50, 3.50, 5.00, 7.50, 10.00, 20.00, 30.00]
harps = 'ham/eggs mode'
nirps = 'he/ha mode'
R_rat = radius ratio of planet to star
M_s = mass of star in solar masses
Vsys = radial velocity of the system in km/s
R_p = radius of planet in Jupiter radius
M_p = mass of planet in Jupiter mass. If the planet mass is not known enter M_p = 0 and enter the Mp inc = inclination in degrees.
mpsini = M_p Sin i. Used if the mass is not known, else 0.
w = argument of periastron should be given in degrees
P = orbital period in days
a = semi major axis in AU
ecc = eccentricity 
b = impact parameter. If not known, enter 0.
T0 = mid transit time in BJD.
calc_pb = Y/N for calculation of planetary blur

Example of filled input_file.txt is shown below.

name = 'WASP-127 b'
T = 5620.0
magband = 'J'
mag = 6.591
Vmag = 7.65
Imag = 7.1134829731745395
airmass = 1.2
pwv = 2.5
harps = 'ham'
nirps = 'he'
R_rat = 0.10103
M_s = 0.95
Vsys = -8.25
R_p = 1.311
M_p = 0.1647
inc = 87.84
mpsini = 0.1647
w = 0
P = 4.17806203
a = 0.0484
ecc = 0
b = 0.29
T0 = 2456776.62124
calc_pb = 'Y'

Note: The input_file.txt might have lesser parameters, if the planetary blur (PB) calculation is not requested.

Once the input file is ready, the code computes the SNR for exposure times unto 1500s with increment of 60s. The calculations for Planetary Blur is followed after this.


The output files are stored in Outputs folder with a sub-folder for the planet name. Alternatively, you can also provide the path of the outputs file you want to store. Inside that, you can find a figure of SNR and Planetary Blur vs Exp. Time. And the maximum SNR during transit (Note: this is calculated only when PB is requested). And also the same data in a text file. 

Other details:

In the file ETC_HARPS_NIRPS.py, you can change the upper-limit (or lower-limit) in the exposure time calculator by changing the line: exp = np.arange(0, 1500, 60). The calculations for Planetary Blur can also be edited in the file blur_cal.py

More help on ExoFIle: https://github.com/AntoineDarveau/exofile
More help on ESO ETC 2.0 files: https://etc.eso.org/observing/etc/home search tools.


Files on this folder (apart from Exofile)

blur_cal.py 
calculations.py
etc_cli.py
ETC_Estimator_ipython_script.ipynb
ETC_HARPS_NIRPS.py
etc_json2ascii.py
etc_plotreader.py
etc-form.json
fill_param_no_pb.py
fill_param.py
input_file.txt
read_input_file.py
readme.txt
rv_calculator.py

Cheers
Vignesh

