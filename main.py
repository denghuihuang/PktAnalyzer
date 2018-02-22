#!/usr/bin/env python

'''
Main program that analyze packet in pcap file.
'''

import os
import optparse
import logging
import sys
import json

from pktAnalyzer import pcap
from pktAnalyzer import http
from pktAnalyzer import httpsession
from pktAnalyzer import har
from pktAnalyzer import tcp
from pktAnalyzer import settings
from pktAnalyzer.packetdispatcher import PacketDispatcher
from pktAnalyzer.pcaputil import print_rusage


# get cmdline args/options
parser = optparse.OptionParser(
    usage='usage: %prog inputfile outputfile'
)

parser.add_option('-e', '--endpoint', action='store_true',
                  dest='endpoint', default=True)
parser.add_option('-l', '--log', dest='logfile', default='pktAnalyzer.log')
options, args = parser.parse_args()

# setup logs
logging.basicConfig(filename=options.logfile, level=logging.INFO)

# get filenames, or bail out with usage error
if len(args) == 2:
    inputfile, outputfile = args[0:2]
else:
    parser.print_help()
    sys.exit()

logging.info('Processing %s', inputfile)

# parse pcap file
dispatcher = pcap.EasyParsePcap(filename=inputfile, endpoint=options.endpoint)

# parse HAR stuff
session = httpsession.HttpSession(dispatcher)

logging.info('Flows=%d. HTTP pairs=%d' % (len(session.flows), len(session.entries)))

#write the HAR file
with open(outputfile, 'w') as f:
    json.dump(session, f, cls=har.JsonReprEncoder, indent=2, encoding='utf8', sort_keys=True)

if options.resource_usage:
    print_rusage()
