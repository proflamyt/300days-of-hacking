---
title: "Web Attack Techniques"
topic: "web-attacks"
tags: [web-security, secrets, reconnaissance, bigquery, curl, fuzzing, bug-bounty]
difficulty: intermediate
day: 64
layout: default
parent: Topics
nav_order: 64
---

# Web Attack Techniques

## What You Will Learn
- How to find hardcoded secrets in source code and repositories
- How to use BigQuery and GitHub for secret scanning
- How to enumerate web endpoints with curl
- URL parsing and path manipulation techniques

## What Is It?

Web attacks cover a broad range of techniques used against web applications. This topic focuses on reconnaissance and discovery — finding secrets in source code, mapping attack surfaces, and building effective automation for web testing.

## Why It Matters

Most real bugs in bug bounty programs start with thorough reconnaissance. Leaked API keys, exposed endpoints, and misconfigured paths are often found through smart scanning, not brute force.

## Secret Scanning

### Regex Pattern for Common Secrets

This pattern matches common secret and API key variable names in source code:

```bash
(access_key|access_token|admin_pass|admin_user|algolia_admin_key|algolia_api_key|
alias_pass|alicloud_access_key|amazon_secret_access_key|amazonaws|ansible_vault_password|
api_key|api_key_secret|api_secret|appkey|appkeysecret|application_key|appsecret|
auth_token|authorizationToken|aws_access_key_id|aws_secret|aws_secret_key|
aws_token|AWSSecretKey|client_secret|cloudflare_api_key|cloudflare_auth_key|
database_password|db_password|docker_pass|encryption_key|heroku_api_key|
sonatype_password|awssecretkey)
```

### BigQuery — Search GitHub for Secrets

GitHub publishes a public dataset to BigQuery. Use it to search for hardcoded secrets in public repos:

```sql
SELECT path
FROM `bigquery-public-data.github_repos.contents` AS contents
JOIN `bigquery-public-data.github_repos.files` AS files
  ON files.id = contents.id
WHERE REGEXP_CONTAINS(content, r"PATTERN_HERE")
```

Replace `PATTERN_HERE` with the secret pattern you are looking for.

## URL and Path Analysis

### Extract Unique Paths from a URL List

```bash
# Extract repo owner/name from GitHub URLs, remove query strings, deduplicate
cut -d '/' -f 4,5 < urls.txt | sed 's/?.*//g' | sort -u
```

### Parse URL Paths with unfurl

```bash
# Print each path component on its own line
unfurl paths < urls.txt | tr '/' '\n' | sort -u

# Alternative with sed
sed 's#/#\n#g' paths.txt | sort -u
```

## Web Endpoint Fuzzing with curl

### Sequential URL Fuzzing

```bash
# Fetch URLs numbered 0 to 10, save each response to out/post_X.txt
curl --silent --fail "https://example.com/[0-10]" -o "out/post_#1.txt"

# Print URL and status code for each
curl -s -w '%{url} %{http_code}\n' https://example.com/[0-10] -o /dev/null

# Filter for successful responses
curl -s -w '%{url} %{http_code}\n' https://example.com/[0-10] -o /dev/null | grep 200

# Filter out 404s
curl -s -w '%{url} %{http_code}\n' https://example.com/[0-10] -o /dev/null | grep -v 404
```

### Directory Fuzzing

```bash
# ffuf — fast web fuzzer
ffuf -w /usr/share/wordlists/dirb/common.txt -u https://target.com/FUZZ

# With extension filtering
ffuf -w wordlist.txt -u https://target.com/FUZZ -e .php,.html,.txt

# Parameter fuzzing
ffuf -w params.txt -u "https://target.com/search?FUZZ=test"
```

## JavaScript Endpoint Discovery

Modern web apps expose endpoints through JavaScript files. Parse them to find hidden APIs:

```bash
# Download all JS files
gau target.com | grep "\.js$" | sort -u | xargs -I{} curl -s {} > all.js

# Extract endpoints from JS
grep -oP '(/api/[a-zA-Z0-9/_-]+)' all.js | sort -u

# Use jsluice
jsluice urls -r < all.js
```

## Resources

- [TruffleHog — Secret Scanning](https://github.com/trufflesecurity/trufflehog)
- [ffuf — Web Fuzzer](https://github.com/ffuf/ffuf)
- [BigQuery Public GitHub Dataset](https://cloud.google.com/bigquery/public-data)
- [HackTricks — Web Reconnaissance](https://book.hacktricks.xyz/network-services-pentesting/pentesting-web)
- [Reconmap — Reconnaissance Tool](https://reconmap.org/)
