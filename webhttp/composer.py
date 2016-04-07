""" Composer for HTTP responses

This module contains a composer, which can compose responses to
HTTP requests from a client.
"""

import time
import webhttp.message
import webhttp.resource


class ResponseComposer:
    """Class that composes a HTTP response to a HTTP request"""

    def __init__(self, timeout):
        """Initialize the ResponseComposer
        
        Args:
            timeout (int): connection timeout
        """
        self.timeout = timeout
    
    def compose_response(self, request):
        """Compose a response to a request
        
        Args:
            request (webhttp.Request): request from client

        Returns:
            webhttp.message.Response: response to request
        """
        response = webhttp.message.Response()
        #image/jpeg for .jpeg/.jpg files
        #text/html or text/plain for .html?
        if not request.method == "GET":
            response.code = 400
        else:
		response.code = 200
		resource = webhttp.resource.Resource(request.uri)
		response.set_header("Content-Length", str(resource.get_content_length()))
#	        response.set_header("Connection", "close")
		response.body = resource.get_content()
		print "Test " + response.body        
        return response

    def make_date_string(self):
        """Make string of date and time
        
        Returns:
            str: formatted string of date and time
        """
        return time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
