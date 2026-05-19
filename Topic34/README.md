---
title: "Side Channel Attacks"
topic: "side-channel-attacks"
tags: [side-channel, timing-attack, power-analysis, cache-attack, hardware-security]
difficulty: advanced
day: 34
layout: default
parent: Topics
nav_order: 34
---

# Side Channel Attacks

## What You Will Learn
- What a side channel attack is and how it differs from direct attacks
- The main types of side channel attacks
- How timing attacks work in practice
- How to defend against side channel leakage

## What Is It?

A **side channel attack** does not attack the algorithm or logic of a system directly. Instead, it exploits **physical information leaked during execution** — things like how long an operation takes, how much power it consumes, or what electromagnetic signals it emits.

Even if the cryptographic algorithm is perfect, a bad implementation can leak the secret key through these physical side channels.

## Why It Matters

Side channel attacks have broken real-world hardware and software:
- Smart card keys extracted via power analysis
- AES keys leaked via cache timing on CPUs
- RSA keys recovered from electromagnetic emissions

These attacks are used in hardware hacking, embedded security research, and advanced CTF challenges.

## Key Concepts

### Types of Side Channels

| Type | What It Measures |
|------|-----------------|
| **Timing** | How long an operation takes |
| **Power Analysis** | How much power a chip consumes |
| **Electromagnetic (EM)** | EM emissions from a device |
| **Cache** | CPU cache access patterns |
| **Acoustic** | Sound emitted during computation |

### Timing Attack

A timing attack measures **how long code takes to run**. If a comparison function returns early when it finds a mismatch, an attacker can determine correct bytes one at a time by measuring response time.

Example of **vulnerable** string comparison:

```python
def check_password(input_pw, real_pw):
    for i in range(len(input_pw)):
        if input_pw[i] != real_pw[i]:
            return False  # returns early — leaks position of first mismatch
    return True
```

Example of **safe** constant-time comparison:

```python
import hmac
def check_password(input_pw, real_pw):
    return hmac.compare_digest(input_pw, real_pw)  # always takes same time
```

### Cache Timing Attack (Flush+Reload)

Modern CPUs cache memory accesses. An attacker sharing a CPU can measure whether a memory address is in cache (fast access) or not (slow access) to infer what data a victim process touched.

```
flush(target_address)       # evict from cache
wait for victim to run
t1 = time()
access(target_address)      # measure reload time
t2 = time()
if (t2 - t1) < threshold:
    # address was accessed by victim (it was in cache)
```

### Simple Power Analysis (SPA)

During cryptographic operations, different operations (multiply, square) consume different amounts of power. An attacker with a power probe can read RSA private key bits directly from the power trace.

### Differential Power Analysis (DPA)

DPA uses statistical analysis across many power traces to extract key material even with noise. It is far more powerful than SPA.

## Defenses

- Use **constant-time algorithms** for comparisons and crypto
- Add **random delays** to obscure timing
- Use **power noise generators** in hardware
- Apply **masking** — XOR intermediate values with random data
- Use hardware security modules (HSMs) with built-in countermeasures

## Resources

- [Paul Kocher — Timing Attacks on Implementations of DH, RSA, DSS](https://paulkocher.com/doc/TimingAttacks.pdf)
- [Cryptopals — Implement Timing Attacks](https://cryptopals.com/)
- [CHES Conference Papers](https://ches.iacr.org/)
- [TryHackMe — Hardware Hacking](https://tryhackme.com/room/hardwarehacking101)
- [Colin O'Flynn — Side Channel Analysis](https://www.youtube.com/@ColinOFlynn)
