# -*- coding: utf-8 -*-
"""
Created on Tue Apr 05 14:44:00 2016

@author: hessel
"""

from socket import *
import webhttp.resource
import logging
import webhttp.message
import webhttp.parser
import sys

# generic-message = start-line *(message-header CRLF) CRLF [ message-body ]
# start-line = Request-Line | Status-Line
# Request-Line = Method SPACE Request-URI SPACE HTTP-Version CRLF
# Request-URI = "*" | absoluteURI | abs_path | authority
# http://www.tutorialspoint.com/http/http_requests.htm

portnr = 8001

client_socket = socket(AF_INET,SOCK_STREAM)
client_socket.connect(('localhost', portnr))

#TODO Test hashes met gzip en zonder

parser = webhttp.parser.ResponseParser()

#    def test_caching(self):
"""GET for an existing single resource followed by a GET for that same
resource with caching utilized on the client/tester side
"""
# Send the request
request1 = webhttp.message.Request("","")
request1.method = "GET"
request1.uri = "/test/index.html"
request1.set_header("Host", "localhost:{}".format(portnr))
request1.set_header("Connection", "keep alive")
client_socket.send(str(request1))

# Test response
message1 = client_socket.recv(1024)
print("message1 : " + message1)
response1 = parser.parse_response(message1)
etag1 = response1.get_header("ETag")

# Send the second request
request2 = webhttp.message.Request("","")
request2.method = "GET"
request2.uri = "/test/index.html"
request2.set_header("Host", "localhost:{}".format(portnr))
request2.set_header("If-None-Match", etag1)
request2.set_header("Connection", "close")
client_socket.send(str(request2))

# Test second response
message2 = client_socket.recv(1024)
print("message 2 : " + message2)
response2 = parser.parse_response(message2)


client_socket.close()
