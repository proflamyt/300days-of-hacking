# Certificates 

 Electronic credentials used to verify the identity of a user, device, or server, and to encrypt communication.


### SSL certificate 

A digital certificate that authenticates a website's identity and enables an encrypted connection between a web server and a web browser. 

```
certificate :
issued by 
issued to
public key
misc 
signature
```



### Certificate Authority (CA)

 A trusted third-party entity, known as a CA, issues the SSL certificate, which includes the public key along with the server’s identity information.

You genrate a public/private key pair, then request a certificate from the CA by providing a certificate signing request, which contains your domain details and your public key. The CA returns a certificate signed with its private key.

### How the SSL/TLS Handshake Works
The SSL/TLS handshake is the process of establishing a secure connection between the client and the server. Here’s how it works:

a. Client Hello

The client sends a "Client Hello" message to the server, which includes:
- The SSL/TLS version it supports.
- A randomly generated number (used in the creation of sessionwsssww2aqqqaA'/ keys).
- A list of supported cipher suites (encryption algorithms).
-

b. Server Hello

The server responds with a "Server Hello" message, which includes:
- The SSL/TLS version and cipher suite selected from the client's list.
- The server’s SSL certificate, containing its public key.
- A randomly generated number (used in the creation of session keys).

c. Certificate Verification

The client verifies the server’s certificate against a list of trusted CAs. If the certificate is valid, the handshake continues.





d. Pre-Master Secret Generation

- The client generates a pre-master secret, which is another random value, and encrypts it with the server’s public key.
- The client sends this encrypted pre-master secret to the server.

e. Session Key Derivation

- Both the client and server use the pre-master secret, along with the two random numbers exchanged earlier, to independently generate the same session key.
- This session key is symmetric, meaning the same key is used for both encryption and decryption of the data during the session.

f. Final Handshake

The client sends a “Finished” message encrypted with the session key, signaling that future communication will be encrypted.
The server responds with its own “Finished” message, also encrypted with the session key.



```python
import base64
from Crypto.PublicKey import RSA
import json
from Crypto.Hash.SHA256 import SHA256Hash
import pwn

user_key = RSA.generate(1024)

user_certificate = {
    "name": "ola",
    "issued by" : "ola",
    "issued to" : "bola",
    "key": {
        "e": user_key.e,
        "n": user_key.n,
    },
    "signer": "root",
}


root_trusted_certificates = {
    "root": user_certificate,
}


user_certificate_data = json.dumps(user_certificate).encode()


user_certificate_hash = SHA256Hash(user_certificate_data).digest()


target = pwn.process('/challenge/run')

target.readuntil("root key d: ")

d = target.readline()

target.readuntil("root certificate (b64): ")

certificate = target.readline()


cert = base64.b64decode(certificate)

root_cert =  json.loads(cert)

print(root_cert)

user_certificate_signature = pow(
    int.from_bytes(user_certificate_hash, "little"),
    int(d, 16),
    root_cert['key']['n']
).to_bytes(256, "little")

# print(base64.b64encode(user_certificate_signature))


target.readuntil("user certificate (b64): ")

target.sendline(base64.b64encode(user_certificate_data))

target.readuntil("user certificate signature (b64): ")

target.sendline(base64.b64encode(user_certificate_signature))

target.readuntil("secret ciphertext (b64): ")

cipher = target.readline()

c = base64.b64decode(cipher)

result =  pow(int.from_bytes(c, 'little'), user_key.d, user_key.n )


print(result.to_bytes(256, "little"))
```




### Certificate Pinning Bypass

