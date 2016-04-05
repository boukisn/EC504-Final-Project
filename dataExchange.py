from pybloom import BloomFilter
import cPickle as pickle
import socket
import json
import sys


def sendBloom(to_ip, bloom):
	f = open('bloomFileOut', 'w+')
	bloom.tofile(f)
	f.close()
	f = open('bloomFileOut', 'rb')

	host = to_ip
	port = 50008
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	while True:
		try:
			s.connect((host, port))
		except socket.error:
			pass
		else:
			break

	while True:
	    chunk = f.read(1024)
	    if not chunk:
	        break
	    s.sendall(chunk)
	f.close()
	s.close()


def waitForBloom(from_ip):
	f = open('bloomFileIn', 'wb')

	host = from_ip
	port = 50008
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
	print "Size: " + str(size)
	f.close()
	f = open('bloomFileIn', 'rb')
	bloom = BloomFilter.fromfile(f)
	f.close()
	conn.close()
	s.close()
	return bloom

def sendBloom2(to_ip, bloom):
	host = to_ip
	port = 50008
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	while True:
		try:
			s.connect((host, port))
		except socket.error:
			pass
		else:
			break
	print "Connected to " + host
	data_string = pickle.dumps(bloom)
	s.sendall(data_string)
	s.close()


def waitForBloom2(from_ip):
	host = from_ip
	port = 50008
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
	data = conn.recv(1000000)
	while data:
		before = sys.getsizeof(data)
		data += conn.recv(1000000)
		after = sys.getsizeof(data)
		if before == after:
			break
	print "Size: " + str(sys.getsizeof(data))
	data_loaded = pickle.loads(data)
	conn.close()
	s.close()
	return data_loaded

def sendData(to_ip, data):
	host = to_ip
	port = 50008
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
	port = 50008
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	while True:
		try:
			s.bind((host, port))
		except socket.error:
			pass
		else:
			break
	s.listen(2)
	print "Waiting for data..."
	conn, addr = s.accept()
	print "Connection from " + addr[0]
	data = conn.recv(1024)
	data_loaded = json.loads(data)
	conn.close()
	s.close()
	return data_loaded