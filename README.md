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
This launches a TCP socket and attempt to establish a connection with the server. If successful, the client will initiate the handshake protocol by sending a dictionary with all protocols to the server:
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

The client receives the response from the server containing the server's choices from the cipher suite as well as the signed value and the public key for the RSA signature. The client can then verify the server's signature, and outputs an appropriate message if successful:
```
Verifying server signature...
Signature from server is verified. Communication can continue.
```
If unsuccessful, the connection is closed and the program is terminated.
Once the server is verified and the handshake is complete, the key exchange protocol is run. For both cases, large random numbers (1024-bit for Diffie-Hellman and 256-bit for ECC) are generated for both the client and server and the appropriate information is exchanged. The server outputs its public key to get a sense of how large the numbers are. Server:
```
Running Diffie-Hellman Key Exchange
Generated a private key and an exchange key. Sending exchange key to client
Exchange key: 51049796633367923878763089559096334560268338561585619906085487212790084424194514949783484478082797869615392349018071417165546988026519653596614719083399776779745744944150799235903692362437998737922379706854506457315094571494407589026251070433200425973844527419089377011978421223849006009887245773506707502599
```

A secure communication channel is now set up, and the server has been verified through blind signature. Messages can now be securely exchanged. A prompt will appear in the client terminal, where the user can enter what message they want to send to the server:
```
Keys have been exchanged. Ready to send messages.
Encrypting with TDES, hashing with SHA-1, and verifying signature with RSA

-->
```

Upon entering a message, the HMAC is computed, the message is encrypted, and both are sent to the server.
Client:
```
--> hello
Computed HMAC: febb7a15ab5eb1fbdadb6b51f7ce515fdba61a9e
Encrypted: 0001000111100100010100110100001100110110110110111100110101101001
Sending ciphertext and HMAC to the server
```
Upon receiving the message, the server decrypts the message, computes the HMAC of the plaintext and compares it to the HMAC sent from the client. If they are not equal, the program is terminated. If they are, then the server reverses the plaintext, computes the hash, encrypts the plaintext and sends the cipher text and hash to the client, where the client follows the same procedure.
Server:
```
Received encrypted msg: 0001000111100100010100110100001100110110110110111100110101101001
Client HMAC: febb7a15ab5eb1fbdadb6b51f7ce515fdba61a9e
Decrypting...
Plaintext from client: hello
Computing HMAC... febb7a15ab5eb1fbdadb6b51f7ce515fdba61a9e
Hashes match. Data integrity maintained.
Reversing the plaintext and echoing to client
```

Project writeup (we opted to create one longer writeup to not bore the graders with the same writeup 3 times over): https://docs.google.com/document/d/1p7xu87DeFxT94hb90uiroPHekZe1nagRAS--X8ujVkk/edit?usp=sharing
