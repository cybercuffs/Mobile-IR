# A-hunt 

A tool to collect IR data from Android devices 

Prerequisites:

	Following are the two prerequisites for A-hunt.py
		1-ADB
		2-pyadb
 		3-(Optional) rooted device to collect full data

Setting up ADB:
	Install ADB from http://developer.android.com/sdk/index.html

Setting up pyadb:

	Download pyadb from https://pypi.python.org/pypi/pyadb/0.1.1
	tar -xvzf pyadb-0.1.1.tar.gz
	python setup.py build
	python setup.py install

Check if pyadb is installed properly
	python
	from pyadb import ADB
	adb= ADB(‘~/android/platform-tools/adb’)
	print adb.pyadb_version()

How to use A-hunt:

	Make sure the USB debugging is turned on. It is recommended to put the device in never sleep mode

	e.g: python A-hunt.py

	A folder name like “2015-02-15 22:03:31_A-hunt_Collect” would be created in the same location where A-hunt.py exists. Additional files with name starting with “sudo_” are created, in case of rooted phones.

