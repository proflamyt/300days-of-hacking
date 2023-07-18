# PIVOTING
During Pentest , There is probability the machine you compromised is on a network i.e connected to diffrent machines.Pivoting is entending your tendrils to these other machines on the network, either to compromise or to access a service you cant access directly . A company may have private internal network that are inaccessible to any user from the internet. compromising a machine linked to these private computer can allow you to access these internal services.

### Ports
<https://cybernews.com/what-is-vpn/port-forwarding/>

### Port Forwarding
Port forwarding is a technique that is used to allow external devices access to computers services on private networks. redirect what comes into or leaves the port 

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
 The quick and easy way to set up a port forward with socat is quite simply to open up a listening port on the compromised server, and redirect whatever comes into it to the target server.
      
 
  
