import sys
import socket
import time
import select

class Client:
    def __init__(self, server_address = '127.0.0.1', server_port = 1234):
        self.running  = True
        try:
            self.sock  = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
            self.sock.connect((server_address,int(server_port)))
        except socket.error:
            print 'error'
            self.sock.close();
            self.running = False

    def process(self, x):
        if (x == sys.stdin):
            data = sys.stdin.readline()
            self.send(data)
        elif x == self.sock:
            data = x.recv(100)
            print >>sys.stderr , data,

    def send(self,data):
        if data:
            data = sys.argv[1] + ': ' + data
            self.sock.sendall(data)

    def main(self):
        self.input = [self.sock,sys.stdin]
        self.output = []
        while self.running:
            inputready,self.outputready,exceptional = select.select(self.input,self.output,[])
            for s in inputready:
                self.process(s)
            


if __name__ == '__main__':
    if (len(sys.argv) < 4):
        print >> sys.stderr, 'Usage python client.py user ip port'
    else:
        Client(sys.argv[2],sys.argv[3]).main()