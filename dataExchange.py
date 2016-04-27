'''
Nick Boukis & Sami Shahin
EC504
dataExchange.py
'''

from pybloom import BloomFilter
import cPickle as pickle
import socket
import json
import sys
from bloomSync import *
import time
import unicodedata
import os
from Tkinter import *
import ttk

def sendBloom(to_ip, bloom, print_labels=False, frame=None, print_start=0):
	# Create output file for bloom filter export
	f = open('bloomFileOut', 'w+')
	f.close()
	f = open('bloomFileOut', 'wb')
	bloom.tofile(f)
	f.close()
	f = open('bloomFileOut', 'rb')

	# Connect to IP address
	host = to_ip
	port = 10000
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Keep trying until a connection is made
	while True:
		try:
			s.connect((host, port))
		except socket.error:
			pass
		else:
			break

	print "Connected to " + host
	size = 0

	# Send bloom file in increments
	while True:
	    chunk = f.read(1024)
	    if not chunk:
	        break
	    size += sys.getsizeof(chunk)
	    s.sendall(chunk)

	print "Sent " + str(size/1000) + " KB"

	# Print to GUI
	if print_labels:
		ttk.Label(frame, text=("Sent bloom filter (" + str(size/1000) + " KB)")).grid(row=print_start,column=0)

	# Cleanup
	f.close()
	s.close()
	os.remove('bloomFileOut')


def waitForBloom(from_ip, print_labels=False, frame=None, print_start=0):
	# Create file for bloom filter import
	f = open('bloomFileIn', 'wb')

	# Connect to IP address
	host = from_ip
	port = 10000
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Keep trying until a connection is made
	while True:
		try:
			s.bind((host, port))
		except socket.error:
			pass
		else:
			break

	s.listen(1)
	print "Waiting for data..."
	conn, addr = s.accept()
	print "Connection from " + addr[0]

	# Receive bloom filter in increments
	data = conn.recv(1024)
	size = sys.getsizeof(data)
	while(data):
		f.write(data)
		data = conn.recv(1024)
		size += sys.getsizeof(data)

	print "Received " + str(size/1000) + " KB"

	# Print to GUI
	if print_labels:
		ttk.Label(frame, text=("Received bloom filter (" + str(size/1000) + " KB)")).grid(row=print_start,column=0)

	# Cleanup & bloom filter creation
	f.close()
	f = open('bloomFileIn', 'rb')
	bloom = BloomFilter.fromfile(f)
	f.close()
	conn.close()
	s.close()
	os.remove('bloomFileIn')
	return bloom

def sendData(to_ip, data, print_labels=False, frame=None, print_start=0):
	# Connect to IP address
	host = to_ip
	port = 10000
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Keep trying until a connection is made
	while True:
		try:
			s.connect((host, port))
		except socket.error:
			pass
		else:
			break

	print "Connected to " + host

	# Create JSON string
	data_string = json.dumps(data)

	# Print to GUI
	if print_labels:
		ttk.Label(frame, text=("Sent json (" + str(sys.getsizeof(data_string)/1000) + " KB)")).grid(row=print_start,column=0)

	# Send JSON and close connection
	s.sendall(data_string)
	s.close()


def waitForData(from_ip, print_labels=False, frame=None, print_start=0):
	# Connect to IP address
	host = from_ip
	port = 10000
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Keep trying until a connection is made
	while True:
		try:
			s.bind((host, port))
		except socket.error:
			pass
		else:
			break

	s.listen(1)
	print "Waiting for data..."
	conn, addr = s.accept()
	print "Connection from " + addr[0]

	# Read from JSON string
	data = conn.recv(1024)
	complete_data = data
	size = sys.getsizeof(data)
	while(data):
		data = conn.recv(1024)
		complete_data += data
		size += sys.getsizeof(data)

	print "Received " + str(size/1000) + " KB"

	# Print to gUI
	if print_labels:
		ttk.Label(frame, text=("Received json (" + str(size/1000) + " KB)")).grid(row=print_start,column=0)

	# Load data from JSON and close connection
	data_loaded = json.loads(complete_data)
	conn.close()
	s.close()
	return data_loaded

# Execute process from server's perspective (initially waiting for data)
def serverSync(filename, ip_to, ip_from, print_labels=False, frame=None, print_start=0):
	server_list = []
	server_bloom = BloomFilter(capacity=200000, error_rate=0.0001)
	index_dict = {}

	print "------------------------------------------------"
	print "0. Analyze file"
	
	# Read entries from file
	with open(filename) as f:
		entries = f.read().splitlines()

	# Load entries into bloom filter and keep track of their position
	value = 0
	for entry in entries:
		indices_used = server_bloom.add(entry)
		encoded_entry = unicodedata.normalize('NFKD', entry.decode('unicode-escape')).encode('ascii', 'ignore')
		server_list.append(encoded_entry)
		value = value + 1
		for index in indices_used:
			if index in index_dict:
			    curr_list = index_dict[index]
			    curr_list.append(entry)
			    index_dict[index] = list(set(curr_list))
			else:
			    index_dict[index] = [entry]
	print

	# 1. Receive other bloom
	print "1. Receive other bloom"
	print "------------------------------------------------"
	client_bloom = waitForBloom(ip_from, print_labels, frame, print_start)
	print

	# 2. Compare with my bloom & generate list to send
	print "2. Compare with my bloom & generate list to send"
	entries_to_send = compare_blooms(server_bloom, client_bloom, index_dict)
	print

	# 3. Send list
	print "3. Send list"
	print "------------------------------------------------"
	sendData(ip_to, entries_to_send, print_labels, frame, (print_start + 1))
	time.sleep(1)
	print

	# 4. Send bloom
	print "4. Send bloom"
	print "------------------------------------------------"
	sendBloom(ip_to, server_bloom, print_labels, frame, (print_start + 2))
	print

	# 6. Receive list
	print "6. Receive list"
	print "------------------------------------------------"
	entries_needed = waitForData(ip_from, print_labels, frame, (print_start + 3))
	print

	# 7. Add new entries
	print "7. Adding new entries"
	for entry in entries_needed:
		encoded_entry = entry.encode('ascii', 'ignore')
		server_list.append(encoded_entry)
	print

	# 8. Generate output file
	print "8. Generate output file"
	try:
		os.remove('server_out.txt')
	except OSError:
		pass
	f = open('server_out.txt','w+')
	for item in server_list:
		f.write("%s\n" % item)
	print "------------------------------------------------"
	print

# Execute process from client's perspective (initiates interactions with other databases)
def clientSync(filename, ip_to, ip_from, print_labels=False, frame=None, print_start=0):
	client_list = []
	client_bloom = BloomFilter(capacity=200000, error_rate=0.0001)
	index_dict = {}

	print "------------------------------------------------"
	print "0. Analyze file"

	# Read entries from file
	with open(filename) as f:
		entries = f.read().splitlines()
	
	# Load entries into bloom filter and keep track of their position
	value = 0
	for entry in entries:
		indices_used = client_bloom.add(entry)
		encoded_entry = unicodedata.normalize('NFKD', entry.decode('unicode-escape')).encode('ascii', 'ignore')
		client_list.append(encoded_entry)
		value = value + 1
		for index in indices_used:
			if index in index_dict:
			    curr_list = index_dict[index]
			    curr_list.append(entry)
			    index_dict[index] = list(set(curr_list))
			else:
			    index_dict[index] = [entry]
	print

	# 1. Send bloom
	print "1. Send bloom"
	print "------------------------------------------------"
	sendBloom(ip_to, client_bloom, print_labels, frame, print_start)
	print

	# 3. Receive list
	print "3. Receive list"
	print "------------------------------------------------"
	entries_needed = waitForData(ip_from, print_labels, frame, (print_start + 1))
	print

	# 4. Receive bloom
	print "4. Receive bloom"
	print "------------------------------------------------"
	server_bloom = waitForBloom(ip_from, print_labels, frame, (print_start + 2))
	print

	# 5. Compare with my bloom & generate list to send
	print "5. Compare with my bloom & generate list to send"
	print "------------------------------------------------"
	entries_to_send = compare_blooms(client_bloom, server_bloom, index_dict)
	print

	# 6. Send list
	print "6. Send list"
	print "------------------------------------------------"
	sendData(ip_to, entries_to_send, print_labels, frame, (print_start + 3))
	print

	# 7. Add new entries
	print "7. Add new entries"
	for entry in entries_needed:
		encoded_entry = entry.encode('ascii', 'ignore')
		client_list.append(encoded_entry)
	print

	# 8. Generate output file
	print "8. Generate output file"
	try:
		os.remove('client_out.txt')
	except OSError:
		pass
	f = open('client_out.txt','w+')
	for item in client_list:
		f.write("%s\n" % item)
	print "------------------------------------------------"
	print
