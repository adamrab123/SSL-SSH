from TcpServer import TcpServer
import negotiation as neg



def do_stuff(data):
    print(data)

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    server = TcpServer(host, port)

    key_exchange, cipher, hmac = neg.handshake(server, "server")
    





    # data = server.receive()
    # msg = do_stuff(data)
    # server.send("hi")