## Cookie Based XSS 

Description :

Process stores the workspace parameter as a cookie value 

As we can see here, the javascript attempts to read a cookie called 'pm_sys_sys' and covert it to string , The XSS vulnerability arises due to this code snippet attempting to assign a JSON object to the 'obj' variable through the use of the eval function. The unsafe usage of eval in this 
snippet allows an attacker who controls cookie "pm_sys_sys" to execute a arbitrary javascript code.

![image](https://github.com/proflamyt/300days-of-hacking/assets/53262578/309ee307-bccf-4586-8dcf-1fe007220c09)


### Crafting an exploit 
The eval fuction in javascript will execute the string  argument it receives as a javascript body, by crafting a json with a field as the javascript function an attacker can execute arbitrary javascript on the vulnerable web application.
To make attack more stealthy the attacker can make the payload behave as the intended behaviour of the code snippets wants that is allow the "sys_sys" argument accessible as argument to 'obj'.

final payload : 
By setting the cookie "pm_sys_sys" to 

```json
{"sys_sys": "workflow", "ola": alert(1)}
```

an attacker can execute arbitrary js code, while setting the workspace field to the intended workspace.



### Possible Exploit Execution

An attacker finds an XSS or CRLF vulnerability on a domain example.com , he uses the vulnerability to set the cookie "pm_sys_sys" as {"sys_sys": "workflow", "ola": alert(1)} 
with domain 

document.cookie="pm_sys_sys={"sys_sys": "workflow", "ola": alert(1)};domain=example.com;path=/;expires=2070-01-01"

Ones thesame user visits the vulnrable page "sys/en/*/login/login" , the xss triggers 

Note: The exeploit could be a key logger as this is the login page
