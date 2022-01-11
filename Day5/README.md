# PIVOTING
During Pentest , There is probability the machine you compromised is on a network i.e connected to diffrent machines.Pivoting is entending your tendrils to these other machines on the network, either to compromise or to access a service you cant access directly . A company may have private internal network that are inaccessible to any user from the internet. compromising a machine linked to these private computer can allow you to access these internal services.

### Ports

### Two Types 
  1. Tunnelling/Proxying
  2. Port Forwarding

### Enumeration
    arp -a (lists  ARP cache of the machine)<br>
    cat /etc/hosts (check loccally configured hosts to domain names )
    type C:\Windows\System32\drivers\etc\hosts (for windows) 
  #### check the DNS servers:
    nmcli dev show  (linux)
    ipconfig /all (windows)
   
   
 #### SSH TUNNELLING/PROXYING 
  ### TUNNELLING 
  
 #### Forward Port forwarding
      ssh -L <port to open on attacker>:< intrernal IP>:<internal port> <compromised machine ssh> -fN
      
 #### SOCAT
      
 
  
