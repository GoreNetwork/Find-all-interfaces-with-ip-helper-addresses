import random
import os
import re
import socket
import sys
import netmiko
import time
from getpass import getpass
from ciscoconfparse import CiscoConfParse


def get_ip (input):
	return(re.findall(r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', input))

def to_doc_a(file_name, varable):
	f=open(file_name, 'a')
	f.write(varable)
	f.write("\n")
	f.close()

def to_doc(file_name, varable):
	f=open(file_name, 'w')
	f.write(varable)
	f.close()
	running_configs.append(file_name)
	

def read_doc_ips (file_name):
	for line in open(file_name, 'r').readlines():
		line = get_ip(line)
		for each in line:
			ips.append(each)
		
def go_get_info_from_devices(ip):
	try:
		net_connect = netmiko.ConnectHandler(device_type='cisco_ios', ip=ip, username=username, password=password) 
		tmp_device_info =  net_connect.send_command_expect('show run')
		return tmp_device_info
	except:
		cant_ssh = "Can't SSH to "+ip
		to_doc("results.txt",cant_ssh)
		return "Can't SSH to this"
running_configs = []
ips = []
read_doc_ips('IPs.csv')	
print (ips)	
		
username = input("Username: ")
password = getpass() 

for ip in ips:
	file_name = ip+"show run.txt"
	run = go_get_info_from_devices(ip)
	to_doc(file_name,run)

results = []
for doc in running_configs:
	ip = get_ip (doc)
	for each in ip:
		ip = each
	needs_helper = []
	running_config=CiscoConfParse(doc)
	helpers = running_config.find_objects("ip helper-address")
	for each in helpers:
		#print(each.parent.text)
		if each.parent.text not in needs_helper:
			needs_helper.append(each.parent.text)
	temp = [ip,needs_helper]
	results.append(temp)

print (results)	
for each in results:
	print(each[0])
	try:
		to_doc_a("results.txt",each[0])
		for int in each[1]:
			print (int)
			tmp = "\t"+int
			to_doc_a("results.txt",tmp)
	except:
		issue = "there was an issue with "+str(each)
		to_doc_a("results.txt",issue)
		
	
		
	
	
	
	
	
	
	
	
	
	
	
	
	