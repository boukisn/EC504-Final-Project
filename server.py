import socket
import json
from bloomSync import *
from dataExchange import *
import time

 
data_received = waitForData('127.0.0.1')
print data_received
#time.sleep(5)
sendData('127.0.0.1', [4, 5, 6])