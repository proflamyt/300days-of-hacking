---
title: "OAuth 2.0"
topic: "oauth"
tags: [oauth, oauth2, csrf, state-parameter, authorization-code, web-security]
difficulty: intermediate
day: 48
layout: default
parent: Topics
nav_order: 48
---

# OAuth 2.0

## What You Will Learn
- How the OAuth 2.0 authorization flow works
- What the `state` parameter does and why it is critical
- How CSRF attacks on OAuth flows work
- How to prevent OAuth CSRF vulnerabilities

## What Is It?

**OAuth 2.0** is an authorization framework that lets applications access resources on behalf of a user — without sharing the user's password. It is the standard behind "Login with Google", "Login with GitHub", etc.

OAuth has several security pitfalls. The most common is missing or unverified `state` parameter protection.

## Normal OAuth Flow

1. User clicks "Login with Google"
2. App redirects user to Google OAuth URL
3. User authenticates with Google
4. Google redirects back with a `code`
5. App exchanges `code` for user identity

The `code` links the user's Google account to their app account.

## CSRF Attack in OAuth — Login CSRF / OAuth Misbinding

This attack exploits OAuth flows when the `state` parameter is missing or not verified.

### The Vulnerability

If the app does **not** use or verify a `state` parameter, it cannot verify that the same user who started the login flow is the one completing it.

### Step-by-Step Attack

**Scenario**: HR web app, attacker wants access to victim's account using attacker's own Google account.

**Step 1 — Attacker initiates OAuth**

Attacker clicks "Login with Google". Generated URL:

```
https://accounts.google.com/o/oauth2/v2/auth?
  client_id=HR_APP
  &redirect_uri=https://hr-app.com/callback
  &response_type=code
```

**Step 2 — Attacker captures callback**

After login, Google redirects to:

```
https://hr-app.com/callback?code=ATTACKER_CODE
```

This `ATTACKER_CODE` is tied to the attacker's Google account. Attacker copies this URL instead of completing login.

**Step 3 — Attacker sends crafted link to victim**

```
https://hr-app.com/callback?code=ATTACKER_CODE
```

Sent via phishing email, hidden redirect, or malicious site.

**Step 4 — Victim visits the link**

Victim is already logged into the HR app. Browser sends session cookies + request to `/callback`.

**Step 5 — App accepts it blindly**

App processes `code=ATTACKER_CODE`:
- Exchanges it with Google
- Gets attacker's identity
- Links it to victim's account

### Result

Victim's account is now linked to the attacker's Google account. The attacker can log in as the victim using Google and gains access to victim's data.

### Root Cause

The app assumes: *"The user completing the OAuth flow is the same one who started it."* This assumption is false without verification.

## Mitigation: The `state` Parameter

### Step 1 — Generate state

```javascript
const state = crypto.randomUUID();
```

Store in cookie or session.

### Step 2 — Include in OAuth request

```
https://accounts.google.com/o/oauth2/v2/auth?
  ...
  &state=RANDOM_123
```

### Step 3 — Google returns state

```
https://hr-app.com/callback?code=XYZ&state=RANDOM_123
```

### Step 4 — Verify state

```javascript
if (req.query.state !== cookie.state) {
  throw new Error("Invalid state — possible CSRF attack");
}
```

### Why This Works

Attacker sends:

```
https://hr-app.com/callback?code=ATTACKER_CODE&state=ATTACKER_STATE
```

Victim has:

```
cookie.state = VICTIM_STATE
```

Mismatch — request rejected.

## Key Insight

This attack does **not** steal credentials. It forces the victim to log in as the attacker — linking the attacker's identity to the victim's account.

**Impact**: Account takeover, unauthorized data access, CRM and email exposure.

**One-line takeaway**: OAuth without `state` cannot guarantee request integrity and is vulnerable to CSRF.

## Resources

- [PortSwigger — OAuth Vulnerabilities](https://portswigger.net/web-security/oauth)
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)
- [TryHackMe — OAuth Attacks](https://tryhackme.com/)
- [HackTricks — OAuth Attacks](https://book.hacktricks.xyz/pentesting-web/oauth-to-account-takeover)
