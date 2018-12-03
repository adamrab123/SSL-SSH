import secrets
from math import gcd
from ciphers import modInverse

class RSA:
    def __init__(self, secrets_file):
        self.p = 0
        self.q = 0
        self.N = 0
        self.e = 0
        self.d = 0
        self.phi_n = 0
        self.keygen(secrets_file)

    def keygen(self, secrets_file):
        with open(secrets_file) as f:
            self.p = int(f.readline())
            self.q = int(f.readline())
            self.N = self.p * self.q
            self.phi_n = (self.p - 1) * (self.q - 1)
            self.e = secrets.randbelow(self.phi_n)
            while (gcd(self.e, self.phi_n) != 1):
                print("Re-rolling")
                self.e = secrets.randbelow(self.phi_n)
            self.d = modInverse(self.e, self.phi_n)

    def sign(self):
        pass