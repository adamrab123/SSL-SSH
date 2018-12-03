# Transport Layer Security
This is an implementation of TLS. Computational Diffie-Hellman and ECC are available for key exchange, RSA is used for signatures, SHA-1 is used for HMAC, and Triple-DES is used for as the symmetric cipher.

## The Code
* `server.py` : ciphers.py - this file contains the classes for each cipher in our cipher suite. In our case, since we are adhering to TLS 1.3 as closely as possible, this just includes Triple DES (for future improvemenets this will be replaced by AES). The actual source code for Triple DES is in the file DES.py; ciphers.py acts as a wrapper for future possible additions of other ciphers.
* `client.py` - this file serves as the connection client A (e.g. Alice) uses to connect to the server for communication. It will connect the user to the server using Diffie-Hellman or Elliptic-curve Diffie–Hellman (whichever the server picks), will use TripleDES to encrypt and decrypt messages and use HMAC-SHA1 to authenticate message integrity.
* `DES.py` - this file contains the source code implementation for Triple DES
* `ECCDH.py` - this file contains the source code implementation for the Elliptic-curve Diffie–Hellman key exchange. This includes adding points in the elliptic curve, multiplying points, verifying points, etc.
* `hashing.py` - this file contains the source code implementation for both SHA-1 and HMAC.
* `key_exchange.py` - this file contains the source code implementations for both Computational Diffie-Hellman and Elliptic-curve Diffie–Hellman.
* `negotiation.py` - this file contains the implementation of the hand
  server.py - this file will serve as our main server for this cryptosystem. The server will have the ability to use both Computational Diffie-Hellman and Elliptic-curve Diffie–Hellman to create trusted session keys with each client that connects to it, use TripleDES to encrypt and decrypt messages, and use HMAC-SHA1 to authenticate message integrity.
* `signature.py` - this file contains the code adhering to blind-signing messages using RSA blind-signing. It is used in the key exchange protocol part of the cryptosystem setup.
* `TcpServer.py` - this file contains the custom TCP server class created for this cryptosystem. implements the server-side of the application


# How to Run
First, run the server:
```bash
python server.py
```
This will launch a TCP server and block until a client connects. The server is single threaded. Only one client can connect at a time. If the client disconnects, the server shuts down.

Then, run the client:
```bash
python client.py
```
This launch a TCP socket and attempt to establish a connection with the server. If successful, the client will initiate the handshake protocol by sending a dictionary with all protocols to the server:
```python
all_protocols = {
    "key_exchange" : ["DH", "ECC"],
    "cipher" : ["TDES"],
    "signature" : "RSA",
    "HMAC" : "SHA-1",
    "random_value" : None
}
```
A random value is generated and included in the message. When the server receives the message, it randomly chooses a key exchange protocol, generates RSA keys from stored prime numbers, and signs the random value. The public key `e` is randomly generated, so sometimes it needs to be regenerated because it is not co-prime with `phi`:
```
Running key generation for RSA.
RSA: e and phi are not co-prime. Re-rolling.
RSA: e and phi are not co-prime. Re-rolling.
RSA: e and phi are not co-prime. Re-rolling.
```


To run:



Project writeup: https://docs.google.com/document/d/1p7xu87DeFxT94hb90uiroPHekZe1nagRAS--X8ujVkk/edit?usp=sharing
