Requirements:

Files in this folder
Python 3.0 or higher
And interest in astronomy!

Steps: 

To run the simulation, follow the following steps:

1. First edit the parameters in the input_file.py

name = 'name of the planet'
T = star temperature in K
magband = 'Magnitude band name: Eg: J'
mag = magnitude value
airmass = airmass from 1 to 2.9 
pwv = precipitable water vapour in mm. Choose one of the following [0.05, 0.10, 0.25, 0.50, 1.00, 1.50, 2.00, 2.50, 3.50, 5.00, 7.50, 10.00, 20.00, 30.00]
harps = 'ham/eggs mode'
nirps = 'he/ha mode'
R_s = radius of star in solar radii
M_s = mass of star in solar masses
Vsys = radial velocity of the system in km/s
R_p = radius of planet in Jupiter radius
M_p = mass of planet in Jupiter mass. If the planet mass is not known enter M_p = 0 and enter the Mp sin i value in the mpsini column. 
inc = inclination in degrees
mpsini = M_p Sin i. Used if the mass is not known.
w = argument of periastron should be given in radians
P = orbital period in days
a = semi major axis in AU
ecc = eccentricity 
b = impact parameter. If not known, enter 0.

Example of filled input_file.py is shown below.

name = 'WASP-121b'
T = 6460
magband = 'J'
mag = 9.625
airmass = 1.2
pwv = 2.66 
harps = 'ham'
nirps = 'he'
R_s = 1.458
M_s = 1.353
Vsys = 38.4
R_p = 1.81
M_p = 1.184
inc = 87.6
mpsini = 0.0
w = 0.0
P = 1.275
a = 0.02544
ecc = 0.0
b = 0.073 

2. Once the input file is ready, run the simulation using ERC_HARPS_NIRPS.py file.

In terminal:
python ETC_HARPS_NIRPS.py 

In iPython 
run ETC_HARPS_NIRPS.py 

The output files are stored in Outputs folder with a sub-folder for the planet name. Inside that, you can find a figure of SNR and Planetary Blur vs Exp. Time. And also the same data in a text file.


Other details:

In the file ETC_HARPS_NIRPS.py, you can change the upper-limit (or lower-limit) in the exposure time calculator by changing the line: exp = np.arange(10, 1500, 60)

Also, the calculations for Planetary Blur can also be edited in the successive lines in the same file.

Cheers
Vignesh

