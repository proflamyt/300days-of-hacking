---
title: "CVE Analysis — ProcessMaker XSS"
topic: "cve-analysis"
tags: [cve, xss, cookie, eval, javascript, web-security, writeup]
difficulty: intermediate
day: 57
layout: default
parent: Topics
nav_order: 57
---

# CVE Analysis — ProcessMaker XSS

## What You Will Learn
- What a CVE is and how vulnerability research works
- How cookie-based XSS vulnerabilities work
- Why `eval()` on user-controlled data is dangerous
- How to chain findings to create a full attack scenario

## What Is a CVE?

A **CVE (Common Vulnerabilities and Exposures)** is a publicly disclosed security vulnerability with a unique identifier like `CVE-2024-25506`. CVEs are assigned by CVE Numbering Authorities (CNAs) after a researcher discovers and reports a vulnerability.

Each CVE entry includes:
- Description of the vulnerability
- Affected software and versions
- CVSS severity score
- References to patches and write-ups

## CVE-2024-25506 — ProcessMaker Cookie-Based XSS

### Description

ProcessMaker was discovered to have an XSS vulnerability due to a vulnerable implementation of how the `workspace` parameter is stored as a cookie value.

The vulnerability occurs when the JavaScript tries to access a cookie named `pm_sys_sys` and convert its contents to an object using the `eval()` function.

### Root Cause

The code attempts to assign a JSON object to the `obj` variable using `eval()`. The insecure use of `eval()` enables a potential attacker who has control over the `pm_sys_sys` cookie to execute arbitrary JavaScript code.

```javascript
// Vulnerable code pattern
var obj = eval('(' + getCookie("pm_sys_sys") + ')');
// If the cookie contains: {"sys_sys": "workflow", "ola": alert(1)}
// Then eval executes: alert(1)
```

### Crafting an Exploit

A JavaScript `eval()` function executes its string argument as JavaScript code. By creating a JSON value that contains a JavaScript function, an attacker can execute arbitrary code on the vulnerable web application.

**Final payload** — set the cookie `pm_sys_sys` to:

```json
{"sys_sys": "workflow", "ola": alert(1)}
```

This means an attacker can execute arbitrary JavaScript while setting the workspace field to the intended value for unsuspecting users.

```javascript
// Set the malicious cookie
document.cookie = 'pm_sys_sys={"sys_sys": "workflow", "ola": alert(1)};domain=example.com;path=/;expires=2070-01-01'
```

### Full Attack Scenario

1. Attacker finds a separate XSS, subdomain takeover, or CRLF injection vulnerability on `*.example.com`
2. Attacker uses that vulnerability to set the cookie `pm_sys_sys` with the malicious payload, targeting the main domain where ProcessMaker runs
3. When an infected user visits the ProcessMaker login page at `sys/en/*/login/login`, the XSS triggers
4. Since this is the **login page**, the exploit could be a keylogger to capture admin credentials

### Why This Is Dangerous

- The attack chains two vulnerabilities (initial cookie injection + this eval XSS)
- It targets the login page — ideal for credential harvesting
- The malicious cookie blends in with legitimate cookie data

### Fix

Never use `eval()` on user-controlled data. Use `JSON.parse()` instead:

```javascript
// Safe alternative
try {
    var obj = JSON.parse(getCookie("pm_sys_sys"));
} catch (e) {
    var obj = {};
}
```

`JSON.parse()` only parses data — it does not execute code.

## CVE Research Process

1. Find a vulnerability through code review, fuzzing, or dynamic testing
2. Confirm it is exploitable
3. Identify the affected software version
4. Contact the vendor (responsible disclosure)
5. Vendor patches and assigns a CVE
6. Public disclosure after patch is available

## Resources

- [MITRE CVE Database](https://cve.mitre.org/)
- [NVD — National Vulnerability Database](https://nvd.nist.gov/)
- [CVSSv3 Calculator](https://www.first.org/cvss/calculator/3.1)
- [HackerOne — Disclosed Reports](https://hackerone.com/hacktivity)
- [Bugcrowd — Vulnerability Rating Taxonomy](https://bugcrowd.com/vulnerability-rating-taxonomy)
