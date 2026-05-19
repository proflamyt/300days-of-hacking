---
title: "Desktop Application Security"
topic: "desktop-application-security"
tags: [desktop, electron, java, dotnet, thick-client, binary-analysis, decompilation]
difficulty: intermediate
day: 80
layout: default
parent: Topics
nav_order: 80
---

# Desktop Application Security

## What You Will Learn
- What desktop application security testing involves
- How to test Electron, Java, and .NET applications
- Common desktop app vulnerabilities
- How to intercept and analyze desktop app network traffic

## What Is It?

**Desktop application security** testing (also called thick-client testing) covers security assessments of installed applications — as opposed to web or mobile apps. These include Electron apps (built with Node.js/JavaScript), Java apps, .NET apps, and native compiled applications.

Desktop apps often contain vulnerabilities that are harder to find because they are not as widely tested as web applications.

## Why It Matters

- Desktop apps often store credentials and sensitive data locally
- Electron apps run JavaScript with Node.js access — any XSS becomes RCE
- Java and .NET apps can be decompiled to readable source code
- Desktop apps communicate over the network — their traffic can be intercepted

## Electron Applications

Electron apps are essentially a Chromium browser bundled with a Node.js runtime. If an attacker can inject JavaScript into the app's renderer process, they get Node.js code execution (RCE).

### Checking Electron Security Settings

```bash
# Unpack the Electron app
npx @electron/asar extract app.asar ./extracted/

# Check security settings in main process
grep -r "nodeIntegration" ./extracted/
grep -r "contextIsolation" ./extracted/
grep -r "webSecurity" ./extracted/
```

Dangerous settings:

```js
// DANGEROUS — allows JavaScript to access Node.js APIs
mainWindow = new BrowserWindow({
    webPreferences: {
        nodeIntegration: true,       // should be false
        contextIsolation: false,     // should be true
    }
});
```

### Electron XSS → RCE

If `nodeIntegration: true` and you find XSS, this becomes RCE:

```js
// Execute shell command from XSS payload
require('child_process').exec('calc.exe');
```

## Java Applications

Java apps can be decompiled to near-original source code.

```bash
# Decompile a JAR file with jadx
jadx -d output_dir app.jar

# Or use JD-GUI
jd-gui app.jar

# Decompile .class files
javap -c MyClass.class
```

Common findings:
- Hardcoded credentials in source code
- Insecure deserialization (ysoserial payloads)
- SQL injection in JDBC queries
- Weak cryptography

### Java Deserialization

```bash
# Check if the app accepts serialized Java objects
# Look for Content-Type: application/x-java-serialized-object

# Generate deserialization payloads
ysoserial CommonsCollections4 "calc.exe" > payload.bin
```

## .NET Applications

.NET apps can be decompiled with ILSpy or dnSpy.

```bash
# Decompile .NET assembly with ilspy (CLI)
ilspy MyApp.exe -o ./decompiled/

# Or use dnSpy (GUI)
dnspy MyApp.exe
```

Common findings:
- Hardcoded keys and connection strings
- Insecure deserialization (BinaryFormatter, JSON.NET TypeNameHandling)
- SQL injection in LINQ or raw queries

## Intercepting Desktop App Traffic

Desktop apps often trust the system certificate store. Install Burp's CA certificate as a system-trusted certificate.

```bash
# Windows: Import Burp CA into certificate store
certmgr.msc → Trusted Root Certification Authorities → Import burp_ca.der

# macOS
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain burp_ca.der

# Redirect traffic through Burp proxy
# Set system proxy to 127.0.0.1:8080
```

For apps that ignore system proxy settings, use ProxyCap or `proxychains`.

## Local Storage and Registry

```bash
# Check local storage (Electron apps store in AppData)
%APPDATA%\AppName\Local Storage\

# Windows Registry for stored credentials
reg query "HKCU\Software\AppName"

# SQLite databases
sqlite3 storage.db ".tables"
sqlite3 storage.db "SELECT * FROM credentials;"
```

## Resources

- [HackTricks — Thick Client Pentesting](https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/electron-desktop-apps)
- [Doyensec — Electron Security Research](https://www.doyensec.com/resources/us-17-Carettoni-Electronegativity-A-Study-Of-Electron-Security.pdf)
- [PortSwigger — Deserialization](https://portswigger.net/web-security/deserialization)
- [TryHackMe — Thick Client Applications](https://tryhackme.com/room/thickclientpentesting)
- [jadx — Java Decompiler](https://github.com/skylot/jadx)
