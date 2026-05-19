---
title: "DevSecOps"
topic: "devsecops"
tags: [devsecops, devops, security, ci-cd, sast, dast, containers, sca]
difficulty: intermediate
day: 38
layout: default
parent: Topics
nav_order: 38
---

# DevSecOps

## What You Will Learn
- What DevSecOps is and how it differs from traditional security
- Where security fits into the CI/CD pipeline
- The main security tools used in DevSecOps
- How to shift security left in software development

## What Is It?

**DevSecOps** stands for Development, Security, and Operations. It is the practice of incorporating security into every stage of the software development lifecycle (SDLC) — not just at the end before release.

Traditional security checked software after it was built. DevSecOps moves security earlier ("shift left") so that vulnerabilities are found and fixed cheaply, before they reach production.

## Why It Matters

- A bug found in development costs $80 to fix
- The same bug found in production can cost $7,500+
- DevSecOps makes security automatic, fast, and repeatable
- Modern organizations ship hundreds of times per day — manual security review does not scale

## Key Concepts

### The CI/CD Pipeline

```
Code → Commit → Build → Test → Deploy → Monitor
         ↑          ↑       ↑      ↑         ↑
       SAST        SCA    DAST  Container   Runtime
```

### SAST (Static Application Security Testing)

SAST scans source code **without running it**. It finds vulnerabilities like SQL injection, XSS, and insecure functions early.

```bash
# Semgrep — fast static analysis
semgrep --config "p/owasp-top-ten" ./src/

# Bandit — Python security linter
bandit -r ./myapp/

# Checkov — Infrastructure as Code scanning
checkov -d ./terraform/
```

### SCA (Software Composition Analysis)

SCA checks your **third-party dependencies** for known CVEs.

```bash
# npm audit — check Node.js packages
npm audit

# Safety — check Python packages
safety check

# Trivy — scan container images and filesystem
trivy image myapp:latest
trivy fs ./
```

### DAST (Dynamic Application Security Testing)

DAST tests a **running application** from the outside, like an attacker would.

```bash
# OWASP ZAP — automated web scanner
zap-cli quick-scan --self-contained https://staging.example.com

# Nikto — web server scanner
nikto -h https://staging.example.com
```

### Secrets Scanning

Catch hardcoded API keys and passwords before they reach source control.

```bash
# TruffleHog — scan git history for secrets
trufflehog git https://github.com/org/repo

# GitLeaks — fast secrets scanner
gitleaks detect --source .
```

### Container Security

```bash
# Scan a Docker image for vulnerabilities
trivy image python:3.11

# Check Dockerfile for issues
hadolint Dockerfile

# Run container with minimal privileges
docker run --read-only --user 1000 --no-new-privileges myapp
```

### Example GitHub Actions Pipeline

```yaml
name: Security Scan
on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Semgrep
        uses: semgrep/semgrep-action@v1
        with:
          config: p/owasp-top-ten
          
      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          
      - name: Check for secrets
        uses: gitleaks/gitleaks-action@v2
```

## Resources

- [OWASP DevSecOps Guideline](https://owasp.org/www-project-devsecops-guideline/)
- [Semgrep — Static Analysis](https://semgrep.dev/)
- [Trivy — Container Security Scanner](https://trivy.dev/)
- [TryHackMe — DevSecOps Room](https://tryhackme.com/room/introductiontodevsecops)
- [SANS — DevSecOps Foundations](https://www.sans.org/cyber-security-courses/security-for-devsecops/)
