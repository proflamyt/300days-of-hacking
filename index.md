---
title: Home
layout: home
nav_order: 1
description: "A practical hacking knowledge base covering 90+ security topics"
---

# 300 Days of Hacking

This program is aimed at teaching young and aspiring hackers the skills they need to stand out in the pentesting community. Beginners are welcomed to fork and contribute to the community.

Use the search bar at the top (or press <kbd>K</kbd>) to jump to any topic. You can also filter the list below as you type.

## Topics and Vulnerabilities

<input
  type="text"
  id="topic-filter"
  placeholder="Filter topics… (e.g. android, kernel, crypto)"
  aria-label="Filter topics"
  style="width:100%;padding:10px 14px;margin:14px 0;font-size:1rem;border:1px solid #ccc;border-radius:6px;box-sizing:border-box;" />

<div id="topic-list" markdown="1">

- [Git and GitHub](Day1/README.md)
- [Shells](Day2/README.md)
- [Understanding HTTP](Day3/README.md)
- [Linux Privilege Escalation](Day4/README.md)
- [Pivoting](Day5/README.md)
- [Malware](Day6/README.md)
- [OSINT](Day7/README.md)
- [Linux Internals](Day8/README.md)
- [Windows Internals](Day9/README.md)
- [Encryption](Day10/README.md)
- [Tracking Mobile Phone From Personal Laptop](Day11/README.md)
- [Android Internals](Day12/README.md)
- [Networking](Day13/README.md)
- [Active Directory](Topic14/README.md)
- [Firewall Evasion](Topic15/README.md)
- [Blockchain](Topic16/README.md)
- [Smart Contracts](Topic17/README.md)
- [Wireless](Topic18/README.md)
- [ARP](Topic19/README.md)
- [Process Injection](Topic20/README.md)
- [VPN](Topic21/README.md)
- [CORS](Topic22/README.md)
- [Android Debug Shell](Topic23/README.md)
- [Containerization](Topic24/README.md)
- [EDR Evasion](Topic25/README.md)
- [Assembly Language](Topic26/README.md)
- [PowerShell](Topic27/README.md)
- [Windows and Networking](Topic28/README.md)
- [Reverse Engineering](Topic29/README.md)
- [Android Hacking](Topic30/README.md)
- [CTF (Capture The Flag)](Topic31/README.md)
- [Same-Origin Policy and CORS](Topic32/README.md)
- [Security Research](Topic33/README.md)
- [Side Channel Attacks](Topic34/README.md)
- [RTOS (Real-Time Operating System)](Topic35/README.md)
- [Threads and Processes](Topic36/README.md)
- [WebSockets, SSE, Long Polling](Topic37/README.md)
- [DevSecOps](Topic38/README.md)
- [Cryptography](Topic39/README.md)
- [AWS Cloud Pentesting](Topic40/README.md)
- [Malware Development](Topic41/README.md)
- [Exploit Development](Topic42/README.md)
- [Network Security](Topic43/README.md)
- [UAC Bypass](Topic44/README.md)
- [Windows Privilege Escalation](Topic45/README.md)
- [Prototype Pollution](Topic46/README.md)
- [Windows Authentication](Topic47/README.md)
- [OAuth 2.0](Topic48/README.md)
- [GraphQL](Topic49/README.md)
- [Arduino Rubber Ducky / BadUSB](Topic50/README.md)
- [Shodan Dorking](Topic51/README.md)
- [Microservices Security](Topic52/README.md)
- [HTTP Request Smuggling](Topic53/README.md)
- [Web Server in Assembly](Topic54/README.md)
- [GDB](Topic55/README.md)
- [Kubernetes](Topic56/README.md)
- [CVE Analysis](Topic57/README.md)
- [XSS in React](Topic58/README.md)
- [Red Teaming (Windows)](Topic59/README.md)
- [Azure Cloud Pentesting](Topic62/README.md)
- [Google Cloud Pentesting](Topic63/README.md)
- [Web Attacks](Topic64/README.md)
- [Nginx Misconfigurations](Topic65/README.md)
- [Certificates and PKI](Topic67/README.md)
- [NoSQL Injection](Topic68/README.md)
- [Frontend Vulnerabilities](Topic69/README.md)
- [DNS Spoofing](Topic70/README.md)
- [ROP (Return-Oriented Programming)](Topic71/README.md)
- [Heap Exploitation](Topic72/README.md)
- [Embedded Systems](Topic73/README.md)
- [Memory Paging and Virtual Memory](Topic74/README.md)
- [WinDbg](Topic76/README.md)
- [Linux Kernel Exploitation](Topic77/README.md)
- [Windows Injection and Hijacking](Topic78/README.md)
- [ARM64 Assembly](Topic79/README.md)
- [Desktop Application Security](Topic80/README.md)
- [macOS IPC — Mach IPC](Topic81/README.md)
- [LLDB](Topic82/README.md)
- [Rust](Topic83/README.md)
- [Bluetooth Security](Topic84/README.md)
- [Fault Injection](Topic85/README.md)
- [SageMath for Cryptography](Topic86/README.md)
- [Miscellaneous Security Concepts](Topic87/README.md)
- [Hardware Hacking](Topic88/README.md)
- [VHDL for Hardware Security](Topic89/README.md)
- [Firmware and UEFI Security](Topic90/README.md)
- [Format String Vulnerabilities](Topic91/README.md)
- [UEFI Internals and Debugging](Topic92/README.md)
- [AI Red Teaming](Topic93/README.md)

</div>

<p id="topic-count" style="margin-top:8px;color:#666;font-size:0.9rem;"></p>

<script>
(function () {
  var input = document.getElementById('topic-filter');
  var list  = document.getElementById('topic-list');
  var count = document.getElementById('topic-count');
  if (!input || !list) return;

  var items = list.querySelectorAll('li');
  var total = items.length;

  function update() {
    var q = input.value.trim().toLowerCase();
    var shown = 0;
    items.forEach(function (li) {
      var match = !q || li.textContent.toLowerCase().indexOf(q) !== -1;
      li.style.display = match ? '' : 'none';
      if (match) shown++;
    });
    count.textContent = q
      ? 'Showing ' + shown + ' of ' + total + ' topics'
      : total + ' topics';
  }

  input.addEventListener('input', update);
  update();
})();
</script>
