import secrets


p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
n = 115792089210356248762697446949407573529996955224135760342422259061068512044369
a = -3
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
g_x = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
g_y = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5


def modInverse(a, m) :
    a = a % m
    for x in range(1, m) : 
        if ((a * x) % m == 1) : 
            return x 
    return 1


def verify_point(x,y):
    lhs = pow(y,2,p)
    rhs = (pow(x,3,p) + a * x + b) % p
    print(lhs)
    print(rhs)


def ECC_add(Xp,Yp,Xq,Yq,a):
    if Xp == Xq and Yp == Yq:
        Lambda = 3*(Xp**2) + a / (2 * Yp)
    else:
        Lambda = (Yq-Yp)/(Xq-Xp)
    Xr = Lambda**2 - Xp - Xq
    Yr = Lambda*(Xp-Xr)-Yp
    return [Xr,Yr]

# n = 128