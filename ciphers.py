# General Use -----------------------------------------------------------------
def modInverse(a, m) :
    a = a % m
    for x in range(1, m) : 
        if ((a * x) % m == 1) : 
            return x 
    return 1

# Blum-Goldwasser -------------------------------------------------------------
p = 65147
q = 78311
my_x0 = 159201

class Blum:
    def __init__(self,m,x):
        self.X = x
        self.M = m
    def getBit(self):
        bit = self.X % 2
        self.X = pow(self.X,2,self.M)
        return bit

def encrypt(message, x0):
	blum = Blum(p* q, x0)
	new = [blum.getBit() ^ bit for bit in message]
	return new, blum.X

def decrypt(encrypted, x_l):
	r_p = pow(x_l, pow((p+1)//4,len(encrypted),p-1) ,p)
	r_q = pow(x_l, pow((q+1)//4,len(encrypted),q-1) ,q)
	x_0 = (r_q * p * modInverse(p,q) + r_p *q * modInverse(q,p)) % (p*q)
	decrypted = encrypt(encrypted,x_0)[0]
	return decrypted




# Triple DES ------------------------------------------------------------------
class TDES:
    def __init__(self):
        pass


    def encrypt(self):
        pass

    def decrypt(self):
        pass


# ignore ======================================================================
if __name__ == "__main__":
    input = [1,0,0,1,1,1,0,0,0,0,0,1,0,0,0,0,1,1,0,0]
    print(input)
    encrypted, x_l = encrypt(input, my_x0)
    print(encrypted)
    decrypted = decrypt(encrypted, x_l)
    print(decrypted)
    assert(decrypted == input)
    # print(p * a + b * q)