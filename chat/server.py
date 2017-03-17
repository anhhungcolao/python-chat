import socket
import sys
import select
import time

class ChatServer:
    def __init__(self, server_address = '127.0.0.1', server_port = 1234):
        self.clients = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.server.bind((server_address,int(server_port)))
        self.server.listen(5)

    def process(self, x):
        if (x == self.server):
            #co 1 thang client ket noi toi server
            client, address = self.server.accept()
            client.setblocking(0)
            self.clients.append(client)
            self.inputs.append(client)
            print >> sys.stderr, 'new connection from' , client, address

        elif x == sys.stdin:
            #ai do dang dung cham vao server
            self.running = False
            print >> sys.stderr, 'Dont touch anything to server pls'
            self.server.close()
        
        else:
            #x gui den server 1 request
            try:
                data = x.recv(1024)
                # print >> sys.stderr , 'server revieved: ' , data
                if data:
                    for o in self.clients:
                        if o!=x:
                            o.send(data)
                else:
                    self.inputs.remove(x)
                    if s in self.clients:
                        self.clients.remove(x)
                    x.close()
                    print >> sys.stderr , 'Closing ', address , '!'
            except socket.error:
                x.close()
                print>>sys.stderr,'Client',x, 'is disconnect'   
                # self.running = False


    def main(self):
        self.inputs = [self.server, sys.stdin]
        self.running = 1
        print >> sys.stderr , 'Waiting for a connection....!'
        while self.running:
            try:
                inputready, outputready, exceptionready = select.select(self.inputs, self.clients, [])
            except select.error:
                self.running = False
                self.server.close()
            except socket.error:
                self.running = False
                self.server.close()
            for s in inputready:
                self.process(s)
            for s in exceptionready:
                if s in inputready: 
                    self.inputs.remove(s)
                if s in self.clients:
                    self.clients.remove(s)
            for s in exceptionready:
                self.inputs.remove(s)
                self.clients.remove(s)

        self.server.close()

if __name__ == '__main__':
    if (len(sys.argv) < 3):
        print >> sys.stderr, 'Usage python ',sys.argv[0],' listen_ip listen_add'    
    else:
        ChatServer(sys.argv[1], sys.argv[2]).main()
