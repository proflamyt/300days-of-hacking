---
title: "Nginx Misconfigurations"
topic: "nginx-misconfigurations"
tags: [nginx, misconfiguration, path-traversal, crlf, off-by-slash, web-security]
difficulty: intermediate
day: 65
layout: default
parent: Topics
nav_order: 65
---

# Nginx Misconfigurations

## What You Will Learn
- Common Nginx configuration mistakes that lead to vulnerabilities
- How the "off-by-slash" alias misconfiguration enables path traversal
- How `$uri` can cause CRLF injection
- How missing root location exposes files to the internet

## What Is It?

**Nginx** is one of the most widely deployed web servers and reverse proxies. Small mistakes in its configuration can create serious security vulnerabilities — path traversal, file disclosure, CRLF injection, and cache poisoning.

Many of these misconfigurations are subtle and easy to miss in code reviews.

## Why It Matters

These misconfigurations are common on bug bounty targets and real infrastructure. Finding them requires knowing what to look for in Nginx config files and how to test for them.

## Missing Root Location

If the `root` directive is set at the server level but only specific `location` blocks are defined, requests for other paths still use that root directory:

```nginx
server {
    root /etc/nginx;

    location /index.html {
        # only this is "intended"
    }
}
```

Any file within `/etc/nginx/` is now reachable — including sensitive files like `nginx.conf`, SSL certificates, or any other files in that directory.

**Test:**

```bash
curl https://target.com/nginx.conf
curl https://target.com/conf.d/default.conf
```

## Off-By-Slash (Alias Path Traversal)

The `alias` directive maps a URL path to a filesystem path. If the `location` block does not end with a `/` but the `alias` does, path traversal is possible.

**Vulnerable config:**

```nginx
location /cats {
    alias /usr/share/nginx/html/;
}
```

```bash
ls /usr/share/nginx/html/
# index.html  ola.html
```

**Test:** Check if both of these resolve to the same resource:

```bash
curl http://target/cats/index.html   # intended
curl http://target/catsindex.html    # traversal via off-by-slash
```

If both return the same content, path traversal exists. An attacker can use `..` to read files outside the intended directory:

```bash
curl "http://target/cats../etc/passwd"
```

**Fix:** Add a trailing slash to the location:

```nginx
location /cats/ {   # <-- trailing slash added
    alias /usr/share/nginx/html/;
}
```

## CRLF Injection via `$uri`

The variables `$uri` and `$document_uri` are already URL-decoded (normalized) by Nginx. When used in a `Location` redirect or response header, appending `%0d%0a` can inject CRLF (Carriage Return + Line Feed):

**Vulnerable config:**

```nginx
location / {
    return 301 https://example.com$uri;
}
```

**Attack:**

```
https://target.com/%0d%0aSet-Cookie:%20malicious=1
```

Nginx decodes `%0d%0a` to `\r\n`, injecting an HTTP header into the response. This can be used to:
- Set arbitrary cookies (session fixation)
- Inject fake headers
- Split the response (HTTP response splitting)

**Fix:** Use `$request_uri` instead of `$uri` for redirects — it is not decoded:

```nginx
return 301 https://example.com$request_uri;
```

## merge_slashes Off

By default, Nginx normalizes multiple slashes in URLs. Setting `merge_slashes off` can cause issues if backend applications assume normalized paths — potentially bypassing security controls that check the path.

```nginx
merge_slashes off;
```

With this, `//admin` is forwarded as-is to the backend, which might interpret it differently than the Nginx access control.

## Raw Backend Response Reading

If an attacker can influence the `X-Accel-Redirect` header (used for internal redirects), they may be able to read arbitrary files from the server.

## Resources

- [HackTricks — Nginx Misconfigurations](https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/nginx)
- [gixy — Nginx Security Scanner](https://github.com/yandex/gixy)
- [orangetsai — Breaking Parser Logic](https://i.blackhat.com/us-18/Wed-August-8/us-18-Orange-Tsai-Breaking-Parser-Logic-Take-Your-Path-Normalization-Off-And-Pop-0days-Out-2.pdf)
- [TryHackMe — Web Application Security](https://tryhackme.com/)
