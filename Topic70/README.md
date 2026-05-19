---
title: "DNS Spoofing"
topic: "dns-spoofing"
tags: [dns, spoofing, dnsmasq, mitm, poisoning, network-security]
difficulty: intermediate
day: 70
layout: default
parent: Topics
nav_order: 70
---

# DNS Spoofing

## What You Will Learn
- What DNS spoofing is and how it differs from DNS cache poisoning
- How to set up a local DNS server with dnsmasq for testing
- How DNS spoofing is used in man-in-the-middle attacks
- How to defend against DNS spoofing

## What Is It?

**DNS spoofing** (also called DNS poisoning) is an attack where a malicious DNS server returns a fake IP address for a domain. When a victim queries `google.com`, the attacker's DNS server returns the attacker's IP instead of Google's real IP. The victim's traffic is redirected to the attacker's server.

This is a critical component of **man-in-the-middle (MITM)** attacks.

## Why It Matters

DNS spoofing can:
- Redirect users to phishing pages that look identical to legitimate sites
- Intercept credentials and session cookies
- Serve malware disguised as legitimate software downloads
- Redirect payment pages to attacker-controlled servers

## How DNS Spoofing Works

1. Attacker positions themselves on the network (e.g., same Wi-Fi) or controls the DNS server
2. Victim's device queries DNS for `bank.com`
3. Attacker responds with `attacker-IP` instead of the real IP
4. Victim's browser connects to the attacker's server
5. Attacker presents a fake login page and captures credentials

## Setting Up dnsmasq for Testing

**dnsmasq** is a lightweight DNS server commonly used for local testing and MITM labs.

Create or edit your local `dnsmasq.conf`:

```bash
# Format: address=/domain/IP

# Redirect ALL domains to your IP (wildcard)
address=/#/192.168.200.147

# Redirect a specific domain to localhost (block it)
address=/google.com/127.0.0.1

# Enable query logging
log-queries
```

### Running dnsmasq with Docker

```bash
# Pull the image
docker pull andyshinn/dnsmasq

# Run with your config file and expose UDP port 53
docker run --name my-dnsmasq --rm -it \
  -p 0.0.0.0:53:53/udp \
  -v /path/to/dnsmasq.conf:/etc/dnsmasq.conf \
  andyshinn/dnsmasq
```

Now point your test device's DNS server to the Docker host's IP. All DNS queries will be intercepted.

### Redirecting a Victim's DNS

In a local network attack:

```bash
# Using ARP spoofing to become the gateway
arpspoof -i eth0 -t <victim-IP> <gateway-IP>

# Then run a DNS spoofing tool
dnschef --fakeip 192.168.1.100 --interface eth0
```

## Real Attack Chain Example

1. Connect to same Wi-Fi as victim
2. ARP spoof to intercept victim's traffic
3. Run dnsmasq or dnschef to respond to all DNS queries with your IP
4. Run a fake web server (nginx/Apache) at your IP with a cloned login page
5. Victim visits `paypal.com` → your fake page → enters credentials → you capture them

## Detection

DNS spoofing can be detected by:
- Comparing DNS responses from multiple resolvers
- Using DNSSEC (DNS Security Extensions) — responses are cryptographically signed
- Monitoring for unexpected changes in DNS records
- Using encrypted DNS (DNS-over-HTTPS or DNS-over-TLS)

## Defenses

- **DNSSEC**: Verifies DNS responses with cryptographic signatures
- **DNS-over-HTTPS (DoH)**: Encrypts DNS queries so an attacker cannot intercept and modify them
- **HSTS**: Forces HTTPS — the browser rejects invalid certificates even if redirected
- **Certificate Pinning**: Mobile apps reject unexpected certificates even with valid CA signatures
- Use a trusted, well-secured DNS resolver (Cloudflare `1.1.1.1`, Google `8.8.8.8`)

## Resources

- [Cloudflare — DNS Cache Poisoning](https://www.cloudflare.com/learning/dns/dns-cache-poisoning/)
- [dnsmasq — Documentation](http://www.thekelleys.org.uk/dnsmasq/doc.html)
- [dnschef — DNS Chef Tool](https://github.com/iphelix/dnschef)
- [TryHackMe — Network Security](https://tryhackme.com/room/networksec)
- [DNSSEC Overview](https://www.icann.org/resources/pages/dnssec-what-is-it-why-important-2019-03-05-en)
