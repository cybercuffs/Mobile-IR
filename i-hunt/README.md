Prerequisites:

	Following are the prerequisites for i-hunt.py
		
		1- Jail-broken iDevice
		2- Open SSH package installed from Cydia store
		3- RSA/DSA key pair 

How to use i-hunt:

	Make sure that device is unlocked (it is recommended that Auto-Lock option in Settings is set to Never or maximum)
	
	IR_BINARIES folder should be saved at the same location as script. 
	
	e.g: python i-hunt.py

	A folder name like "2015-03-0523/18/11_i-hunt_Collect" would be created in the same location where i-hunt.py exists

Note: Public keys e.g. yourkey.pub should be at location /var/root/.ssh and named as “authorized_keys”. For additional keys, name them as “authorized_keys2” and so on. The permission should be "0600" for the keys. 
