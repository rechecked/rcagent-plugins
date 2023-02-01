#!/bin/python3

import sys
import argparse
import traceback
import ssl
import json
import urllib.error
import urllib.parse
import urllib.request

VERSION = "1.0.0"

def parseArgs():
    
    parser = argparse.ArgumentParser(description="Plugin used to make active checks against an rcagent.")
    parser.add_argument("-H", "--hostname", help="The hostname of the rcagent host.")
    parser.add_argument("-p", "--port", type=int, default=5995, help="The port to connect to. Defaults to 5995.")
    parser.add_argument("-M", "--metric", help="The metric (api endpoint) that you want to check against.")
    parser.add_argument("-P", "--plugin", help="Plugin to run on the rcagent host.")
    parser.add_argument("-t", "--token", help="The token to access rcagent defined in the rcagent's config file.")
    parser.add_argument("-w", "--warning", help="The warning value to check against.")
    parser.add_argument("-c", "--critical", help="The critical value to check against.")
    parser.add_argument("-d", "--delta", help="Time between calls. Some checks require delta time (in seconds).")
    parser.add_argument("-u", "--units", help="Change units to a type: B, kB, KiB, MB, MiB, GB, GiB, TB, TiB. Default set in cagent config.")
    parser.add_argument("-l", "--protocol", default="https", help="Whether to use 'http' or 'https'. Defaults to https.")
    parser.add_argument("-k", "--secure", action="store_true", help="Verify the host SSL certificate. Defaults to false.")
    parser.add_argument("-v", "--version", action="store_true", help="Print plugin version number.")
    parser.add_argument("-D", "--debug", action="store_true", help="Turn on debug mode to print out lots of extra info for debugging.")
    args = parser.parse_args()

    # Verify protocol
    protos = ["http", "https"]
    if args.protocol not in protos:
        parser.error("Protocol must be one of: http, https")

    # Verify hostname
    if not args.hostname:
        parser.error("Hostname is required")
    
    # Verify metric
    if not args.metric and not args.plugin:
        parser.error("Must enter a plugin or a metric")

    if args.plugin:
        args.metric = "plugins"

    return args

def createURL(args):
    host = args.hostname
    port = args.port
    protocol = args.protocol
    metric = urllib.parse.quote(args.metric)
    url = "%s://%s:%s/api/%s" % (protocol, host, port, metric)
    return url

def getFullURL(args):
    url = createURL(args)
    urlArgs = {
        'token': args.token,
        'units': args.units,
        'check': 1,
        'warning': args.warning,
        'critical': args.critical,
        'delta': args.delta,
        'plugin': args.plugin
    }
    urlArgs = list((k, v) for k, v in list(urlArgs.items()) if v is not None)
    url = "%s?%s" % (url, urllib.parse.urlencode(urlArgs))
    return url

def getJSON(args):
    url = getFullURL(args)
    
    if args.debug:
        print("Request URL: " + url)

    # Create SSL context so we can ignore cert checks
    try:
        if args.protocol is "https":
            ctx = ssl.create_default_context()
            if not args.secure:
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
            ret = urllib.request.urlopen(url, context=ctx)
        else:
            ret = urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        return "UNKNOWN: %s" % e, 3
    except Exception as e:
        return "UNKNOWN: %s" % e, 3

    ret = ret.read()
    data = json.loads(ret)

    # Handle errors, if there are any
    if 'status' in data and data['status'] == "error":
        return "CRITICAL: %s" % data['message'], 2

    # Parse output
    output = data['output']

    # Add on perfdata if it exits
    if 'prefdata' in data and data['perfdata']:
        output = "%s | %s" % (output, data['perfdata'])

    # Add longoutput if it exits
    if 'longoutput' in data and data['longoutput']:
        output += " | %s" % data['longoutput']
    
    return output, data['exitcode']

def main():
    args = parseArgs()

    if args.version:
        print("check_rcagent.py, version: %s" % VERSION)
        sys.exit(0)

    stdout, exitcode = getJSON(args)

    print(stdout)
    sys.exit(exitcode)

if __name__ == "__main__":
    main()

