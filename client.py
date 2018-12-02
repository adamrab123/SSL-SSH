from TcpServer import TcpServer
import negotiation as neg






if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    server = TcpServer(host, port, "client")
    key_exchange, cipher, hmac = neg.handshake(server, "client")