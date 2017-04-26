This will SSH to the devices in IPs.csv.  Then make a copy of the running config in the folder.  
It will then find any interface with "ip helper-address" (The Parent in the the config according to  ciscoconfigparse).
It will then make a file named results.txt with the IP address of each device and the interfaces listed.
