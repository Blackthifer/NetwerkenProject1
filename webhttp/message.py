"""HTTP Messages

This modules contains classes for representing HTTP responses and requests.
"""

reasondict = {
    # Dictionary for code reasons
    # Format: code : "Reason"
    304 : "Not Modified"
    404 : "Not Found"
    406 : "Not Acceptable"
    410 : "Gone"
    500 : "Internal Server Error"
}


class Message(object):
    """Class that stores a HTTP Message"""

    def __init__(self, body):
        """Initialize the Message"""
        self.version = "HTTP/1.1"
        self.startline = ""
        self.body = body
        self.headerdict = dict()
        
    def set_header(self, name, value):
        """Add a header and its value
        
        Args:
            name (str): name of header
            value (str): value of header
        """
        self.headerdict[name] = value
        
    def get_header(self, name):
        """Get the value of a header
        
        Args:
            name (str): name of header

        Returns:
            str: value of header, empty if header does not exist
        """
        if name in self.headerdict:
            return self.headerdict[name]
        else:
            return ""
        
    def __str__(self):
        """Convert the Message to a string
        
        Returns:
            str: representation the can be sent over socket
        """
        message = self.startline + "\r\n"
        for name in self.headerdict.keys():
            message = message + name + " " + self.headerdict[name] + "\r\n"
        message = message + "\r\n" + self.body
        return message


class Request(Message):
    """Class that stores a HTTP request"""

    def __init__(self, method, uri, body):
        """Initialize the Request"""
        super(Request, self).__init__(body)
        self.method = method
        self.uri = uri
        
    def set_header(self, name, value):
        """Add a header and its value
        
        Args:
            name (str): name of header
            value (str): value of header
        """
        super(Request, self).set_header(name, value)
        
    def get_header(self, name):
        """Get the value of a header
        
        Args:
            name (str): name of header

        Returns:
            str: value of header, empty if header does not exist
        """
        return super(Request, self).get_header(name)
        
    def __str__(self):
        """Convert the Request to a string

        Returns:
            str: representation the can be sent over socket
        """
        self.startline = self.method + " " + self.uri + " " + self.version
        return super(Request, self).__str__()
        

class Response(Message):
    """Class that stores a HTTP Response"""

    def __init__(self):
        """Initialize the Response"""
        super(Response, self).__init__("")
        self.code = 500
    
    def __str__(self):
        """Convert the Response to a string

        Returns:
            str: representation the can be sent over socket
        """
        self.startline = str(self.code) + " " #+ reasondict[self.code]
        return super(Response, self).__str__()
