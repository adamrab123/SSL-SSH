import secrets
import ECCDH
# -----------------------------------------------------------------------------
def key_exchange(server, key_exchange, role):

    # FOR TESTING
    # key_exchange = "DH"

    if key_exchange == "DH":
        session_key = DH(server, role)
    elif key_exchange == "ECC":
        session_key = ECC(server, role)

    return session_key

# -----------------------------------------------------------------------------
def DH(server, role):
    print("\nRunning Diffie-Hellman Key Exchange")
    p = 137379528414317606724783492848081555720283075091870828195519131515167070861754597199829274387302328027015419063936033191563930078052582356021467556154341659725297054437914526417256171045697340225118653762315080757061962488124994375567389300922747400080660694665773568950985145405095127742611044300419476060483
    g = 71
    a = secrets.randbelow(p-1)
    public_key = pow(g, a, p)
    if role == "server":
        print("Generated a private key and an exchange key. Sending exchange key to client")
        print("Generated key:", public_key)
        print("Sending to client")
        server.send(public_key)

        # get response from client and generate session key
        received_key = server.receive()

    elif role == "client":
        received_key = server.receive()
        print("Received public key from server. Generating private key")
        print("Received:", received_key)

        server.send(public_key)

    session_key = pow(received_key, a, p)
    print("Determined session key:", session_key)
    return session_key

# -----------------------------------------------------------------------------
def ECC(server, role):
    print("Running ECC Key Exchange")
    d = secrets.randbelow(ECCDH.n)
    public_key = ECCDH.generate_public_key(d)
    if role == "server":
        print("Generated a private key and an exchange key. Sending exchange key to client")
        print("Generated key:", public_key)
        print("Sending to client")
        server.send(public_key)

        # get response from client and generate session key
        received_key = server.receive()

    elif role == "client":
        received_key = server.receive()
        print("Received public key from server. Generating private key")
        print("Received:", received_key)

        server.send(public_key)

    session_key = ECCDH.get_secret(received_key,d)
    print("Determined session key:", session_key)
    return session_key