# OAUTH

# CSRF Attack in OAuth (Login CSRF / OAuth Misbinding)

This describes how an OAuth flow can be exploited when the `state` parameter is missing or not verified.

---

## 🧠 Normal OAuth Flow (Expected Behavior)

1. User clicks “Login with Google”
2. App redirects user to Google OAuth URL
3. User authenticates with Google
4. Google redirects back with a `code`
5. App exchanges `code` for user identity

👉 The `code` links the user's Google account to their app account.

---

## 💥 The Vulnerability

If the app does **not** use or verify a `state` parameter:

> The app cannot verify that the same user who started the login flow is the one completing it.

---

## 🔥 Step-by-Step Attack

### 🎯 Scenario

* Target: HR web app
* Attacker: wants access to victim’s account
* Uses attacker’s own Google account

---

### 🔹 Step 1 — Attacker initiates OAuth

Attacker clicks “Login with Google”

Generated URL:

```
https://accounts.google.com/o/oauth2/v2/auth?
  client_id=HR_APP
  &redirect_uri=https://hr-app.com/callback
  &response_type=code
```

---

### 🔹 Step 2 — Attacker captures callback

After login, Google redirects to:

```
https://hr-app.com/callback?code=ATTACKER_CODE
```

👉 This `ATTACKER_CODE` is tied to the attacker’s Google account.

Attacker copies this URL instead of completing login.

---

### 🔹 Step 3 — Attacker sends crafted link

Victim receives:

```
https://hr-app.com/callback?code=ATTACKER_CODE
```

Via:

* phishing email
* hidden redirect
* malicious site

---

### 🔹 Step 4 — Victim visits the link

Victim is already logged into the HR app.

Browser sends:

* session cookies
* request to `/callback`

---

### 🔹 Step 5 — App accepts it blindly

App processes:

```
code=ATTACKER_CODE
```

Then:

* exchanges it with Google
* gets attacker’s identity
* links it to victim’s account

---

## 💥 Result

* Victim’s account is now linked to attacker’s Google account
* Attacker can log in as victim using Google
* Attacker gains access to victim’s data

---

## 🧠 Root Cause

The app assumes:

> “The user completing the OAuth flow is the same one who started it.”

This assumption is false without verification.

---

## 🔐 Mitigation: `state` Parameter

### ✅ Step 1 — Generate state

```
const state = crypto.randomUUID()
```

Store in:

* cookie
* session

---

### ✅ Step 2 — Include in OAuth request

```
https://accounts.google.com/o/oauth2/v2/auth?
  ...
  &state=RANDOM_123
```

---

### ✅ Step 3 — Google returns state

```
https://hr-app.com/callback?code=XYZ&state=RANDOM_123
```

---

### ✅ Step 4 — Verify state

```
if (req.query.state !== cookie.state) {
  throw new Error("Invalid state")
}
```

---

## 🚫 Attack After Fix

Attacker sends:

```
https://hr-app.com/callback?code=ATTACKER_CODE&state=ATTACKER_STATE
```

Victim has:

```
cookie.state = VICTIM_STATE
```

👉 Mismatch → request rejected

---

## 🧠 Simple Analogy

Without `state`:

> Anyone can complete the login flow

With `state`:

> Only the user who started the flow can complete it

---

## ⚠️ Key Insight

This attack does NOT steal credentials.

It:

> forces the victim to log in as the attacker

---

## 🔥 Impact

* Account takeover
* Unauthorized data access
* CRM / email exposure

---

## 🧠 One-Line Takeaway

> OAuth without `state` cannot guarantee request integrity and is vulnerable to CSRF.
