#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script will read the json output of ETC 2.0 and create a number of plots.

Created on Thu Jun  4 10:02:28 2020
@author: Henri Boffin

Updated Fri Jun 10 2022:
Jakob Vinther
- changed np.int() to int()
- changed default input file name from etc-data.json to plot-data.json
- appending ".ascii" extension to the output files
- changed some internal variable names
- added console print indicating when the pylab plot window is opened
"""

import json
import numpy as np
import pylab as plt
import pathlib
import sys

# define figure size here...
plt.figure(figsize=[7., 10.])

# assume the name of the file as downloaded from ETC. Otherwise edit this.
json_file = './plot-data.json'

# can also provide a different file name on the command line
try:
    json_file = sys.argv[1]
except:
    pass

# checking that the file exists
path = pathlib.Path(json_file)
if not path.exists():
    print("file", json_file, " does not exist!")
    sys.exit()

# read file
with open(json_file, 'r') as myfile:
    data = myfile.read()

# parse file
obj = json.loads(data)

# get the numbers of groups of plots they are
npanels = (len(obj["ypanels"]))
print("You have ", npanels, " group(s) of plots")

# get the numbers of subplots for each group of plots
nsu0 = []
for i in range(npanels):
    nsu0 = np.append(nsu0, int(len(obj["ypanels"][i]["seriesArray"])))
nsu = nsu0.astype(int)
nsub = int(np.sum(nsu))
print("You will have", nsub, " plot(s) in total")

# Get the label for the X-axis
t = obj["xaxis"]["title"]
u = obj["xaxis"]["unit"]
xl = t + " (" + u + ")"

for pa in range(npanels):

    for paa in range(nsu[pa]):

        # index for the subplot
        nsub1 = nsub * 100 + 10 + pa + paa + 1

        # number of datasets
        ndst = len(obj["ypanels"][pa]["seriesArray"][paa]["detectors"])

        plt.subplot(nsub1)

        X = []
        Y = []
        for i in range(ndst):
            x = obj["xaxis"]["detectors"][i]["data"]
            X = np.append(X, x)
            y = obj["ypanels"][pa]["seriesArray"][paa]["detectors"][i]["data"]
            Y = np.append(Y, y)
            plt.plot(x, y)

        # Let us save the data as well...
        Z = np.array([X, Y])
        filename = 'plotdata' + '_' + str(pa) + '_' + str(paa) + '.ascii'
        np.savetxt(filename, Z.T, fmt='%s')
        print('File ', filename, ' has been written')

        t = obj["ypanels"][pa]["title"]
        u = obj["ypanels"][pa]["unit"]
        label = ''
        try:
            label = obj["ypanels"][pa]["seriesArray"][paa]["label"]
        except KeyError:
            pass

        # use ylabel = t if you prefer title than label on yaxis
        ylabel = label
        # uncomment next 2 lines if you want to also have the units in the ylabel
        #          if (u) :
        #               ylabel = label+"("+u+")"

        plt.xlabel(xl)
        plt.ylabel(ylabel)

plt.tight_layout()
print("opening plot window")
plt.show()

