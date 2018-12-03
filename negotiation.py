import secrets


all_protocols = {
    "key_exchange" : ["DH", "ECC"],
    "cipher" : ["BG", "TDES"],
    "signature" : "RSA",
    "HMAC" : "SHA-1"
}

def handshake(server, role):
    if role == "server":
        client_protocols = server.receive()
        print("Received Cipher Suite from client\n  Key exchange protocols: ", end="")
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
        print("  Key Exchange: {0}\n  Cipher: {1}\n  Signature: {2}\n  HMAC: {3}".format(key_exchange, cipher, signature, hmac))

        msg = {
            "key_exchange" : key_exchange,
            "cipher" : cipher,
            "signature" : signature,
            "HMAC" : hmac
        }
        server.send(msg)

    elif role == "client":
        print("Sending Cipher Suite to server. Awaiting response.")
        server.send(all_protocols)
        protocol = server.receive()
        key_exchange = protocol["key_exchange"]
        cipher = protocol["cipher"]
        hmac = protocol["HMAC"]
        signature = protocol["signature"]
        print("Received server choice. Using:")
        print("  Key Exchange: {0}\n  Cipher: {1}\n  Signature: {2}\n  HMAC: {3}".format(key_exchange, cipher, signature, hmac))

    return key_exchange, cipher, signature, hmac