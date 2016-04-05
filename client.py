import socket
import json
from bloomSync import *
from dataExchange import *
import time

sendData('127.0.0.1', [1, 2, 3])
#time.sleep(5)
data_received = waitForData('127.0.0.1')
print data_received