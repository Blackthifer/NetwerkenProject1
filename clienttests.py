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


        # Send the request
        request1 = webhttp.message.Request("","")
        request1.method = "GET"
        request1.uri = "/test/index.html"
        request1.set_header("Host", "localhost:{}".format(portnr))
        request1.set_header("Connection", "close")
        self.client_socket.send(str(request1))

        # Test response
        message1 = self.client_socket.recv(1024)
        response1 = self.parser.parse_response(message1)
        etag1 = response1.get_header("ETag")
        self.assertEqual(response1.code, 200)
        self.assertTrue(response1.body)
        
        # Send the second request
        request2 = webhttp.message.Request("","")
        request2.set_header("Host", "localhost:{}".format(portnr))
        request2.set_header("If-None-Match", etag1)
        request2.set_header("Connection", "close")
        self.client_socket.send(str(request2))

        # Test second response
        message2 = self.client_socket.recv(1024)
        print repr(message2)
        response2 = self.parser.parse_response(message2)
        self.assertEqual(response2.code, 304)
        self.assertTrue(response2.body)

"""
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect(('localhost', 8001))
clientSocket.send(getReqt1)
response = clientSocket.recv(1024)
print response
clientSocket.close()
"""
