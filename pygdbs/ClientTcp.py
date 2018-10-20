import socket
import sys

class ClientTcp(object):

    def __init__(self):
        self.sock = None
        self.server_address = None

    def open(self, host='127.0.0.1', port=9999):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(5.0)
        self.server_address = (host, port)
        print('starting up on %s port %s' % self.server_address)
        self.sock.connect(self.server_address)

    def write(self, message):
        print('sending "%s"' % message)
        self.sock.sendall(message)

    def read(self):
        data = None
        try:
            data = self.sock.recv(4096)
            print('received "%s"' % data)
        finally:
            return data

    def close(self):
        print('closing socket')
        self.sock.close()
