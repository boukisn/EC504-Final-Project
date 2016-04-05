import socket
import json
from bloomSync import *
from dataExchange import *
import time

bloom = BloomFilter(capacity=200000, error_rate=0.01)
index_dict = {}
database_one_list 	= ["a","b","d","g","i","m","o","q","u","w","x","k","z"]
for entry in database_one_list:
	indices_used = bloom.add(entry)
	for index in indices_used:
		if index in index_dict:
		    curr_list = index_dict[index]
		    curr_list.append(entry)
		    index_dict[index] = list(set(curr_list))
		else:
		    index_dict[index] = [entry]

sendBloom('127.0.0.1', bloom)
#time.sleep(1)
#sendData('127.0.0.1', index_dict)