import secrets


def key_exchange(key_exchange):
    if key_exchange == "DH":
        DH(server)
    elif key_exchange == "RSA":
        RSA(server)
    elif key_exchange == "ECC":
        ECC(server)
    elif key_exhange == "PSK":
        PSK(server)


# -----------------------------------------------------------------------------
def DH(server):
    print("Running Diffie-Hellman Key Exchange")


# -----------------------------------------------------------------------------
def RSA(server):
    print("Running RSA Key Exchange")

# -----------------------------------------------------------------------------
def ECC(server):
    print("Running ECC Key Exchange")

# -----------------------------------------------------------------------------
def PSK(server):
    print("Running PSK key-exchange")
