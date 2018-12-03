from TcpServer import TcpServer
from negotiation import handshake
from key_exchange import key_exchange
from hashing import HMAC
from ciphers import Blum, TDES
from signature import RSA

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    server = TcpServer(host, port, "client")
    key_exchange_algo, cipher_algo, signature_algo, hmac = handshake(server, "client")
    session_key = key_exchange(server, key_exchange_algo, "client")
    bin_session_key = bin(session_key)[2:]
    keys = []
    for i in range(0, 256, 64):
        keys.append(int(bin_session_key[i:i+64], 2))

    # get helper objects for encryption, hashing, and signature
    # if cipher_algo == "BG":
        # cipher = Blum()

    cipher_algo = "TDES"
    if cipher_algo == "TDES":
        cipher = TDES(keys[0], keys[1], keys[2])

    hmac_generator = HMAC(str(keys[3]))

    print("\nKeys have been exchanged. Ready to send messages.")
    print("Encrypting with {0}, hashing with {1} and signing with {2}".format(cipher_algo, signature_algo, hmac))

    # secure communication
    plaintext = input("--> ")
    while plaintext != "quit" or plaintext != "exit" or plaintext != "q":
        hashed = hmac_generator.compute(plaintext)
        print("Hashed the message:", hashed)

        # CHANGE THIS TO CIPHERTEXT ONCE THE CIPHERS ARE DONE
        ciphertext = cipher.encrypt(plaintext)
        msg = {
            "msg" : ciphertext,
            "hash" : hashed
        }
        server.send(msg)

        # wait for response
        data = server.receive()
        print('Received from server: ',data)
        response = cipher.decrypt(ciphertext)

        plaintext = input("--> ")