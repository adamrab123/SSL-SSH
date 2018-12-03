import DES
import numpy as np
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


# # Blum-Goldwasser -------------------------------------------------------------
# # THIS IS BROKEN

# class Blum:
#     def __init__(self):
#         self.X = 0
#         self.M = 0
#         self.p = 65147
#         self.q = 78311
#         self.x0 = 159201

#     def getBit(self):
#         bit = self.X % 2
#         self.X = pow(self.X,2,self.M)
#         return bit

#     def encrypt(self, plaintext):
#         pass
#     	# blum = Blum(p* q, x0)
#     	# new = [blum.getBit() ^ bit for bit in message]
#     	# return new, blum.X

#     def decrypt(self, ciphertext):
#         pass
#     	# r_p = pow(x_l, pow((p+1)//4,len(encrypted),p-1) ,p)
#     	# r_q = pow(x_l, pow((q+1)//4,len(encrypted),q-1) ,q)
#     	# x_0 = (r_q * p * modInverse(p,q) + r_p *q * modInverse(q,p)) % (p*q)
#     	# decrypted = encrypt(encrypted,x_0)[0]
#     	# return decrypted




# Triple DES ------------------------------------------------------------------
class TDES:
    def __init__(self, k1, k2, k3):
        self.k1 = DES.to_bits(k1,64)
        self.k2 = DES.to_bits(k2,64)
        self.k3 = DES.to_bits(k3,64)


    def encrypt(self, plaintext):
        to_encrypt = np.unpackbits(bytearray(plaintext,'utf_8'))
        to_encrypt = np.pad(to_encrypt, pad_width=(64-(len(to_encrypt) % 64), 0), mode='constant').reshape(-1,64)
        encrypted_once = np.apply_along_axis(DES.apply_DES, 1, to_encrypt, self.k1,True).astype(np.uint8)
        encrypted_twice = np.apply_along_axis(DES.apply_DES, 1, encrypted_once, self.k2,False).astype(np.uint8)
        encrypted_thrice = np.apply_along_axis(DES.apply_DES, 1, encrypted_twice, self.k3,True).astype(np.uint8)
        return "".join(encrypted_thrice.flatten().astype(str).tolist())

    def decrypt(self, ciphertext):
        to_decrypt = np.array(list(ciphertext)).reshape(-1,64).astype(np.uint8)
        decrypted_once = np.apply_along_axis(DES.apply_DES, 1, to_decrypt, self.k3,False).astype(np.uint8)
        decrypted_twice = np.apply_along_axis(DES.apply_DES, 1, decrypted_once, self.k2,True).astype(np.uint8)
        decrypted_thrice = np.apply_along_axis(DES.apply_DES, 1, decrypted_twice, self.k1,False).astype(np.uint8)
        packed = np.packbits(decrypted_thrice);
        return "".join([chr(item) for item in packed]).replace("\x00","")


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