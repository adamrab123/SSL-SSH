from TcpServer import TcpServer
import negotiation as neg
from key_exchange import key_exchange






if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    server = TcpServer(host, port, "client")
    key_exchange_algo, cipher, hmac = neg.handshake(server, "client")
    key_exchange(server, key_exchange_algo, "client")
