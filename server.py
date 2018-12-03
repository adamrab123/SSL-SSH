from TcpServer import TcpServer
from negotiation import handshake
from key_exchange import key_exchange
from hashing import SHA1
from ciphers import Blum, TDES
from signature import RSA

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    server = TcpServer(host, port)

    key_exchange_algo, cipher_algo, signature_algo, hmac = handshake(server, "server")
    key_exchange(server, key_exchange_algo, "server")

    # get helper objects for encryption, hashing, and signature
    if cipher_algo == "BG":
        cipher = Blum()
    elif cipher_algo == "TDES":
        cipher = TDES()

    hasher = SHA1()
    signature = RSA()

    print("\nKeys have been exchanged. Ready to receive messages.")
    print("Encrypting with {0}, hashing with {1} and signing with {2}".format(cipher_algo, signature_algo, hmac))

    while True:
        data = server.receive()
        print("Received encrypted data:", data)

        # for now just return the encrypted data
        server.send(data)