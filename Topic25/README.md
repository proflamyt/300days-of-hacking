# EDR EVASION

EDR, or endpoint detection and response, is a security technology that is designed to detect and respond to malicious activity on a network. EDR systems typically use a combination of techniques, such as network monitoring, behavioral analysis, and machine learning, to identify and stop threats. In this tutorial, we will discuss some techniques that attackers may use to evade EDR systems and how to defend against them.

One common method of evading EDR is to use encrypted traffic to hide the malicious payload. Encrypting the payload makes it difficult for EDR systems to inspect and analyze the content of the traffic, allowing the attacker to sneak past the EDR's defenses. To defend against this tactic, organizations can use network traffic analysis to identify and block encrypted traffic from known malicious sources.

Another tactic that attackers may use to evade EDR is to use legitimate, signed applications to deliver the payload. In this case, the attacker will use a legitimate application, such as a trusted file transfer tool, to deliver the malicious payload. This tactic can be effective because EDR systems are typically configured to allow signed applications to run without interference. To defend against this tactic, organizations can implement application whitelisting, which only allows known, trusted applications to run on the network.

Attackers may also try to evade EDR by using evasion techniques, such as changing the file name or modifying the file header, to make the payload appear legitimate. In this case, the attacker is trying to trick the EDR system into thinking that the payload is a benign file, rather than a malicious one. To defend against this tactic, organizations can use machine learning algorithms to analyze the behavior of the payload and identify any suspicious activity.

In summary, EDR evasion is a common tactic used by attackers to bypass security systems and deliver malicious payloads. To defend against this tactic, organizations can use a combination of network traffic analysis, application whitelisting, and machine learning to identify and block encrypted traffic, signed applications, and evasion techniques.




### There are several possible ways that an attacker could attempt to evade EDR on a Windows system. Some of these tactics include:

1. Using encrypted traffic: As mentioned earlier, attackers can use encryption to hide the malicious payload from EDR systems. This can be effective because EDR systems are typically not able to inspect encrypted traffic.

2. Using signed applications: Attackers may also try to use legitimate, signed applications to deliver the payload. In this case, the attacker will use a trusted application, such as a file transfer tool, to deliver the payload.

3. Using evasion techniques: Attackers may also try to evade EDR by using techniques such as changing the file name or modifying the file header to make the payload appear legitimate.

4. Using scripting languages: Attackers may use scripting languages, such as PowerShell, to execute the payload. This can be effective because scripting languages are often used for legitimate purposes and may not be flagged by EDR systems.

To defend against these tactics, organizations can use a combination of network traffic analysis, application whitelisting, and machine learning to identify and block encrypted traffic, signed applications, evasion techniques, and scripting languages. Additionally, organizations can implement network segmentation and access controls to limit the ability of attackers to move laterally within the network.



