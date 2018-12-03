# Transport Layer Security
This is an implementation of TLS. Computational Diffie-Hellman and ECC are available for key exchange, RSA is used for signatures, SHA-1 is used for HMAC, and Triple-DES is used for as the symmetric cipher.

## The Code
* `server.py` : implements the server-side of the application
* `client.py` : implements the client side of the application


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



List of things we need to do:

1. Triple-Des and/or AES
2. ~~HMAC-SHA1~~
3. RSA
4. ECC
5. ~~BG~~
6. Network-aspect

Project writeup: https://docs.google.com/document/d/1p7xu87DeFxT94hb90uiroPHekZe1nagRAS--X8ujVkk/edit?usp=sharing
