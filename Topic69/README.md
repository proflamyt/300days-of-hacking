---
title: "Frontend Vulnerabilities"
topic: "frontend-vulnerabilities"
tags: [frontend, javascript, postmessage, xss, dom, chrome-devtools, web-security]
difficulty: intermediate
day: 69
layout: default
parent: Topics
nav_order: 69
---

# Frontend Vulnerabilities

## What You Will Learn
- How to use Chrome DevTools for security testing
- What postMessage vulnerabilities are
- How to use URL APIs to find XSS sources
- How to set up local overrides for testing frontend code

## What Is It?

Frontend vulnerabilities are security issues that exist in client-side JavaScript. Unlike server-side issues, these run in the browser — making them harder to find with standard scanners. You need to manually trace data flows in JavaScript code.

## Why It Matters

Frontend bugs can lead to:
- XSS (cross-site scripting)
- postMessage hijacking
- DOM-based open redirects
- Client-side access control bypasses
- Sensitive data exposure in JavaScript

## Chrome DevTools

Chrome DevTools is your primary tool for frontend security testing.

### Debugging postMessage

```js
// Break when a postMessage event listener is called with origin "*"
debug(postMessage, 'argument[1] == "*"')

// Monitor all message events on the window
monitorEvents(window, 'message')
```

### Setting Up Local Overrides

Override JavaScript files served by the site with your modified versions:

1. Open Chrome DevTools
2. Go to the **Sources** tab
3. Find the **Overrides** panel
4. Click **Add Override Folder**
5. Select a directory to save your changes
6. Click **Allow** when Chrome asks for filesystem access

Now you can edit any JavaScript file and the modified version will load next time — without changing the server.

### Conditional Breakpoints

Right-click on a line number in Sources → Add conditional breakpoint → Enter a condition (e.g., `user == 'admin'`). Execution pauses only when the condition is true.

## URL and Location APIs

These properties and methods are common sources and sinks for DOM-based XSS:

```js
// Sources (attacker-controlled data)
url.searchParams          // URLSearchParams object
url.searchParams.get()    // Get specific parameter
url.searchParams.has()    // Check if parameter exists
window.location.href      // Full URL
window.location.search    // Query string

// Sinks (dangerous places to put data)
document.write()
innerHTML
eval()
location.href = data      // Open redirect or XSS if data = "javascript:..."
```

### History API

```js
history.pushState(state, title, url)   // Changes URL without page reload
history.replaceState(state, title, url) // Replaces current history entry
```

Attackers can manipulate these to confuse security checks that inspect `location.href`.

## postMessage Vulnerabilities

`postMessage` is the browser API for cross-origin communication between iframes and windows. If the receiver does not validate the origin of incoming messages, it is vulnerable.

**Vulnerable code:**

```js
window.addEventListener('message', function(event) {
    // No origin check!
    eval(event.data);
});
```

**Attack from attacker's page:**

```js
target = window.open('https://victim.com');
target.postMessage('alert(1)', '*');
```

**Safe code:**

```js
window.addEventListener('message', function(event) {
    if (event.origin !== 'https://trusted.example.com') return;
    // process event.data safely
});
```

## DOM XSS Sources and Sinks

When reading JavaScript, trace data from **sources** (user-controlled input) to **sinks** (dangerous functions):

Common **sources:**
- `location.search`, `location.hash`, `location.href`
- `document.cookie`
- `document.referrer`
- `window.name`
- `postMessage` event data

Common **sinks:**
- `document.write()`
- `innerHTML`, `outerHTML`
- `eval()`, `setTimeout(string)`, `Function(string)`
- `location.href = ...`
- `src`, `href` attributes set from data

## Resources

- [Beyond XSS — Advanced Frontend Attacks](https://aszx87410.github.io/beyond-xss/en/)
- [PortSwigger — DOM-Based XSS](https://portswigger.net/web-security/cross-site-scripting/dom-based)
- [PortSwigger — Web Message Vulnerabilities](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source)
- [Chrome DevTools — Sources Panel](https://developer.chrome.com/docs/devtools/sources/)
- [TryHackMe — DOM XSS](https://tryhackme.com/)
