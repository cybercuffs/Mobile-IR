# Author: Nasa & Khizra (NK): This script is to collect IR data from Android devices
# Version: 1.0.0

import time
import os
import os.path
import sys
from pyadb import ADB


# Defining colors
red = "\033[01;31m{0}\033[00m"
blue = "\033[1;34m{0}\033[00m"
aqua = "\033[1;36m{0}\033[00m"
 
print blue.format("[+] Warning: Please make sure that the USB debugging is checked on the device")

# Taking ADB path input
adb_path = raw_input("Enter the full path of adb e.g. ~/adt-bundle-mac-x86_64-20140702/sdk/platform-tools/adb:\n")
adb = ADB(adb_path)

# Verifying ADB path
print aqua.format("[+] Verifying ADB path...")
if adb.check_path() is False:
	print red.format("ERROR: Wrong path")
	exit(-2)

print blue.format("OK")

# Creating output folder at the location from where the script is running from
dirfmt = "%4d-%02d-%02d %02d:%02d:%02d_A-hunt_Collect/"
dirname = dirfmt % time.localtime()[0:6]
file = sys.argv[0]
drname = os.path.dirname(file)
abspath = os.path.abspath(drname)
foldername = dirname
fullpath = abspath + '/' + foldername
os.mkdir(fullpath, 0755)

# Changing the cwd to the folder created to collect the data
os.chdir(fullpath)

# Function to collect data from unrooted device
def unrooted():

	print "[+] List of attached devices %s:" %devices
	f = open('devices.txt', 'w' )
	f.write( devices + '\n' )
	f.close()

	print "[+] Saving list of processes..."
	process = str(adb.shell_command("ps"))
	f = open('ps.txt', 'w' )
	f.write( process + '\n' )
	f.close()

	print "[+] Saving lsmod output..."
	lsmod = str(adb.shell_command("lsmod"))
	f = open('lsmod.txt', 'w' )
	f.write( lsmod + '\n' )
	f.close()

	print "[+] Saving network data..."
	netstat = str(adb.shell_command("netstat -an"))
	f = open('netstat.txt', 'w' )
	f.write( netstat + '\n' )
	f.close()


	print "[+] Saving disk information..."
	df = str(adb.shell_command("df"))
	f = open('df.txt', 'w' )
	f.write( df + '\n' )
	f.close()


	print "[+] Saving list of installed packages..."
	packages = str(adb.shell_command("pm list packages"))
	f = open('packages.txt', 'w' )
	f.write( packages + '\n' )
	f.close()

	print "[+] Saving list of permission groups..."
	permission_grps = str(adb.shell_command("pm list permission-groups"))
	f = open('permission_groups.txt', 'w' )
	f.write( permission_grps + '\n' )
	f.close()

	print "[+] Saving dumpsys... This might take few minutes"
	dumpsys = str(adb.shell_command("dumpsys"))
	f = open('dumpsys.txt', 'w' )
	f.write( dumpsys + '\n' )
	f.close()

	print "[+] Saving meminfo..."
	meminfo = str(adb.shell_command("cat /proc/meminfo"))
	f = open('meminfo.txt', 'w' )
	f.write( meminfo + '\n' )
	f.close()


	print "[+] Saving system apps..."
	sys_apks = str(adb.shell_command("ls -la /system/app"))
	f = open('system_apps.txt', 'w' )
	f.write( sys_apks + '\n' )
	f.close()


	print "[+] Saving sdcard's list..."
	sdcard = str(adb.shell_command("ls -la /sdcard"))
	f = open('sdcard.txt', 'w' )
	f.write( sdcard + '\n' )
	f.close()


	# Collecting /dev/logs
	print "[+] Saving logcat events logs..."
	event = str(adb.shell_command("logcat -d -b events -v long"))
	f = open('logcat_events.txt', 'w' )
	f.write( event + '\n' )
	f.close()


	print "[+] Saving logcat radio logs..."
	radio = str(adb.shell_command("logcat -d -b radio -v long"))
	f = open('logcat_radio.txt', 'w' )
	f.write( radio + '\n' )
	f.close()


	print "[+] Saving logcat system logs..."
	systm = str(adb.shell_command("logcat -d -b system -v long"))
	f = open('logcat_system.txt', 'w' )
	f.write( systm + '\n' )
	f.close()


	print "[+] Saving logcat main logs..."
	main = str(adb.shell_command("logcat -d -b main -v long"))
	f = open('logcat_main.txt', 'w' )
	f.write( main + '\n' )
	f.close()


	print "[+] Copying /system/SW_Configuration.xml..."
	systmremote = "/system/SW_Configuration.xml"
	foldername = "system"
	systmlocal = fullpath + '/' + foldername
	os.mkdir(systmlocal, 0755)
	pull = str(adb.get_remote_file(systmremote,systmlocal))

# Function to collect data from rooted device
def rooted():

	unrooted()

	print "[+] Saving lsof output..."
	lsof = str(adb.shell_command("su -c 'lsof -rPn'"))
	f = open('sudo-lsof.txt', 'w' )
	f.write( lsof + '\n' )
	f.close()


	print "[+] Saving user installed apps..."
	usr_apks = str(adb.shell_command("su -c 'ls -la /data/app'"))
	f = open('sudo-user_installed_apps.txt', 'w' )
	f.write( usr_apks + '\n' )
	f.close()


	print "[+] Saving pstree output..."
	pstree = str(adb.shell_command("pstree"))
	f = open('sudo-pstree.txt', 'w' )
	f.write( pstree + '\n' )
	f.close()

# Checking if the device is rooted
def rootchecker():

	sudocheck = str(adb.shell_command("su -c 'pwd'"))

	if "not found" in sudocheck:
		print red.format("No sudo access to the device, data collection would be limited")
		unrooted()
	else:
		print aqua.format("The device is rooted")
		rooted()


# Getting list of attached devices and saving the output
devices = str(adb.get_devices())
if len(devices) == 7:
		print red.format("[+] No devices detected! \n")
		exit(-4)
else:
	rootchecker()


