---
title: "Pivoting"
topic: "pivoting"
tags: [pivoting, port-forwarding, tunneling, ssh, socat, lateral-movement]
difficulty: intermediate
day: 5
layout: default
parent: Topics
nav_order: 5
---

# Pivoting

## What You Will Learn
- What pivoting is and why it's needed during penetration tests
- The difference between port forwarding and tunneling/proxying
- How to enumerate a network from a compromised machine
- How to use SSH and Socat for port forwarding
- How to transfer files to and from a compromised host

During a penetration test, there is a probability that the machine you compromised is on a network — connected to different machines. **Pivoting** is extending your reach to these other machines on the network, either to compromise them or to access services you cannot reach directly. A company may have a private internal network that is inaccessible to anyone from the internet. Compromising a machine linked to these private computers can allow you to access those internal services.

## Ports

<https://cybernews.com/what-is-vpn/port-forwarding/>

## Port Forwarding

Port forwarding is a technique used to allow external devices to access computer services on private networks. It redirects traffic coming into or leaving a port.

## Two Types

1. Tunneling/Proxying
2. Port Forwarding

## Enumeration

```bash
arp -a                                          # list ARP cache of the machine
cat /etc/hosts                                  # check locally configured host-to-domain-name mappings
type C:\Windows\System32\drivers\etc\hosts      # for Windows
```

#### Check the DNS Servers

```bash
nmcli dev show      # Linux
ipconfig /all       # Windows
```


## SSH Tunneling/Proxying

### Forward Port Forwarding

```bash
ssh -L <port to open on attacker>:<internal IP>:<internal port> <compromised machine ssh> -fN
```

This opens a port on your attacking machine that forwards all traffic to the internal IP and port through the compromised machine.

### Dynamic Port Forwarding (SOCKS Proxy)

```bash
ssh -D 1080 user@<compromised machine> -fN
```

This creates a SOCKS proxy on port 1080. You can then route tools through it using `proxychains`.

```bash
# Configure proxychains
echo "socks5 127.0.0.1 1080" >> /etc/proxychains.conf
proxychains nmap -sT <internal_IP>
```

## File Transfer

```bash
# Copy a directory recursively
scp -r user@remote_host:/path/to/remote/directory /path/to/local/destination

# Copy a single file
scp user@remote_host:/path/to/remote/file /path/to/local/destination
```

## SOCAT

The quick and easy way to set up a port forward with Socat is to open a listening port on the compromised server and redirect whatever comes into it to the target server.

```bash
# Forward traffic from port 8080 on the compromised host to an internal target
socat TCP-LISTEN:8080,fork TCP:<internal_IP>:<internal_port>
```

## Resources

- [Port Forwarding Explained](https://cybernews.com/what-is-vpn/port-forwarding/)
- [TryHackMe — Lateral Movement and Pivoting](https://tryhackme.com/room/lateralmovementandpivoting)
- [Chisel — Fast TCP Tunnel](https://github.com/jpillora/chisel)
- [PayloadsAllTheThings — Network Pivoting](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Network%20Pivoting%20Techniques.md)
