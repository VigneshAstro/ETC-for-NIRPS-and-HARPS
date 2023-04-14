#!/usr/bin/env python3

import sys
import json
import argparse
import textwrap


def write_detector(params):

    detector = params.get('detector')

    # wavelength x
    x = detector['data']['wavelength']['wavelength']['data']

    # convert the wavelength from m to nm:
    # x[:] = [t * 1e9 for t in x]
    for groupkey in detector['data'].keys():
        
        if(groupkey != 'wavelength'):
            # the PSF profile is a function of angle
            if(groupkey == 'psf'):
                xpsf = detector['data']['psf']['angle']['data']
                ypsf = detector['data']['psf']['psf']['data']
                writefile(params, groupkey, '', xpsf, ypsf)

            # everything else are functions of wavelength x
            else:
                for serieskey in detector['data'][groupkey]:
                    if isinstance(detector['data'][groupkey][serieskey], dict):
                        if 'data' in detector['data'][groupkey][serieskey].keys():
                            y = detector['data'][groupkey][serieskey]['data']
                            writefile(params, groupkey, serieskey, x, y)


def writefile(params, groupkey, serieskey, x, y):

    prefix = params.get('prefix')
    detector = params.get('detector')
    # may not be present in the params dict
    ordername = params.get('ordername')
    sep = params.get('separator')
    labelsep = params.get('labelseparator')

    outputfilename = prefix

    if ordername:
        outputfilename = outputfilename + \
            sep + "order" + labelsep + ordername

    outputfilename = outputfilename + \
        sep + "det" + labelsep + detector['name'] + \
        sep + groupkey

    if serieskey != '':
        outputfilename += sep + serieskey

    outputfilename += ".ascii"

    with open(outputfilename, 'w') as of:
        for xx, yy in zip(x, y):
            of.write(f"{xx} {yy}\n")
        if params.get('verbose'):
            print(outputfilename)


def main():
    parser = argparse.ArgumentParser(
        description='Extract data from a given JSON file, such as the output from etc_cli.py\n'
        + 'Write the wavelength and data into columns in an ASCII file.\n'
        + 'Output files names are prefixed with the input file name by default, but can be\nchanged with the -p option.',
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('inputfilename',
                        help="Input JSON file, which is output from an ETC")

    parser.add_argument('-p', '--prefix', dest='prefix',
                        help='output file name prefix to use instead of the default\nwhich is the input file name')

    parser.add_argument('-s', '--separator', dest='separator', default='_',
                        help='separator string in the constructed output file name')

    parser.add_argument('-l', '--labelseparator', dest='labelseparator', default=':',
                        help='separator string between labels (ordername/detectorname)\n'
                        + 'and their values in the file names, e.g. "det-1" instead of default "det:1"')

    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='print the output file names')

    args = parser.parse_args()

    if(args.prefix):
        prefix = args.prefix
    else:
        prefix = args.inputfilename

    with open(args.inputfilename) as f:
        data = json.load(f)
        if 'orders' in data['data'].keys():
            for order in data['data']['orders']:
                for detector in order['detectors']:
                    write_detector({'prefix': prefix, 'ordername': order['order'], 'detector': detector,
                                    'verbose': args.verbose, 'separator': args.separator, 
                                    'labelseparator': args.labelseparator})
        else:
            for detector in data['data']['detectors']:
                write_detector({'prefix': prefix,
                                'detector': detector, 'verbose': args.verbose, 'separator': args.separator, 
                                'labelseparator': args.labelseparator})

if __name__ == '__main__':
    main()
