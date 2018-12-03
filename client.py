from TcpServer import TcpServer
from negotiation import handshake
from key_exchange import key_exchange
from hashing import HMAC
from ciphers import TDES
from signature import RSA

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    server = TcpServer(host, port, "client")

    # protocol handshake and key exchange
    key_exchange_algo, cipher_algo, signature_algo, hmac, signature_verifier = handshake(server, "client")
    session_key = key_exchange(server, key_exchange_algo, "client")
    bin_session_key = bin(session_key)[2:]
    keys = []
    for i in range(0, 256, 64):
        keys.append(int(bin_session_key[i:i+64], 2))

    # get helper objects for encryption and hmac
    if cipher_algo == "TDES":
        cipher = TDES(keys[0], keys[1], keys[2])
    hmac_generator = HMAC(str(keys[3]))

    # ready for secure communication
    print("\nKeys have been exchanged. Ready to send messages.")
    print("Encrypting with {0}, hashing with {1}, and verifying signature with {2}\n".format(cipher_algo, hmac, signature_algo))

    plaintext = input("--> ")
    while plaintext != "quit\n" or plaintext != "exit\n" or plaintext != "q\n":

        # encrypt and hash the message, send to server
        hashed = hmac_generator.compute(plaintext)
        ciphertext = cipher.encrypt(plaintext)
        print("Computed HMAC:", hashed)
        print("Encrypted:", ciphertext)
        print("Sending ciphertext and HMAC to the server\n")
        msg = {
            "msg" : ciphertext,
            "hash" : hashed
        }
        server.send(msg)

        # receive server response
        data = server.receive()
        ciphertext, server_hash = data["msg"], data["hash"]
        print("Received encrypted msg:", ciphertext)
        print("Server HMAC:", server_hash)
        print("Decrypting...")
        response = cipher.decrypt(ciphertext)
        print("Server Response:", response)
        hash_verify = hmac_generator.compute(response)
        print("Computing HMAC...", hash_verify)
        if hash_verify != server_hash:
            print("Hashes do not match. Data integrity is compromised. Closing connection.")
            exit()
        else:
            print("Hashes match. Data integrity maintained.")

        # send another message
        plaintext = input("\n--> ")