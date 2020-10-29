"""
File description TBD
"""

import socketserver
import socket
import sys

# Constants
host = "0.0.0.0"
port = 10000
address = (host, port)

class MyTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

class TCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        message = self.request.recv(10).strip()
        print(f"got a message {message}")

        if message == b'ping':
            self.request.sendall(b'pong\n')

def serve():
    server = MyTCPServer(address, TCPHandler)
    server.serve_forever()

def ping():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    sock.sendall(b'ping')
    resp = sock.recv(10)
    print(f'Received: {resp.decode()}')
    
if __name__ == "__main__":
    if sys.argv[1] == "serve":
        serve()
    elif sys.argv[1] == "ping":
        ping()
    else:
        pass
