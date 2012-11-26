#!/usr/bin/python

import httplib, sys, urllib2, argparse

from bcolors import bcolors

parser = argparse.ArgumentParser(description='Check for IIS internal IP leakage. CALL TH AMBER LAMPS.')
parser.add_argument('host', metavar='www.asp.net', help='target host')
parser.add_argument('--dir', '-D', metavar='/exchange', default='', help='directory (optional)')
parser.add_argument('--port', '-P', metavar='xx', type=int, nargs='*', default='80', help='ports to test (default: 80)')
parser.add_argument('--timeout', '-T', metavar='s', type=int, default='30', help='request timeout in seconds (default: 30)')
parser.add_argument('--https', '-S', action="store_true", help='use https')
#parser.add_argument('--verbose', '-V', action="store_true", help='verbose output')

args = parser.parse_args()

protocol = 'https://' if args.https else 'http://'
args.port = [args.port] if type(args.port) is int else args.port

for port in args.port:

	uri = protocol + args.host + ":" + str(port) + args.dir

	
	print bcolors.OKBLUE + "\n\nURI: " + uri + bcolors.ENDC
	try:
	    response = urllib2.urlopen(uri, '', args.timeout)
	    print 'http status: ', str(response.getcode())
	    print 'response headers: "%s"' % response.info()

	except IOError, e:
	    if hasattr(e, 'code'): # HTTPError
	    	print 'http status: ', e.code
	        print 'response headers: ', e.hdrs
	    elif hasattr(e, 'reason'): # URLError
	        print bcolors.FAIL + "can't connect, reason: ", e.args, bcolors.ENDC
	    else:
	        raise


sys.exit