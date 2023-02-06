# Active Directory


## Domain Controller 

A Windows domain is a form of a computer network in which all user accounts, computers, printers and other security principals, are registered with a central database located on one or more clusters of central computers known as domain controllers.

### Powershell Cmd

  ```
  Get-ADComputer 
  ```
  > The Get-ADComputer cmdlet gets a computer or performs a search to retrieve multiple computers.
  ```
  Get-ADDomainController
  ```

  > We can use the Get-ADDomainController PowerShell cmdlet to get information about the domain controllers in Active Directory. 


### NTLM

NTLM Authentication Process

NTLM authentication typically follows the following step-by-step process:

1. The user shares their username, password and domain name with the client.
2. The client develops a scrambled version of the password — or hash — and deletes the full password.
3. The client passes a plain text version of the username to the relevant server.
4. The server replies to the client with a challenge, which is a 16-byte random number.
5. In response, the client sends the challenge encrypted by the hash of the user’s password.
6. The server then sends the challenge, response and username to the domain controller (DC).
7. The DC retrieves the user’s password from the database and uses it to encrypt the challenge.
8. The DC then compares the encrypted challenge and client response. If these two pieces match, then the user is authenticated and access is granted.

![NTLM](https://github.com/proflamyt/300days-of-hacking/blob/main/Topic14/pictures/c9113ad0ff443dd0973736552e85aa69.png)





Kerberos Authentication
Here is the twelve-step process for Kerberos authentication:

The user shares their username, password, and domain name with the client.
The client assembles a package — or an authenticator — which contains all relevant information about the client, including the user name, date and time. All information contained in the authenticator, aside from the user name, is encrypted with the user’s password.
The client sends the encrypted authenticator to the KDC.
The KDC checks the user name to establish the identity of the client. The KDC then checks the AD database for the user’s password. It then attempts to decrypt the authenticator with the password. If the KDC is able to decrypt the authenticator, the identity of the client is verified.
Once the identity of the client is verified, the KDC creates a ticket or session key, which is also encrypted and sent to the client.
The ticket or session key is stored in the client’s Kerberos tray; the ticket can be used to access the server for a set time period, which is typically 8 hours.
If the client needs to access another server, it sends the original ticket to the KDC along with a request to access the new resource.
The KDC decrypts the ticket with its key. (The client does not need to authenticate the user because the KDC can use the ticket to verify that the user’s identity has been confirmed previously).
The KDC generates an updated ticket or session key for the client to access the new shared resource. This ticket is also encrypted by the server’s key. The KDC then sends this ticket to the client.
The client saves this new session key in its Kerberos tray, and sends a copy to the server.
The server uses its own password to decrypt the ticket.
If the server successfully decrypts the session key, then the ticket is legitimate. The server will then open the ticket and review the access control list (ACL) to determine if the client has the necessary permission to access the resource.




reference : https://www.crowdstrike.com/cybersecurity-101/ntlm-windows-new-technology-lan-manager/
