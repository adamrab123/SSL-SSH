import secrets
from math import gcd
from ciphers import modInverse
from hashing import SHA1

class RSA:
    def __init__(self, secrets_file="", e=0, N=0):
        self.p = 0
        self.q = 0
        self.N = N
        self.e = e
        self.d = 0
        self.phi_n = 0
        self.hasher = SHA1()

        # gen keys if needed, else we are only using this to verify
        # signatures form the server
        if self.e == 0 and self.N == 0:
            self.keygen(secrets_file)

    def keygen(self, secrets_file):
        print("\nRunning key generation for RSA.")
        with open(secrets_file) as f:
            self.p = int(f.readline())
            self.q = int(f.readline())
            self.N = self.p * self.q
            self.phi_n = (self.p - 1) * (self.q - 1)
            self.e = secrets.randbelow(self.phi_n)
            while (gcd(self.e, self.phi_n) != 1):
                print("RSA: e and phi are not co-prime. Re-rolling.")
                self.e = secrets.randbelow(self.phi_n)
            self.d = modInverse(self.e, self.phi_n)

    def sign(self, message):
        hashed = self.hasher.hash(message)
        hashed_int = int(hashed,16)
        signed = pow(hashed_int,self.d,self.N)
        return signed

    def verify(self, message, signature):
        hashed = self.hasher.hash(message)
        decrypted = pow(signature, self.e, self.N)
        print(decrypted)
        hashed_int = int(hashed,16)
        return (hashed_int == decrypted)
