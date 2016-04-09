"""HTTP Server

This module contains a HTTP server
"""
import time
import threading
import webhttp.parser
import webhttp.composer
from socket import *


class ConnectionHandler(threading.Thread):
    """Connection Handler for HTTP Server"""

    def __init__(self, conn_socket, addr, timeout):
        """Initialize the HTTP Connection Handler
        
        Args:
            conn_socket (socket): socket used for connection with client
            addr (str): ip address of client
            timeout (int): seconds until timeout
        """
        super(ConnectionHandler, self).__init__()
        self.daemon = True
        self.conn_socket = conn_socket
        self.addr = addr
        self.timeout = timeout
    
    def handle_connection(self):
        """Handle a new connection"""
<<<<<<< HEAD
        message = self.conn_socket.recv(1024)
        reqParser = webhttp.parser.RequestParser()
        resComposer = webhttp.composer.ResponseComposer(self.timeout)
        requests = reqParser.parse_requests(message)
        for request in requests:
            self.conn_socket.send(str(resComposer.compose_response(request)))
=======
        close_conn = False
        last_active = time.time()
        while not close_conn:
            message = self.conn_socket.recv(1024)
            if message:
                last_active = time.time()
                print "Client message: ", message
            reqParser = webhttp.parser.RequestParser()
            resComposer = webhttp.composer.ResponseComposer(self.timeout)
            requests = reqParser.parse_requests(message)
            for request in requests:
                self.conn_socket.send(str(resComposer.compose_response(request)))
                if request.headerdict.has_key("Connection") \
                and request.get_header("Connection") == "close":
                    close_conn = True
                    break
            if time.time() > last_active + self.timeout:
                close_conn = True
                self.conn_socket.send(str(resComposer.timeout_message()))
>>>>>>> 70230fde6346a60eadaebfcf2d271e07af640d3f
        self.conn_socket.close()
        
    def run(self):
        """Run the thread of the connection handler"""
        self.handle_connection()
        

class Server:
    """HTTP Server"""

    def __init__(self, hostname, server_port, timeout):
        """Initialize the HTTP server
        
        Args:
            hostname (str): hostname of the server
            server_port (int): port that the server is listening on
            timeout (int): seconds until timeout
        """
        self.hostname = hostname
        self.server_port = server_port
        self.timeout = timeout
        self.done = False
    
    def run(self):
        """Run the HTTP Server and start listening"""
        webSocket = socket(AF_INET,SOCK_STREAM)
        webSocket.bind(('',self.server_port))
        webSocket.listen(1)
        while not self.done:
            (connSocket, address) = webSocket.accept()
            connHandler = ConnectionHandler(connSocket,address,self.timeout)
            connHandler.run()
    
    def shutdown(self):
        """Safely shut down the HTTP server"""
        self.done = True
