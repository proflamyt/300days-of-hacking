---
title: "Shodan Dorking"
topic: "shodan-dorking"
tags: [shodan, osint, recon, internet-of-things, search-engine, favicon-hash, bug-bounty]
difficulty: intermediate
day: 51
layout: default
parent: Topics
nav_order: 51
---

# Shodan Dorking

## What You Will Learn
- What Shodan is and how it differs from regular search engines
- How to write Shodan search queries (dorks)
- How to find exposed services, expired certificates, and specific software
- How to compute and use favicon hashes

## What Is It?

**Shodan** is a search engine for internet-connected devices. Unlike Google, which indexes web page content, Shodan indexes **banner information** from services — open ports, server software, SSL certificates, and device metadata.

Shodan is an essential OSINT tool for recon in bug bounty and penetration testing.

## Why It Matters

Shodan can find:
- Exposed databases (MongoDB, Elasticsearch, Redis) with no authentication
- Industrial control systems (SCADA, PLCs) accessible from the internet
- Jenkins, Grafana, and admin panels with default credentials
- Assets belonging to a target organization that are not in scope yet

## Shodan Filters

### Favicon Hash

Every website with a favicon (the small icon in the browser tab) can be found using a hash of that favicon. This is powerful for finding all servers running the same software or belonging to the same company.

```python
import mmh3
import requests
import codecs

response = requests.get('https://cybersecurity.wtf/favicon.ico')
favicon = codecs.encode(response.content, "base64")
hash = mmh3.hash(favicon)
print(hash)
```

Then search Shodan:

```
http.favicon.hash:<hash>
```

### ASN

Search by Autonomous System Number:

```
asn:AS12345
```

### CIDR Range

Search for all IPs in a subnet:

```
net:192.168.1.0/24
```

### Organization

```
org:microsoft
org:"target company name"
```

### Expired Certificates

Find hosts with expired SSL certificates:

```
ssl.cert.expired:true
```

### Certificate Common Name (CN)

Find certificates for a specific domain — useful for finding subdomains:

```
ssl.cert.subject.cn:example.com
```

### WordPress Config Exposure

```
http.html:"* The wp-config.php creation script uses this file"
```

### Jenkins

Find exposed Jenkins dashboards:

```
"X-Jenkins" "Set-Cookie: JSESSIONID" http.title:"Dashboard"
x-jenkins 200
```

### Port Search

```
port:27017     # MongoDB
port:6379      # Redis
port:9200      # Elasticsearch
port:5900      # VNC
port:3389      # RDP
```

### Combining Filters

```
org:target http.title:"admin" port:8080
ssl.cert.subject.cn:*.example.com port:443
```

## Shodan CLI

```bash
# Install
pip install shodan

# Initialize
shodan init <API_KEY>

# Search
shodan search org:microsoft port:3389

# Download results
shodan download results.json.gz org:microsoft

# Convert to CSV
shodan convert results.json.gz csv
```

## Practical Bug Bounty Workflow

```bash
# 1. Find all IPs for the target organization
shodan search "org:targetname" --fields ip_str,port

# 2. Find subdomains via certificate transparency
shodan search "ssl.cert.subject.cn:*.targetname.com" --fields ssl.cert.subject.cn

# 3. Find exposed admin panels
shodan search 'http.title:"admin panel" org:targetname'

# 4. Find expired certs (potential subdomain takeover)
shodan search 'ssl.cert.expired:true org:targetname'
```

## Resources

- [Shodan — Official Search Engine](https://www.shodan.io/)
- [Shodan Dork List](https://github.com/blaCCkHatHacEEkr/PENTESTING-BIBLE/blob/master/Shodan%20Dorks.md)
- [Shodan CLI Documentation](https://cli.shodan.io/)
- [TryHackMe — Shodan.io](https://tryhackme.com/room/shodan)
- [OSINT Framework — Shodan](https://osintframework.com/)
