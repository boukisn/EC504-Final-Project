from pybloom import BloomFilter
import cPickle as pickle
import socket
import json
import sys
from bloomSync import *
import time
from pytrie import SortedStringTrie as trie
import unicodedata
import os

def sendBloom(to_ip, bloom):
	f = open('bloomFileOut', 'w+')
	f.close()
	f = open('bloomFileOut', 'wb')
	bloom.tofile(f)
	f.close()
	f = open('bloomFileOut', 'rb')

	host = to_ip
	port = 10000
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	while True:
		try:
			s.connect((host, port))
		except socket.error:
			pass
		else:
			break
	print "Connected to " + host
	size = 0
	while True:
	    chunk = f.read(1024)
	    if not chunk:
	        break
	    size += sys.getsizeof(chunk)
	    s.sendall(chunk)
	print "Sent " + str(size) + " bytes"
	f.close()
	s.close()
	os.remove('bloomFileOut')


def waitForBloom(from_ip):
	f = open('bloomFileIn', 'wb')

	host = from_ip
	port = 10000
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
	data = conn.recv(1024)
	size = sys.getsizeof(data)
	while(data):
		f.write(data)
		data = conn.recv(1024)
		size += sys.getsizeof(data)
	print "Received " + str(size) + " bytes"
	f.close()
	f = open('bloomFileIn', 'rb')
	bloom = BloomFilter.fromfile(f)
	f.close()
	conn.close()
	s.close()
	os.remove('bloomFileIn')
	return bloom

def sendData(to_ip, data):
	host = to_ip
	port = 10000
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	while True:
		try:
			s.connect((host, port))
		except socket.error:
			pass
		else:
			break
	print "Connected to " + host
	data_string = json.dumps(data)
	s.sendall(data_string)
	s.close()


def waitForData(from_ip):
	host = from_ip
	port = 10000
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
	data = conn.recv(1024)
	complete_data = data
	size = sys.getsizeof(data)
	while(data):
		data = conn.recv(1024)
		complete_data += data
		size += sys.getsizeof(data)
	print "Received " + str(size) + " bytes"
	data_loaded = json.loads(complete_data)
	conn.close()
	s.close()
	return data_loaded

def serverSync(filename, ip_to, ip_from):
	print "0. Analyze file"
	
	with open(filename) as f:
		entries = f.read().splitlines()

	server_trie = trie()
	server_bloom = BloomFilter(capacity=200000, error_rate=0.0001)
	index_dict = {}

	value = 0
	for entry in entries:
		indices_used = server_bloom.add(entry)
		encoded_entry = unicodedata.normalize('NFKD', entry.decode('unicode-escape')).encode('ascii', 'ignore')
		server_trie[encoded_entry] = value
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
	client_bloom = waitForBloom(ip_from)
	print

	# 2. Compare with my bloom & generate list to send
	print "2. Compare with my bloom & generate list to send"
	entries_to_send = compare_blooms2(server_bloom, client_bloom, index_dict)
	print

	# 3. Send list
	print "3. Send list"
	print "------------------------------------------------"
	sendData(ip_to, entries_to_send)
	time.sleep(1)
	print

	# 4. Send bloom
	print "4. Send bloom"
	print "------------------------------------------------"
	sendBloom(ip_to, server_bloom)
	print

	# 6. Receive list
	print "6. Receive list"
	print "------------------------------------------------"
	entries_needed = waitForData(ip_from)
	print

	# Add new entries
	print "7. Adding new entries"
	for entry in entries_needed:
		encoded_entry = entry.encode('ascii', 'ignore')
		server_trie[encoded_entry] = value
	print

	print "8. Generate output file"
	try:
		os.remove('server_out.txt')
	except OSError:
		pass
	f = open('server_out.txt','w+')
	sorted_list = list(server_trie.iterkeys())
	for item in sorted_list:
	  f.write("%s\n" % item)

def clientSync(filename, ip_to, ip_from):
	print "0. Analyze file"

	with open(filename) as f:
		entries = f.read().splitlines()

	client_trie = trie()
	client_bloom = BloomFilter(capacity=200000, error_rate=0.0001)
	index_dict = {}

	value = 0
	for entry in entries:
		indices_used = client_bloom.add(entry)
		encoded_entry = unicodedata.normalize('NFKD', entry.decode('unicode-escape')).encode('ascii', 'ignore')
		client_trie[encoded_entry] = value
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
	sendBloom(ip_to, client_bloom)
	print

	# 3. Receive list
	print "3. Receive list"
	print "------------------------------------------------"
	entries_needed = waitForData(ip_from)
	print

	# 4. Receive bloom
	print "4. Receive bloom"
	print "------------------------------------------------"
	server_bloom = waitForBloom(ip_from)
	print

	# 5. Compare with my bloom & generate list to send
	print "5. Compare with my bloom & generate list to send"
	print "------------------------------------------------"
	entries_to_send = compare_blooms2(client_bloom, server_bloom, index_dict)
	print

	# 6. Send list
	print "6. Send list"
	print "------------------------------------------------"
	sendData(ip_to, entries_to_send)
	print

	# Add new entries
	print "7. Add new entries"
	for entry in entries_needed:
		encoded_entry = entry.encode('ascii', 'ignore')
		client_trie[encoded_entry] = value
	print

	print "8. Generate output file"
	try:
		os.remove('client_out.txt')
	except OSError:
		pass
	f = open('client_out.txt','w+')
	sorted_list = list(client_trie.iterkeys())
	for item in sorted_list:
	  f.write("%s\n" % item)