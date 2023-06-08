# Network Security

## OSI MODEL

Also Known as Open System Model, This was developed as a way to help categorize  how computers communicate with one another

- Application Layer
- Presentation Layer
- Session Layer
- Transport Layer
- Network Layer  (router)     IP (also non-local)
- Data Link Layer (switch, wap)    mac address (local)
- Physical Layer  (modem, hub)


# DOD MODEL


- Process/Application layer
- Host-to-Host layer
- Internet layer
- Network Access layer



## Security Devices

- Firewall :
The purpose of a firewall is to manage the types of traffic that can enter and leave a protected network. First line of defence in protecting internal network from outside threat.

    - Stateless Inspection -> Examines every packets, doesn’t maintain an internal state from one packet to another.
    - Stateful Inspection  -> Only Examine the state of a connection , stores information about active network connections

- IDS :
Identify when a network breach or attack has occured

    - Signature Based
    - Anomaly Based
    - Policy Based

https://github.com/proflamyt/Protocol-Based-Intrusion-Detection

- VPN :
facilitates an encrypted connection to a private network over the internet. remote host will be seen as a private host.
    - site-to-site VPN
    - remote-access VPN
    - SSL VPN (uses webserver)
can operate in layer 2, 3, 7

        - VPN PROTOCOLS:

            - IPSec : Uses AH (authentication but not encryption) or ESP (authenticate and encrypt) , Only transmit one-to-one commmunication
            - GRE (Generic Routing Encapsulation) : one-to-many communication
            - Point-To-Point Tunneling Protocol : supports dial up
            - TLS : uses assymentric enc. (TLS 1.2 & 1.3 is considered save)
            - SSL : older ( TLS 1.0 and even SSL 3.0  unsafe)




## Optimization/Performance Devices

- Load Balancers :
Spread and distribute work load. example: nginx

- Proxy Server: 

Appliance that request resources on behalf of client machine

example: nginx



### DHCP
Dynamic Host COntrol Protocol, Assigns IP address to hosts on a network.

HOW DHCP WORKS:

- A new computer sends a dhcp discovery packet to 255.255.255.255 (broadcast) on UDP port 67.
- DHCP server which listens on that port , replies to the mac address of the requesting computer with an offer packet on UDP port 68.
- This new computer that receives the offer packet now knows the DHCP server, and sends a request packet only this time only to the DHCP server
- DHCP server replies with the acknowledgment packet which contains all necessary information, including the IP address for the new compuer 
- Once the new computer receives this info, it changes it's details to match the information.


### DNS

Matches Human readable names to IP addresses.

Types:

    - Root Server
    - TLD Servers
    - Authoritative
    - Non-Authoritative




https://www.vice.com/en/article/wnnmv9/undersea-cable-surveillance-is-easy-its-just-a-matter-of-money
https://www.cybertalk.org/2022/04/22/hawaii-undersea-cable-attack-a-credential-theft-story/