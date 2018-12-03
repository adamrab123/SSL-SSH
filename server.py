from TcpServer import TcpServer
from negotiation import handshake
from key_exchange import key_exchange
from hashing import HMAC
from ciphers import TDES
from signature import RSA

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    server = TcpServer(host, port)

    # generate signatures to verify the server to the client    
    signature = RSA(secrets_file="rsa_secrets.txt")

    # protocol handshake and key exchange
    key_exchange_algo, cipher_algo, signature_algo, hmac = handshake(server, "server", signer_object=signature)
    session_key = key_exchange(server, key_exchange_algo, "server")
    bin_session_key = bin(session_key)[2:]
    keys = []
    for i in range(0, 256, 64):
        keys.append(int(bin_session_key[i:i+64], 2))

    # get helper objects for encryption and hmac
    if cipher_algo == "TDES":
        cipher = TDES(keys[0], keys[1], keys[2])
    hmac_generator = HMAC(str(keys[3]))

    # ready for secure communication
    print("\nKeys have been exchanged. Ready to receive messages.")
    print("Encrypting with {0}, hashing with {1}, and signing with {2}\n".format(cipher_algo, hmac, signature_algo))

    while True:

        # receive a message from the client
        data = server.receive()
        ciphertext, client_hash = data["msg"], data["hash"]
        print("Received encrypted msg:", ciphertext)
        print("Client HMAC:", client_hash)
        print("Decrypting...")

        # decrypt and verify the hash
        plaintext = cipher.decrypt(ciphertext)
        print("Plaintext from client:", plaintext)
        hash_verify = hmac_generator.compute(plaintext)
        print("Computing HMAC...", hash_verify)
        if hash_verify != client_hash:
            print("Hashes do not match. Data integrity is compromised. Closing connection.")
            exit()
        else:
            print("Hashes match. Data integrity maintained.")

        # send the response, just the reverse of the plaintext
        print("Reversing the plaintext and echoing to client\n")
        ciphertext = cipher.encrypt(plaintext[::-1])
        hashed = hmac_generator.compute(plaintext[::-1])
        # signed_hash = signature.sign(hashed)
        msg = {
            "msg" : ciphertext,
            "hash" : hashed
        }
        server.send(msg)