class SHA1:
    def __init__(self):
        self.h0 = 0x67452301
        self.h1 = 0xEFCDAB89
        self.h2 = 0x98BADCFE
        self.h3 = 0x10325476
        self.h4 = 0xC3D2E1F0

    def hash(self, msg):
        bit_str = self.preprocess(msg)
        chunks = self.get_chunks(bit_str)

        for chunk in chunks:
            # separate 512 bit chunk into 32-bit words
            words = self.get_chunks(chunk, 32)
            
            # the first 16 words are the chunks
            w = [int(word, 2) for word in words[0:16]]
            w += [0]*64

            # then do some weird math for the remaining 64 words
            for i in range(16, 32):
                w[i] = self.rotate_left((w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16]), 1)
            for i in range(32, 80):
                w[i] = self.rotate_left((w[i-6] ^ w[i-16] ^ w[i-28] ^ w[i-32]), 2)
            # print(w)

            a, b, c, d, e = self.hash_it_up(w)

            self.h0 = self.h0 + a & 0xffffffff
            self.h1 = self.h1 + b & 0xffffffff
            self.h2 = self.h2 + c & 0xffffffff
            self.h3 = self.h3 + d & 0xffffffff
            self.h4 = self.h4 + e & 0xffffffff

        return "%08x%08x%08x%08x%08x" % (self.h0, self.h1, self.h2, self.h3, self.h4)


    def hash_it_up(self, w):
        a, b, c, d, e = self.h0, self.h1, self.h2, self.h3, self.h4
        for i in range(80):
            if i <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif i <= 59:
                f = (b & c) | (b & d) | (c & d) 
                k = 0x8F1BBCDC
            elif i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = self.rotate_left(a, 5) + f + e + k + w[i] & 0xffffffff
            e, d, c, b, a = d, c, self.rotate_left(b, 30), a, temp

        return a, b, c, d, e
            # d = c
            # c = b leftrotate 30
            # b = a
            # a = temp
            
    def preprocess(self, msg):
        bit_str = self.convert_to_bits(msg)

        # pad with a single 1, then pad with 0s until length is congruent to
        # 448 mod 512
        bit_str += "1"
        padding = 448 - (len(bit_str) % 512)
        bit_str += "0" * padding

        # append the length of the message as a 64 bit value
        bit_str += "{0:064b}".format(len(msg) * 8)
        assert(len(bit_str) % 512 == 0)

        return bit_str

    def convert_to_bits(self, msg):
        bit_str = ""
        for n in range(len(msg)):
            bit_str += "{0:08b}".format(ord(msg[n]))
        return bit_str


    def get_chunks(self, data, size=512):
        # return np.split(data, data.size // size)
        return [data[i:i+size] for i in range(0, len(data), size)]

    def rotate_left(self, data, n):
        return ((data << n) | (data >> (32 - n))) & 0xffffffff




if __name__ == "__main__":
    msg = "hello world, I am implementing the secure hash algorithm, version \
    1 (a.k.a. SHA-1) and need at least five hundred and twelve characters to \
    test that the chunk separation is working correctly. PLease ignore this \
    message. Thanks. By the way that whole previous message was only two \
    hundred and thirty five characters, so I guesssssssss I neeeeeeeeeeeeeeee\
    eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeddddddddddddddddd wwwwaaaaaaayyyyy\
    yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy moreee than that"

    msg2 = "test"
    msg3 = "The quick brown fox jumps over the lazy dog"
    msg4 = "hello world"
    # print(len(msg))
    hmac = SHA1()
    result = hmac.hash(msg4)
    print(result)

    # print(result, " = de9f2c7fd25e1b3afad3e85a0bd17d9b100db4b3")
    # assert(result == 0xde9f2c7fd25e1b3afad3e85a0bd17d9b100db4b3)