#!/usr/bin/env python
# encoding: utf-8

# Inchk
#
# Test an interwebz connection with the quickness
# By Jesse Wallace (@c0deous)

# < BEGIN SETTINGS > #

# Most reliable host
main_icmp_host = 'google.com'

# If main_icmp_host is MIA > ping this to determine if your DNS server of choice is down 
main_icmp_dns_host = '8.8.8.8'

# These will be pinged when this utility is run with the -f option.  
secondary_icmp_hostnames = ['apple.com', 'youtube.com', 'netflix.com'] #NYI

# < END SETTINGS > #

import os, sys, socket, struct, time, pyping, optparse

def get_default_gateway():
    """Read the default gateway directly from /proc."""
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue

            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def txtclr(text, color):
    colorcode = getattr(bcolors, color)
    return colorcode + text + bcolors.ENDC

class ssb:
	working = txtclr("[*]", "OKBLUE")
	success = txtclr("[+]", "OKGREEN")
	warning = txtclr("[!]", "WARNING")
	fail = txtclr("[-]", "FAIL")

def main():
	print(txtclr("Inchk 2.1 Copyright 2016 Jesse Wallace", "HEADER"))
	if options.foption != True:
                # Test 1 - Main Host
                try:
		    print("%s Testing %s ..." % (ssb.working, main_icmp_host))
		    ping_t1 = pyping.ping(main_icmp_host)
                    # Will raise unknown_host here if unsuccessful
                    print('%s Successfully reached %s!' % (ssb.success, main_icmp_host))
                    if float(ping_t1.avg_rtt) >= 110.0:
                         print('%s Average response time is abnormally high' % (ssb.warning))
                    elif float(ping_t1.avg_rtt) >= 90.0:
                         print('%s Average response time is high' % (ssb.warning))
                    synopsis([ping_t1, 'N/A', 'N/A'], [txtclr('Successful', 'OKGREEN'), 'N/A', 'N/A'], 'Good connection')
                    exit()
                except socket.error as se:
                    print(' ')
                    print('%s Socket Error: %s' % (ssb.fail, se))
                    exit()
                except (Exception, 'unknown_host'):
                    print('%s Couldn\'t reach %s ...' % (ssb.fail, main_icmp_host))

                # Test 2 - Main DNS
                try:
                    print('%s Testing %s ...' % (ssb.working, main_icmp_dns_host))
                    ping_t2 = pyping.ping(main_icmp_dns_host)
                    # Will raise unknown_host here if unsuccessful
                    print('%s Successfully reached %s!' %s (ssb.success, main_icmp_dns_host))
                    if float(ping_t2.avg_rtt) >= 110.0:
                         print('%s Average response time is abnormally high' % (ssb.warning))
                    elif float(ping_t2.avg_rtt) >= 90.0:
                         print('%s Average response time is high' % (ssb.warning))
                    synopsis([ping_t1, ping_t2, 'N/A'], [txtclr('Failed', 'FAIL'), txtclr('Successful', 'OKGREEN'), 'N/A'], 'Your DNS server is reachable but may not be serving DNS requests correctly')
                    exit()
                except (Exception, 'unknown_host'):
                    print('%s Couldn\'t reach %s ...' % (ssb.fail, main_icmp_dns_host))
                # Test 3 - Local Gateway
                try:
                    defaultgateway = get_default_gateway()
                    print('%s Testing local gateway %s ...' % (ssb.working, defaultgateway))
                    ping_t3 = pyping.ping(defaultgateway)
                    # Will raise unknown_host here if unsuccessful
                    print('%s Successfully reached local gateway %s' % (ssb.working, defaultgateway))
                    if float(ping_t3.avg_rtt) >= 15.0:
                        print('%s Average response time is abnormally high' % (ssb.warning))
                    elif float(ping_t3.avg_rtt) >= 5.0:
                        print('%s Average response time is high' % (ssb.warning))
                    synopsis([ping_t1, ping_t2, ping_t3], [txtclr('Failed', 'FAIL'), txtclr('Failed', 'FAIL'), txtclr('Successful', 'OKGREEN')], 'Your LAN is not connected to the WAN')
                    exit()
                except (Exception, 'unknown_host'):
                    print('%s Couldn\'t reach %s ...' % (ssb.fail, defaultgateway))
                synopsis(['N/A', 'N/A', 'N/A'], ['N/A', 'N/A', 'N/A'], 'You are not connected to a functional LAN')

def synopsis(pingobjs, conclusion, statement):
    print('Network Synopsis: %s' % (statement))
    if conclusion[0] != 'N/A':
        print('  Main Connection: %s' % (conclusion[0]))
        print('    Max Response: %s ms' % (pingobjs[0].max_rtt))
        print('    Min Response: %s ms' % (pingobjs[0].min_rtt))
        print('    Avg Response: %s ms' % (pingobjs[0].avg_rtt))
    if conclusion[1] != 'N/A':
        print('  DNS Connection: %s' % (conclusion[1]))
        print('    Max Response: %s ms' % (pingobjs[1].max_rtt))
        print('    Min Response: %s ms' % (pingobjs[1].min_rtt))
        print('    Avg Response: %s ms' % (pingobjs[1].avg_rtt))
    if conclusion[2] != 'N/A':
        print('  Local Gateway Connection: %s' % (conclusion[2]))
        print('    Max Response: %s ms' % (pingobjs[2].max_rtt))
        print('    Min Response: %s ms' % (pingobjs[2].min_rtt))
        print('    Avg Response: %s ms' % (pingobjs[2].avg_rtt))

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-f', action='store_true', default=False, dest="foption") # NYI

    (options, args) = parser.parse_args()

    main()


""" Copyright 2016 Jesse Wallace (@c0deous) - business@c0deo.us

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
