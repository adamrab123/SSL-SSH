import socket
import json



class TcpServer:
    def __init__(self, host, port, kind="server"):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.kind = kind
        self.conn = None
        self.sock.setblocking(1)

        if self.kind == "server":
            self.sock.bind((self.host, self.port))
            self.sock.listen(1)
            print("Waiting for client connection")
            conn, addr = self.sock.accept()
            self.conn = conn

        elif self.kind == "client":
            self.sock.connect((self.host, self.port))
    
    def __del__(self):
        if self.conn:
            self.conn.close()

    def send(self, data):
        if self.kind == "server":
            self.conn.send(json.dumps(data).encode())
        elif self.kind == "client":
            self.sock.send(json.dumps(data).encode())

    def receive(self, size=1024):
        if self.kind == "server":
            try:
                data = self.conn.recv(size)
            except socket.error:
                return None
        elif self.kind == "client":
            try:
                data = self.sock.recv(size)
            except socket.error:
                return None
        return json.loads(data.decode())



# Ignore
if __name__ == "__main__":
    # run tests on the UDP server object
    host = "127.0.0.1"
    port = 5000

    server = TcpServer(host, port)

    # example
    while True:
        data = server.receive()
        msg = do_stuff(data)
        server.send(msg)