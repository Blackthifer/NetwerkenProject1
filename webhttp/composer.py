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
        
    def timeout_message(self):
        """Create a response message when the connection timeouts
        
        Returns:
            webhttp.message.Response: timeout message
        """
        response = webhttp.message.Response()
        response.code = 408
        response.set_header("Connection", "close")
        return response
    
    def compose_response(self, request):
        """Compose a response to a request
        
        Args:
            request (webhttp.Request): request from client
    
        Returns:
            webhttp.message.Response: response to request
        """
        response = webhttp.message.Response()
        if not request.method == "GET":
            response.code = 400
        else:
            try:
<<<<<<< HEAD
                response.code = 200
                resource = webhttp.resource.Resource(request.uri)
                response.set_header("Content-Length", str(resource.get_content_length()))
                response.set_header("Content-Type", resource.get_content_type())
                newETag = resource.generate_etag()
                response.set_header("ETag", newETag)
                response.body = resource.get_content()
                if (request.headerdict.has_key("If-None-Match")) \
                and (newETag == request.get_header("If-None-Match")):
                    response.code = 304
                    response.body = ""
=======
				response.code = 200
				resource = webhttp.resource.Resource(request.uri)
				response.set_header("Content-Length", str(resource.get_content_length()))
				response.set_header("Content-Type", resource.get_content_type())
				response.body = resource.get_content()
				# Caching
				newETag = resource.generate_etag()
				response.set_header("ETag", newETag)
				if (request.headerdict.has_key("If-None-Match")) \
				and (newETag == request.get_header("If-None-Match")):
					response.code = 304
					response.body = ""
				# Encoding
				if (request.headerdict.has_key("Accept-Encoding")) \
				and (gzip == request.get_header("Accept-Encoding")):
					response.set_header("Content-Encoding", this.resource.get_content_encoding)
					response.body = this.resource.gzip_encode(response.body)
			# Exceptions
>>>>>>> origin/master
            except webhttp.resource.FileExistError:
                response.code = 404
            except webhttp.resource.FileAccessError:
                response.code = 401
            if request.get_header("Connection") == "close":
                response.set_header("Connection", "close")
            else:
                response.set_header("Connection", "keep alive")
        return response
    
    def make_date_string(self):
        """Make string of date and time
        
        Returns:
            str: formatted string of date and time
        """
        return time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
