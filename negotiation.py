import secrets
from signature import RSA

all_protocols = {
    "key_exchange" : ["DH", "ECC"],
    "cipher" : ["TDES"],
    "signature" : "RSA",
    "HMAC" : "SHA-1",
    "random_value" : None
}

def handshake(server, role, signer_object=None):
    if role == "server":
        client_protocols = server.receive()
        print("\nReceived Cipher Suite from client\n  Key exchange protocols: ", end="")
        for kep in client_protocols["key_exchange"]: print(kep, end=" ")
        print("\n  Ciphers: ", end="")
        for c in client_protocols["cipher"]: print(c, end=" ")
        print("\n  Signature: ", client_protocols["signature"], end="")
        print("\n  HMAC: ", client_protocols["HMAC"])

        # pick at random from the options sent by the client
        print("\nMaking random choice. Using:")
        key_exchange = secrets.choice(client_protocols["key_exchange"])
        cipher = secrets.choice(client_protocols["cipher"])
        signature = client_protocols["signature"]
        hmac = client_protocols["HMAC"]
        random_value = client_protocols["random_value"]
        print("  Key Exchange: {0}\n  Cipher: {1}\n  Signature: {2}\n  HMAC: {3}".format(key_exchange, cipher, signature, hmac))
        print("Signed client value. Sending public signature key and protocol choice.")
        msg = {
            "key_exchange" : key_exchange,
            "cipher" : cipher,
            "signature" : signature,
            "HMAC" : hmac,
            "e" : signer_object.e,
            "N" : signer_object.N,
            "signed" : signer_object.sign(client_protocols["random_value"])
        }
        server.send(msg)

        return key_exchange, cipher, signature, hmac


    elif role == "client":
        # generate random value for server to sign
        rand = str(secrets.randbelow(10000000))
        all_protocols["random_value"] = rand
        print("Generating random value for server to sign:", rand)

        print("Sending Cipher Suite to server. Awaiting response.")
        server.send(all_protocols)

        # unpack response
        protocol = server.receive()
        key_exchange = protocol["key_exchange"]
        cipher = protocol["cipher"]
        hmac = protocol["HMAC"]
        signature = protocol["signature"]
        print("Received server choice. Using:")
        print("  Key Exchange: {0}\n  Cipher: {1}\n  Signature: {2}\n  HMAC: {3}".format(key_exchange, cipher, signature, hmac))

        # verify signature
        signed = protocol["signed"]
        signature_verifier = RSA(e=protocol["e"], N=protocol["N"])
        print("\nVerifying server signature...")
        if signature_verifier.verify(rand, signed):
            print("Signature from server is verified. Communication can continue.")
        else:
            print("Signature verification failed")

        return key_exchange, cipher, signature, hmac, signature_verifier