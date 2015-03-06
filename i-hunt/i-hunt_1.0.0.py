# Author: Nasa & Khizra (NK): This script is to collect IR data from iDevices
# Version: 1.0.0

import time 
import os
import sys
import os.path
import datetime
import socket
import subprocess
from subprocess import Popen, PIPE, STDOUT

# Defining colors
red = "\033[01;31m{0}\033[00m"
blue = "\033[1;34m{0}\033[00m"
aqua = "\033[1;36m{0}\033[00m"
green = "\033[1;32m{0}\033[00m" 

print aqua.format("[+] i-hunt starting...")
print green.format("[+] Please make sure that the device is jail-broken and OpenSSH is installed") 

# Setting up output folder name format
dirfmt = "%4d-%02d-%02d%02d:%02d:%02d_i-hunt_Collect/"
dirname = dirfmt % time.localtime()[0:6]

# Creating output folder at the location from where the script is running from
file = sys.argv[0]
drname = os.path.dirname(file)
abspath = os.path.abspath(drname)
directory = os.path.dirname(file)
abspath = os.path.abspath(directory)
fullpath = os.path.join(abspath, dirname)
#os.mkdir(fullpath, 0755)

# Finding IR_BINARIES folder
IRBINpath = os.path.join(abspath, "IR_BINARIES")
yn = os.path.isdir(IRBINpath)
if yn == False:
	print red.format("[+] Directory IR_BINARIES not found. This should be in the same location where your script is.") 
	exit()

# Getting input of the device's hostname 
hostIP = raw_input(blue.format("[+] Enter the host IP: "))
host = 'root@' + hostIP

# Checking if the given host information is valid
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((hostIP, 22))
    print green.format("[+] Host is reachable")
except socket.error as e:
    print red.format("[+] Error: %s" % e)
    exit()
s.close()


def IR():

	# Uploading the required binaries to the device for live data collection
	print green.format("[+] Uploading the necessary binaries at /usr/sbin/IR_BINARIES/ for live data collection")
	BINupld = Popen(['scp', '-r', IRBINpath, host + ':/usr/sbin/'], stdout=PIPE, stderr=PIPE)
	BINupld.wait()
	
	result = repr(BINupld.stderr.readline())
	
	# Print result
	if result == "''":
		print green.format("[+] Binaries uploaded")
	else:
		print ('Error: %s' % result)
		exit()

	# Creating Livelog folder 
	os.chdir(fullpath)
	os.mkdir(fullpath + '/Livelogs', 0755)
	IRdata = os.path.join(fullpath, 'Livelogs')

	ir = '/usr/sbin/IR_BINARIES/'
	cmd = ['who', 'date', 'uname -a', 'arp -a', 'df', 'ifconfig', 'pstree', 'lsof', 'netstat', 'ps', 'uptime', 'hostinfo']
	move = 'mv /usr/sbin/IR_BINARIES/libpcap* /usr/lib/'

	# Moving the lipcap libraries in the default location /usr/lib for tcpdump binary that can be run manually by the user
	ssh = subprocess.Popen(["ssh", host, move], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	ssh.wait()
	result = repr(ssh.stderr.readline())

	if result != "''":
		print red.format('Error: %s' % result)

	# Running the uploaded binaries
	for x in cmd:
		print x
		ssh = subprocess.Popen(["ssh", host, ir + x], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		result = str(ssh.stdout.readlines())
		f = open(IRdata + '/' + x, 'w')
		f.write (result)
		f.close()

def sshupload():

	# Uploading SSH key to the device to prevent entering passwords repeatedly

	print aqua.format("[+] Copying the public key to the device with the name authorized_keys at /var/root/.ssh/")
	keyupld = Popen(['scp', keypath, host + ':/var/root/.ssh/authorized_keys'], stdout=PIPE, stderr=PIPE)
	keyupld.wait()
	result = repr(keyupld.stderr.readline())
	
	if result == "''":
		print green.format("[+] Public key uploaded")
	else:
		print red.format('Error: %s' % result)
		exit()


def logcollect():

	# Creating Otherlog folder to save other log files from the device
	
	os.mkdir(fullpath + '/Otherlogs', 0755)
	otherlog = os.path.join(fullpath, 'Otherlogs')

	path1 = '/private/var/mobile/Library/Preferences'
	path2 = '/private/var/mobile/Library/Preferences'
	path3 = '/private/var/logs'
	path4 = '/private/var/mobile/Library/Logs/CrashReporter/DiagnosticLogs'
	path5 = '/private/var/root/Library/Caches/locationd'
	path6 = '/private/var/mobile/Library/MobileInstallation'
	path7 = '/private/var/mobile/Library/TCC'
	path8 = '/System/Library/LaunchDaemons'
	path9 = '/Library/LaunchDaemons'
	path10 = '/private/var/mobile/Library/Keyboard'
	path11 = '/private/var/mobile/Library/Cookies'
	path12 = '/private/var/preferences/SystemConfiguration/com.apple.wifi.plist'
	path13 = '/private/var/db/dhcpclient/leases'
	path14 = '/private/var/db/lsd'
	
	print green.format("[+] Please wait while it is copying log files from the device")

	logfile = Popen(['scp', '-r','-C', '-p', host+':{'+path1+','+path2+','+path3+','+path4+','+path5+','+path6+','+path7+','+path8+','+path9+','+path10+','+path11+','+path12+','+path13+','+path14+'}', otherlog+'/'], stdout=PIPE, stderr=PIPE)
	logfile.wait()
	result = repr(logfile.stderr.readline())

	if result == "''":
		print green.format("[+] Log files copied")
	else:
		print red.format('Error: %s' % result)
	
	print green.format("[+] Note: tcpdump has not been run by the script but the binary and libraries have been copied. You can run it manually, the binary is in the /usr/sbin/IR_BINARIES folder on the device\n")
	raise SystemExit(aqua.format("[+] Finished"))

if __name__ == "__main__":

# Setting up SSH key authentication 
	print green.format("[+] Setting up SSH key authentication. If you already have it set, enter 's' to skip otherwise give path")
	print red.format("[+] Warning: If you already have .ssh folder in /var/root/ and still are not skipping this step, it will overwrite the older folder and you will lose known_hosts, authorized keys or anything else saved in this folder. It is better to make a backup of your ssh folder")
	keypath = raw_input(blue.format("[+] To setup ssh key, enter the path of your ssh public key e.g. /Users/name/.ssh/id_rsa.pub:\n Path: "))

	if keypath == 's' or keypath == 'S':
		os.mkdir(fullpath, 0755)
		IR()
		logcollect()

	if keypath != 's' or keypath != 'S':

		tf = os.path.isfile(keypath)
		if tf == False:
			print red.format("[+] Error: Wrong path")
			exit()
		if tf == True:
			os.mkdir(fullpath, 0755)
			print green.format("[+] Checking if .ssh directory exists already")
			dirtest = subprocess.Popen(["ssh", host, 'cd /var/root/.ssh'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			
			result = repr(dirtest.stderr.readline())

			if result == "''":
					print green.format("[+] .ssh is already present")
			else:
	    			print red.format('Error: %s' % result)
	    		
	    			print green.format("[+] Looks like .ssh is not found, creating one now")	
				ssh2 = subprocess.Popen(["ssh", host, 'mkdir -m 700 /var/root/.ssh'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				ssh2.wait()
			
			sshupload()
			
		IR()
		logcollect()





