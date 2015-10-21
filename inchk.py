# Inchk.py
# Script to quickly check for an internet connection
# Requires ANSI to be enabled for colors to work
# By Jesse Wallace (c0deous)
# jessewallace.net

# Load Libraries #
import os, sys, optparse, socket, struct, time

# ----------------Settings----------------------- #

# This should be your most reliable host.  Google.com is probably the best.
main_icmp_host = 'google.com'

# This should be your DNS Server.  If main_icmp_hostname does not respond we will test this to determine if your DNS server of choice is down 
main_icmp_dns_host = '8.8.8.8' # 8.8.8.8 is Google's public DNS service.

# These will be pinged when this utility is run with the -f option.  
secondary_icmp_hostnames = ['apple.com', 'youtube.com', 'netflix.com'] # Add as many as you want just in quotations and separted by a comma and a space. #NYI

# Default Interfaces (get using ifconfig)
interfaces = ['wlan0', 'eth2', 'lo'] # List all interfaces in order of most used to least used

# Default ping packets to send
normal_ping_packetcount = 1
foption_ping_packetcount = 10 # When using -f option it will ping this many times #NYI

# Parse CLI Options
parser = optparse.OptionParser()
parser.add_option('-f', action='store_true', default=False, dest="foption") # NYI

(options, args) = parser.parse_args()



# Functions #
def ping(host, pingtimes, interface):
	try: 
		pingtimes = int(pingtimes)
	except ValueError:
		print(ssb.fail + " Encountered a ValueError when setting pingtimes (pingtimes must be an integer and wasn't)")
		exit()

	if pingtimes == 0:
		response = os.system('ping -c 3 -I ' + str(interface) + ' ' + str(host) + ' > /dev/null 2>&1')
		time.sleep(5)
	else:
		response = os.system('ping -c ' + str(pingtimes) + ' -I ' + str(interface) + ' ' + str(host) + '  > /dev/null 2>&1')
		time.sleep(5)
	if response == 0:
		return True
	else:
		return False

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
	def synopsis():
		pass
	print(txtclr("Inchk 1.0 Copyright 2015 Jesse Wallace", "HEADER"))
	if options.foption != True:
		print(ssb.working + " Testing pingable hostname " + main_icmp_host + " ...")
		ping_t1 = ping(main_icmp_host, normal_ping_packetcount, interfaces[0])
		if ping_t1 == True:
			print(ssb.success + " Connection to main host successful!")
			main_icmp_connection = True
			synopsis()
			exit()
		else:
			print(ssb.fail + " Could not ping main ICMP host (" + main_icmp_host + ")...")
			main_icmp_connection = False
			# Pingtest 2 #
			print(ssb.working + " Testing IPv4 Host " + main_icmp_dns_host +  " ...")
			ping_t2 = ping(main_icmp_dns_host, normal_ping_packetcount, interfaces[0])
			if ping_t2 == True:
				print(ssb.success + " Connection to IPv4 host successful!")
				main_ipv4_connection = True
				print(ssb.warning + " You are connected to the internet but your current DNS servers don't seem to be working.")	
				print(ssb.warning + " Check /etc/resolv.conf to make sure your nameservers are correct")
				print(ssb.working + " Confirming with nslookup...")
				nsl = os.system('nslookup ' + main_icmp_host + ' ' + main_icmp_dns_host)
				if nsl != 0:
					print(ssb.fail + " Confirmed DNS server is down!")
					main_icmp_dns_resolve = False
					synopsis()
					exit()
				elif nsl == 0:
					print(ssb.success + " Successfully resolved hostname...")
					print(ssb.fail + " This is an issue this program cannot detect")
					print(ssb.fail + " You cannot ping your DNS server but you can resolve hostnames... This should never happen")
					main_icmp_dns_resolve = True
					synopsis()
					exit()
			else:
				print(ssb.fail + " Could not ping main IPv4 host (" + main_icmp_dns_host + ")...")
				main_ipv4_connection = False
				print(ssb.warning + " There is a good chance that you aren't connected to the internet...")
				print(ssb.working + " Testing local gateway...")
				gateway = get_default_gateway()
				ping_t3 = ping(gateway, normal_ping_packetcount, interfaces[0])
				if ping_t3 == True:
					print(ssb.success + " Connection to local gateway " + str(gateway) + " successful!")
					print(ssb.working + " You are on a local only network.  There is no external internet connection.")
					local_ipv4_connection = True
					synopsis()
					exit()
				else:
					print(ssb.fail + " Could not ping local gateway " + str(gateway) + "...")
					print(ssb.warning + " You don't seem to be connected to a functional network.")
					synopsis()
					exit()
	else:
		print(ssb.fail + " -f option not yet implemented")
		exit()		

if __name__ == "__main__":
	main()


""" Copyright 2015 Jesse Wallace (c0deous)
    c0deous.business@gmail.com

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
