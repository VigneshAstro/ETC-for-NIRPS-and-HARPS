#!/usr/bin/env python3

import sys
import requests
import json
import argparse


def collapse(jsondata):

    def goThrough(x):
        if isinstance(x, list):
            return goThroughList(x)
        elif isinstance(x, dict):
            return goThroughDict(x)
        else:
            return x

    def goThroughDict(dic):
        for key, value in dic.items():
            if isinstance(value, dict):
                dic[key] = goThroughDict(value)
            elif isinstance(value, list):
                dic[key] = goThroughList(value)
        return dic

    def goThroughList(lst):
        if not any(not isinstance(y, (int, float)) for y in lst):  # pure numeric list
            if len(lst) <= 2:
                return lst
            else:
                return '['+str(lst[0]) + ' ... '+str(lst[-1])+'] ('+str(len(lst))+')'
        else:
            return [goThrough(y) for y in lst]

    return goThroughDict(jsondata)


def callEtc(postdata, url, uploadfile=None):

    # TODO! workaround until we figure put how to handle ssl certificate correctly
    import warnings
    warnings.filterwarnings('ignore', message='Unverified HTTPS request')

    if uploadfile is None:
        try:
            return requests.post(url,
                              data=json.dumps(postdata),
                              headers={'Content-Type': 'application/json'},
                              verify=False,
                              )
        except Exception as e:
            print('Post request with upload returned error:' + str(e))
            sys.exit()
    else:
        try:
            return requests.post(url,
                              data={"data": json.dumps(postdata)},
                              files={"target": open(uploadfile, 'rb')},
                              verify=False)
        except Exception as e:
            print('Post request returned error:' + str(e))
            sys.exit()

def output(jsondata, args):

    if args.collapse:
        jsondata = collapse(jsondata)

    if args.outputfile:
        with open(args.outputfile, "w") as of:
            of.write(json.dumps(jsondata, indent=args.indent))
    else:
        print(json.dumps(jsondata, indent=args.indent))


def getEtcUrl(etcname):
    if '4most' in etcname.lower() or 'qmost' in etcname.lower() or 'fourmost' in etcname.lower():
        return 'Qmost/'
    elif 'crires' in etcname.lower():
        return 'Crires2/'
    else:  # normal case
        return etcname.lower().capitalize() + '/'


def getPostdata(instrument_name, postdatafile):
    """ normaly returning the postdata without modification but
    handle special cases when the postdata has sections for two
    instruments in one request e.g. (HARPS/NIRPS)"""

    try:
        with open(postdatafile) as f:
            postdata = json.loads(f.read())
    except OSError:
        print('cannot open', postdatafile)
        sys.exit()

    if "instrument" in postdata and instrument_name in postdata["instrument"]:
        postdata["instrument"] = postdata["instrument"][instrument_name]

    # normaly returning the postdata without modification
    return postdata

def main():
    parser = argparse.ArgumentParser(
        description='Call an ETC with input parameters and optionally an uploaded spectrum.\n'
        + 'Print the resulting JSON on stdout or optionally a file.\n'
        + 'Examples: \n'
        + './etc_cli.py 4most input.json -o output1.json\n'
        + './etc_cli.py 4most input.json -u upload.dat -o output2.json\n'
        + './etc_cli.py 4most input.json -s https://etc.eso.org -o output3.json',
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('etcname',
                        help='Name of instrument ETC to call, e.g. 4most')

    parser.add_argument('postdatafile',
                        help='Name of JSON file with ETC input parameters,\nlike the ETC input form')

    parser.add_argument('-u,', '--upload', dest="uploadfile",
                        help='Name of file with spectrum to upload.\nSee https://etc.eso.org/observing/etc/doc/upload.html')

    parser.add_argument('-c', '--collapse', action='store_true',
                        help='collapse output JSON data arrays to a short indicative strings')

    parser.add_argument('-i', '--indent', type=int, nargs='?', const=4,
                        help='Format the output JSON with indentation (default 4)')

    parser.add_argument('-o', '--outputfile', dest="outputfile",
                        help='Send the output to file')

    parser.add_argument('-s', '--server', dest="server", default='https://etc.eso.org',
                        help='specific alternative backend web server')

    args = parser.parse_args()

    # ETC backend server
    supported_servers = ['https://etc.eso.org',
                         'https://etctestpub.eso.org',
                         'https://etctest2.hq.eso.org',
                         'https://etctest.hq.eso.org',
                         'http://localhost:8000'
                        ]
    if args.server in supported_servers:
        baseurl = args.server + '/observing/etc/etcapi/'
    else:
        print('not supported: '+args.server)
        print('supported servers:\n')
        print(*supported_servers, sep='\n')
        sys.exit(1)

    url = baseurl + getEtcUrl(args.etcname)

    postdata = getPostdata(args.etcname, args.postdatafile)  # prepare input
    jsondata = callEtc(postdata, url, args.uploadfile).json()  # output

    output(jsondata, args)


if __name__ == "__main__":
    main()
