from TcpServer import TcpServer
import negotiation as neg
from key_exchange import key_exchange


def do_stuff(data):
    print(data)

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    server = TcpServer(host, port)

    key_exchange_algo, cipher, hmac = neg.handshake(server, "server")
    key_exchange(server, key_exchange_algo, "server")
    





    # data = server.receive()
    # msg = do_stuff(data)
    # server.send("hi")