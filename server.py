import socket
import json
from bloomSync import *
from dataExchange import *
import time

bloom = waitForBloom('127.0.0.1')
#index_dict = waitForData('127.0.0.1')