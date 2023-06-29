# User Account Control 



## Windows Integrity Level
- Low : interaction with the Internet
- Medium : Standard Users
- High : Admin 
- System : System priviledges

most of the bypass techniques rely on us being able to leverage a High IL process to execute something on our behalf. Since any process created by a High IL parent process will inherit the same integrity level, this will be enough to get an elevated token without requiring us to go through the UAC prompt.


Bypass

- Leveraging a High IL process to execute something on our behalf







https://tryhackme.com/room/bypassinguac
