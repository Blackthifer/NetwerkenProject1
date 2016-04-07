"""HTTP response and request parsers

This module contains parses for HTTP response and HTTP requests.
"""

import webhttp.message
import sys


class RequestParser:
    """Class that parses a HTTP request"""

    def __init__(self):
        """Initialize the RequestParser"""
        pass
        
    def parse_requests(self, buff):
        """Parse requests in a buffer

        Args:
            buff (str): the buffer contents received from socket

        Returns:
            list of webhttp.message.Request
        """
        requests = self.split_requests(buff)
        
        http_requests = []
        for request in requests:
            requestSplit = request.split('\r\n\r\n')
            headerSplit = requestSplit[0].split('\r\n', 1)
            messageBody = requestSplit[1]
            startLine = headerSplit[0]
            if len(headerSplit) > 1:
                headers = headerSplit[1].split('\r\n')
            else:
                headers = []
            parts = startLine.split(' ')
            http_request = webhttp.message.Request(parts[0], parts[1])
            for header in headers:
                headerPair = header.split(': ',1)
                http_request.set_header(headerPair[0],headerPair[1])
            http_request.body = messageBody
            http_requests.append(http_request)
        return http_requests

    def split_requests(self, buff):
        """Split multiple requests
        
        Arguments:
            buff (str): the buffer contents received from socket

        Returns:
            list of str
        """
        requests = buff.split('\r\n\r\n')
        requests = filter(None, requests)
        requests = [r + '\r\n\r\n' for r in requests]
        requests = [r.lstrip() for r in requests]
        return requests


class ResponseParser:
    """Class that parses a HTTP response"""
    def __init__(self):
        """Initialize the ResponseParser"""
        pass

    def parse_response(self, buff):
        """Parse responses in buffer

        Args:
            buff (str): the buffer contents received from socket

        Returns:
            webhttp.message.Response
        """      
        response = webhttp.message.Response()
        responseSplit = buff.split('\r\n\r\n')
        headerSplit = responseSplit[0].split('\r\n', 1)
        if len(responseSplit) > 1:
            messageBody = responseSplit[1]
        else:
            messageBody = ""
        startLine = headerSplit[0]
        if len(headerSplit) > 1:
            headers = headerSplit[1].split('\r\n')
        else:
            headers = []
        parts = startLine.split(' ')
        response.code = int(parts[1])
        for header in headers:
            headerPair = header.split(': ',1)
            response.set_header(headerPair[0],headerPair[1])
        response.body = messageBody
        return response

