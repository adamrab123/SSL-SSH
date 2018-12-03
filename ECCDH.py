import secrets
from ciphers import modInverse


p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
n = 115792089210356248762697446949407573529996955224135760342422259061068512044369
a = -3
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
g_x = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
g_y = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5

"""
p = 97
a = 2
b = 3
g_x = 3
g_y = 6
"""
g = (g_x,g_y)

def verify_point(x,y):
    lhs = pow(y,2,p)
    rhs = (pow(x,3,p) + a * x + b) % p
    return lhs == rhs


def point_add(i,j):
    if i==0:
        return j
    if j==0:
        return i
    i_x = i[0]
    i_y = i[1]
    j_x = j[0]
    j_y = j[1]
    if i_x + j_x == p:
        return 0
    if i_x == j_x and i_y != j_y:
        return 0
    if i_x == j_x:
        l = ((3 * pow(i_x,2,p) + a) * modInverse(2 * i_y, p)) % p
    else:
        l = ((j_y-i_y) * modInverse(((j_x-i_x)% p),p)) % p
    r_x = (pow(l,2,p) - i_x - j_x) % p
    r_y = (l * (i_x - r_x) - i_y) % p
    return (r_x,r_y)

def naive_point_multiply(q,d):
    x = (q[0],q[1])
    for i in range(d-1):
        x = point_add(q,x)
    return x
# n = 128

def point_multiply(q,d):
    r = 0
    doubling = q
    while d >0:
        lsb = d%2
        if lsb == 1:
            r = point_add(r,doubling)
        doubling = point_add(doubling,doubling)
        d = d//2
    return r

def generate_public_key(d):
    public_point = point_multiply(g,d)
    return public_point

def get_secret(q,d):
    secret = point_multiply(q,d)
    return secret[0]

if __name__ == "__main__":
    print("Beginning Elliptic Key Diffie-Hellman Test:")
    d_1 = secrets.randbelow(n)
    print("First random number:{}".format(d_1))
    q_1 = generate_public_key(d_1)
    print("Generating corresponding public key:")
    print(q_1)

    d_2 = secrets.randbelow(n)
    print("First random number:{}".format(d_2))
    q_2 = generate_public_key(d_2)
    print("Generating corresponding public key:")
    print(q_2)
    print("")

    print("Obtaining key from first private key:")
    result_1 = get_secret(q_2,d_1)
    print(result_1)

    print("Obtaining key from second private key:")
    result_2 = get_secret(q_1,d_2)
    print(result_2)