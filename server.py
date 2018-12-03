from TcpServer import TcpServer
from negotiation import handshake
from key_exchange import key_exchange
from hashing import HMAC
from ciphers import Blum, TDES
from signature import RSA

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    server = TcpServer(host, port)

    key_exchange_algo, cipher_algo, signature_algo, hmac = handshake(server, "server")
    session_key = key_exchange(server, key_exchange_algo, "server")
    bin_session_key = bin(session_key)[2:]
    keys = []
    for i in range(0, 256, 64):
        keys.append(int(bin_session_key[i:i+64], 2))
    print(keys)





    # get helper objects for encryption, hashing, and signature
    # if cipher_algo == "BG":
    #     cipher = Blum()
    cipher_algo = "TDES"
    if cipher_algo == "TDES":
        cipher = TDES(keys[0], keys[1], keys[2])
    hmac_generator = HMAC(str(keys[3]))

    signature = RSA("rsa_secrets.txt")

    print("\nKeys have been exchanged. Ready to receive messages.")
    print("Encrypting with {0}, hashing with {1} and signing with {2}".format(cipher_algo, signature_algo, hmac))

    while True:
        data = server.receive()
        print("Received encrypted data:", data)
        ciphertext = data["msg"]
        client_hash = data["hash"]

        # decrypt and verify the hash
        plaintext = cipher.decrypt(ciphertext)
        print("Plaintext from client:", plaintext)
        hash_verify = hmac_generator.compute(plaintext)
        if hash_verify != client_hash:
            print("Data integrity is compromised")
        else:
            print("Hashes match. Data integrity maintained.")

        # send the response, just the reverse of the plaintext
        ciphertext = cipher.encrypt(plaintext[::-1])
        hashed = hmac_generator.compute(plaintext[::-1])
        signed_hash = signature.sign(hashed)
        msg = {
            "msg" : ciphertext,
            "signature" : signed_hash
        }

        # for now just return the encrypted data
        server.send(msg)