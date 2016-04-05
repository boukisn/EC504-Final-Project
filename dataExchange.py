import socket
import json

#def sendBloom(from, to, bloom):

#def waitForBloom(from):

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