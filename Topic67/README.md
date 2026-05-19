---
title: "Certificates and PKI"
topic: "certificates-pki"
tags: [ssl, tls, certificates, pki, ca, certificate-pinning, handshake, x509]
difficulty: intermediate
day: 67
layout: default
parent: Topics
nav_order: 67
---

# Certificates and PKI

## What You Will Learn
- What digital certificates are and what they contain
- How the SSL/TLS handshake works step by step
- What a Certificate Authority (CA) is
- How certificate pinning works and how to bypass it
- How to implement and work with certificates in Python

## What Is It?

**Digital certificates** are electronic credentials used to verify the identity of a user, device, or server, and to encrypt communication. They are the foundation of HTTPS and Public Key Infrastructure (PKI).

## SSL Certificates

An SSL/TLS certificate is a digital certificate that authenticates a website's identity and enables an encrypted connection between a web server and a web browser.

A certificate contains:

```
certificate:
  issued by    (the CA that signed it)
  issued to    (the domain or entity)
  public key   (used to encrypt data)
  validity     (not before / not after dates)
  signature    (the CA's signature over all the above)
```

## Certificate Authority (CA)

A **CA** is a trusted third-party entity that issues SSL certificates. The CA verifies your identity and signs your certificate with its own private key.

To get a certificate:
1. Generate a public/private key pair
2. Create a Certificate Signing Request (CSR) containing your domain details and public key
3. Submit the CSR to the CA
4. CA verifies ownership (DV), organization (OV), or extended info (EV)
5. CA returns a certificate signed with its private key

## How the SSL/TLS Handshake Works

### a. Client Hello

The client sends a "Client Hello" message including:
- The SSL/TLS version it supports
- A randomly generated number (used to derive session keys)
- A list of supported cipher suites (encryption algorithms)

### b. Server Hello

The server responds with:
- The selected TLS version and cipher suite
- The server's SSL certificate (containing its public key)
- A randomly generated number

### c. Certificate Verification

The client verifies the server's certificate against its list of trusted CAs. If valid, the handshake continues.

### d. Pre-Master Secret Generation

- The client generates a pre-master secret and encrypts it with the server's public key
- The client sends this encrypted value to the server

### e. Session Key Derivation

Both sides use:
- The pre-master secret
- The two random numbers from steps a and b

...to independently derive the same symmetric session key.

### f. Final Handshake

The client sends a "Finished" message encrypted with the session key, and the server responds with its own "Finished" message. All future data is encrypted.

## Certificate Pinning

**Certificate pinning** is a defense mechanism where a client hardcodes the expected certificate (or its hash) for a specific server. If the certificate changes — even to a valid CA-signed one — the connection is rejected.

Pinning is commonly used in mobile apps to prevent MITM attacks with custom CA certificates.

### Pinning Bypass

For penetration testing of mobile apps, pinning must be bypassed to intercept HTTPS traffic:

```bash
# Frida-based bypass (Android)
objection patchapk -s target.apk
objection --gadget "com.target.app" explore
android sslpinning disable

# Using Frida script directly
frida -U -f com.target.app -l ssl_bypass.js
```

### Network-Level Port Forwarding

For intercepting traffic on Windows with Burp:

```cmd
netsh interface portproxy add v4tov4 listenport=9900 listenaddress=0.0.0.0 connectport=9900 connectaddress=<burp_host>
netsh interface portproxy show v4tov4
```

## Working with Certificates in Python

```python
import base64
from Crypto.PublicKey import RSA
from Crypto.Hash.SHA256 import SHA256Hash
import json

# Generate RSA key pair
user_key = RSA.generate(1024)

# Create a certificate (simplified)
user_certificate = {
    "name": "ola",
    "issued by": "ola",
    "issued to": "bola",
    "key": {
        "e": user_key.e,
        "n": user_key.n,
    },
    "signer": "root",
}

# Hash the certificate data
cert_data = json.dumps(user_certificate).encode()
cert_hash = SHA256Hash(cert_data).digest()

# Sign with a private key (using RSA raw signing)
signature = pow(
    int.from_bytes(cert_hash, "little"),
    user_key.d,
    user_key.n
).to_bytes(256, "little")

print(base64.b64encode(signature))
```

## Resources

- [Let's Encrypt — Free SSL Certificates](https://letsencrypt.org/)
- [PortSwigger — TLS Security](https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-in-error-messages)
- [Mozilla — SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [Frida — SSL Pinning Bypass](https://github.com/httptoolkit/frida-android-unpinning)
- [TryHackMe — TLS](https://tryhackme.com/)
