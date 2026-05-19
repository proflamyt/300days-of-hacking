---
title: "Malware"
topic: "malware"
tags: [malware, viruses, trojans, ransomware, rootkits, evasion, fileless]
difficulty: intermediate
day: 6
layout: default
parent: Topics
nav_order: 6
---

# Malware

## What You Will Learn
- What malware is and the different forms it takes
- How viruses, worms, ransomware, Trojans, rootkits, and backdoors work
- How malware evades detection
- What fileless malware is and why it's so dangerous
- Defensive strategies against malware

## What Is It?

Malware is any software intentionally designed to cause damage to a computer, server, client, or computer network. A wide variety of types of malware exist, including computer viruses, worms, Trojan horses, ransomware, spyware, adware, rogue software, and scareware.

Malware is sometimes used broadly against government or corporate websites to gather protected information or to disrupt their operations. However, malware can also be used against individuals to gain information such as personal identification numbers, bank or credit card numbers, and passwords. In addition to criminal money-making, malware can be used for sabotage — often for political motives.

## Malware Types

The best-known types of malware — viruses and worms — are known for the manner in which they spread, rather than any specific type of behavior.

### Viruses

A computer virus is software usually hidden within another seemingly innocuous program that can produce copies of itself and insert them into other programs or files, and that usually performs a harmful action (such as destroying data). An example is a PE infection, a technique that inserts extra data or executable code into PE (Portable Executable) files.

### Worms

A worm is stand-alone malware that actively transmits itself over a network to infect other computers. Unlike a virus, a worm does not require the user to run an infected program — it spreads itself.

### Ransomware

Ransomware encrypts the victim's files and demands payment to restore access. Screen-locking ransomware (also called "lock-screens") blocks screens on Windows or Android devices with a false accusation, trying to scare victims into paying a fee.

### Trojan Horses

A Trojan horse is a harmful program that misrepresents itself to masquerade as a regular, benign program or utility in order to persuade a victim to install it. A Trojan usually carries a hidden destructive function that is activated when the application is started. Trojan horses are generally spread through social engineering — for example, a user is duped into executing an email attachment disguised as something safe.

Many modern Trojans act as a backdoor, contacting a controller who can then have unauthorized access to the affected computer. Unlike viruses and worms, Trojans generally do not attempt to inject themselves into other files or propagate themselves.

### Rootkits

Once malicious software is installed on a system, it is essential that it stays concealed to avoid detection. Software packages known as **rootkits** allow this concealment by modifying the host's operating system so that the malware is hidden from the user. Rootkits can prevent a malicious process from being visible in the system's list of processes, or keep its files from being read.

### Backdoors

A backdoor is a method of bypassing normal authentication procedures, usually over a network connection. Once a system has been compromised, one or more backdoors may be installed to allow future access — invisibly to the user. Backdoors may be installed by Trojans, worms, implants, or other methods.

## Evasion

Since 2015, a significant portion of malware has been using a combination of many techniques designed to avoid detection and analysis:

- **Environment fingerprinting**: The malware checks whether it's running in a sandbox or analysis environment before executing.
- **Signature bypassing**: Changing the server used by the malware or modifying the binary to avoid signature-based antivirus detection.
- **Timing-based evasion**: Malware runs at certain times or following certain user actions, executing during vulnerable periods such as the boot process while remaining dormant otherwise.
- **Obfuscation**: Obfuscating internal data so automated tools cannot detect the malware.
- **Steganography (Stegomalware)**: Hiding malicious code inside images or other media files.

## Fileless Malware (Advanced Volatile Threats)

Fileless malware does not require a file to operate. It runs within memory and uses existing system tools (like PowerShell or WMI) to carry out malicious acts. Because there are no files on disk, there are no executable files for antivirus and forensic tools to analyze, making this type of malware nearly impossible to detect. The only way to detect fileless malware is to catch it operating in real time.

## Anti-Malware Strategies

- **Antivirus software**: Detects known malware signatures.
- **Behavioral analysis**: Monitors for suspicious behavior regardless of file signature.
- **Application whitelisting**: Only allows known, trusted applications to run.
- **Network segmentation**: Limits lateral movement if a machine is compromised.
- **Air gap isolation**: Completely disconnects a computer from all other networks. However, malware can still cross an air gap via removable media.

## Resources

- [MITRE ATT&CK — Malware Techniques](https://attack.mitre.org/)
- [MalwareBazaar](https://bazaar.abuse.ch/) — Malware sample database
- [Any.run](https://any.run/) — Interactive online malware sandbox
- [VirusTotal](https://www.virustotal.com/) — Scan files and URLs for malware
