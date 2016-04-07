# -*- coding: utf-8 -*-
"""
Created on Tue Apr 05 14:44:00 2016

@author: hessel
"""

from socket import *
import webhttp.resource

# generic-message = start-line *(message-header CRLF) CRLF [ message-body ]
# start-line = Request-Line | Status-Line
# Request-Line = Method SPACE Request-URI SPACE HTTP-Version CRLF
# Request-URI = "*" | absoluteURI | abs_path | authority
# http://www.tutorialspoint.com/http/http_requests.htm

getReqt1 = "GET / HTTP/1.1\r\n\r\n"
getReqt2 = "\r\n GET http://www.funnygames.nl/spel/papa_louie.html HTTP/1.1" #Deze eerste CRLF zou genegeerd moeten worden
getReqt3 = "GET /spel/papa_louie.html HTTP/1.1"



clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect(('localhost', 8001))
clientSocket.send(getReqt1)
response = clientSocket.recv(1024)
print response
clientSocket.close()

