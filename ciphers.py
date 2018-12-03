# General Use -----------------------------------------------------------------
def modInverse(a, m) : 
    m0 = m 
    y = 0
    x = 1
  
    if (m == 1) : 
        return 0
  
    while (a > 1) : 
        # q is quotient 
        q = a // m 
        t = m 
  
        # m is remainder now, process 
        # same as Euclid's algo 
        m = a % m 
        a = t 
        t = y 
  
        # Update x and y 
        y = x - q * y 
        x = t 
  
    # Make x positive 
    if (x < 0) : 
        x = x + m0 
  
    return x 

# Blum-Goldwasser -------------------------------------------------------------


# THIS IS BROKEN

class Blum:
    def __init__(self):
        self.X = 0
        self.M = 0
        self.p = 65147
        self.q = 78311
        self.x0 = 159201

    def getBit(self):
        bit = self.X % 2
        self.X = pow(self.X,2,self.M)
        return bit

    def encrypt(self, plaintext):
        pass
    	# blum = Blum(p* q, x0)
    	# new = [blum.getBit() ^ bit for bit in message]
    	# return new, blum.X

    def decrypt(self, ciphertext):
        pass
    	# r_p = pow(x_l, pow((p+1)//4,len(encrypted),p-1) ,p)
    	# r_q = pow(x_l, pow((q+1)//4,len(encrypted),q-1) ,q)
    	# x_0 = (r_q * p * modInverse(p,q) + r_p *q * modInverse(q,p)) % (p*q)
    	# decrypted = encrypt(encrypted,x_0)[0]
    	# return decrypted




# Triple DES ------------------------------------------------------------------
class TDES:
    def __init__(self):
        pass


    def encrypt(self, plaintext):
        pass

    def decrypt(self, ciphertext):
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