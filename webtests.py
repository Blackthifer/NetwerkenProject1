import unittest
import logging
import socket
import sys
import time

import webhttp.message
import webhttp.parser


portnr = 8001
timeout = 15


class TestGetRequests(unittest.TestCase):
    """Test cases for GET requests"""

    def setUp(self):
        """Prepare for testing"""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("localhost", portnr))
        self.parser = webhttp.parser.ResponseParser()

    def tearDown(self):
        """Clean up after testing"""
        self.client_socket.shutdown(socket.SHUT_RDWR)
        self.client_socket.close()

    def test_existing_file(self):
        """GET for a single resource that exists"""
        # Send the request
        request = webhttp.message.Request("","")
        request.method = "GET"
        request.uri = "/test/index.html"
        request.set_header("Host", "localhost:{}".format(portnr))
        request.set_header("Connection", "close")
        self.client_socket.send(str(request))

        # Test response
        message = self.client_socket.recv(1024)
        response = self.parser.parse_response(message)
        self.assertEqual(response.code, 200)
        self.assertTrue(response.body)

    def test_nonexistant_file(self):
        """GET for a single resource that does not exist"""
        # Send the request
        request = webhttp.message.Request("","")
        request.method = "GET"
        request.uri = "/forbiddenKnowledge/swordOfTruth.nope"
        request.set_header("Host", "localhost:{}".format(portnr))
        request.set_header("Connection", "close")
        self.client_socket.send(str(request))

        # Test response
        message = self.client_socket.recv(1024)
        response = self.parser.parse_response(message)
        self.assertEqual(response.code, 404)
        self.assertTrue(not response.body)

    def test_caching(self):
        """GET for an existing single resource followed by a GET for that same
        resource with caching utilized on the client/tester side
        """
        # Send the request
        request1 = webhttp.message.Request("","")
        request1.method = "GET"
        request1.uri = "/test/index.html"
        request1.set_header("Host", "localhost:{}".format(portnr))
        request1.set_header("Connection", "keep alive")
        self.client_socket.send(str(request1))

        # Test response
        message1 = self.client_socket.recv(1024)
        response1 = self.parser.parse_response(message1)
        etag1 = response1.get_header("ETag")
        self.assertEqual(response1.code, 200)
        self.assertTrue(response1.body)
        
        # Send the second request
        request2 = webhttp.message.Request("","")
        request2.method = "GET"
        request2.uri = "/test/index.html"
        request2.set_header("Host", "localhost:{}".format(portnr))
        request2.set_header("If-None-Match", etag1)
        request2.set_header("Connection", "close")
        self.client_socket.send(str(request2))

        # Test second response
        message2 = self.client_socket.recv(1024)
        response2 = self.parser.parse_response(message2)
        self.assertEqual(response2.code, 304)
        self.assertTrue(not response2.body)
        
    def test_existing_index_file(self):
        """GET for a directory with an existing index.html file"""
        # Send the request
        request = webhttp.message.Request("","")
        request.method = "GET"
        request.uri = "/test/"
        request.set_header("Host", "localhost:{}".format(portnr))
        request.set_header("Connection", "close")
        self.client_socket.send(str(request))

        # Test response
        message = self.client_socket.recv(1024)
        response = self.parser.parse_response(message)
        self.assertEqual(response.code, 200)
        self.assertTrue(response.body)

    def test_nonexistant_index_file(self):
        """GET for a directory with a non-existant index.html file"""
        # Send the request
        request = webhttp.message.Request("","")
        request.method = "GET"
        request.uri = "/testNOPE/"
        request.set_header("Host", "localhost:{}".format(portnr))
        request.set_header("Connection", "close")
        self.client_socket.send(str(request))

        # Test response
        message = self.client_socket.recv(1024)
        response = self.parser.parse_response(message)
        self.assertEqual(response.code, 404)
        self.assertTrue(not response.body)

    def test_persistent_close(self):
        """Multiple GETs over the same (persistent) connection with the last
        GET prompting closing the connection, the connection should be closed.
        """
        request1 = webhttp.message.Request("","")
        request1.method = "GET"
        request1.uri = "test/index.html"
        request1.set_header("Host", "localhost:{}".format(portnr))
        request1.set_header("Connection", "keep alive")
        self.client_socket.send(str(request1))
        self.client_socket.recv(1024)
        self.client_socket.send(str(request1))
        self.client_socket.recv(1024)
        self.client_socket.send(str(request1))
        self.client_socket.recv(1024)
        request2 = request1
        request2.set_header("Connection", "close")
        self.client_socket.send(str(request2))
        message = self.client_socket.recv(1024)
        response = self.parser.parse_response(message)
        self.assertEqual(response.get_header("Connection"), "close")

    def test_persistent_timeout(self):
        """Multiple GETs over the same (persistent) connection, followed by a
        wait during which the connection times out, the connection should be
        closed.
        """
        request1 = webhttp.message.Request("GET", "/")
        request1.set_header("Host", "localhost:{}".format(portnr))
        request1.set_header("Connection", "keep alive")
        request2 = webhttp.message.Request("GET", "test/")
        request2.set_header("Host", "localhost:{}".format(portnr))
        request2.set_header("Connection", "keep alive")
        self.client_socket.send(str(request1))
        self.client_socket.recv(1024)
        self.client_socket.send(str(request2))
        self.client_socket.recv(1024)
        time.sleep(timeout)
        message = self.client_socket.recv(1024)
        timeout_resp = self.parser.parse_response(message)
        self.assertEqual(timeout_resp.code, 408)
        self.assertEqual(timeout_resp.get_header("Connection"), "close")

    def test_encoding(self):
        """GET which requests an existing resource using gzip encoding, which
        is accepted by the server.
        """
        log = logging.getLogger("test_encoding")
        # Send the request
        request1 = webhttp.message.Request("","")
        request1.method = "GET"
        request1.uri = "/test/index.html"
        request1.set_header("Host", "localhost:{}".format(portnr))
        request1.set_header("Connection", "keep alive")
        self.client_socket.send(str(request1))
        # Parse the normal response
        message1 = self.client_socket.recv(1024)
        response1 = self.parser.parse_response(message1)
        self.assertEqual(response1.code, 200)
        
        # Send the gzip request
        request2 = webhttp.message.Request("","")
        request2.method = "GET"
        request2.uri = "/test/index.html"
        request2.set_header("Host", "localhost:{}".format(portnr))
        request2.set_header("Accept-Encoding", "gzip")
        request2.set_header("Connection", "close")
        self.client_socket.send(str(request2))

        # Parse the gzip response
        message2 = self.client_socket.recv(1024)
        log.debug("message2: " + message2)
        response2 = self.parser.parse_response(message2)
        self.assertEqual(response2.code, 200)
        self.client_socket.shutdown(socket.SHUT_RDWR)
        self.client_socket.close()
        
        # Compare normal and gzip responses
        self.assertTrue(len(message1) < len(message2))
        self.assertEqual(response1.body, response2.body)


if __name__ == "__main__":
	# Logging utility
    logging.basicConfig(stream = sys.stderr)
    #logging.getLogger("test_encoding").setLevel(logging.DEBUG)
    #logging.getLogger("parse_response").setLevel(logging.DEBUG)
    
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="HTTP Tests")
    parser.add_argument("-p", "--port", type=int, default=8001)
    
    # Arguments for the unittest framework
    parser.add_argument('unittest_args', nargs='*')
    args = parser.parse_args()
    
    # Only pass the unittest arguments to unittest
    sys.argv[1:] = args.unittest_args

    # Start test suite
    unittest.main()
