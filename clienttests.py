# -*- coding: utf-8 -*-
"""
Created on Tue Apr 05 14:44:00 2016

@author: hessel
"""

from socket import *

clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect(('localhost', 8001))
clientSocket.send('Hello')
response = clientSocket.recv(1024)
print response
clientSocket.close()