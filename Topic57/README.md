## CVE-2024-25506

### ProcessMaker - Cookie Based XSS 

Description :

ProcessMaker  was discovered to have an XSS vulnerability due to vulnerable implementation of how the workspace parameter is stored as a cookie value 


The vulnerability occurs when the JavaScript tries to access a cookie named 'pm_sys_sys' and convert its contents to an object using the eval function.

As seen in the provided code snippet,they attempt to assign a JSON object to the 'obj' variable using the eval function. The insecure use of eval in this snippet enables a potential attacker, who has control over the "pm_sys_sys" cookie, to execute arbitrary JavaScript code.


![image](https://github.com/proflamyt/300days-of-hacking/assets/53262578/309ee307-bccf-4586-8dcf-1fe007220c09)


### Crafting an exploit 
A JavaScript eval function executes the string argument as a JavaScript body. By creating a JSON with a value containing a JavaScript function, an attacker can execute arbitrary JavaScript code on the vulnerable web application. To enhance the stealthiness of the attack, the perpetrator can structure the payload to mimic the intended behavior of the code snippet, thereby enabling the "sys_sys" argument to be accessible as an argument to 'obj'.

final payload : 
By setting the cookie "pm_sys_sys" to 

```json
{"sys_sys": "workflow", "ola": alert(1)}
```

therefore, an attacker can execute arbitrary js code, while setting the workspace field to the intended workspace for unsuspecting users.



### Possible Exploitation Scenario

An attacker finds an XSS , subdomain takeover or CRLF vulnerability on a domain "*.example.com", he uses the vulnerability to set the cookie "pm_sys_sys" as {"sys_sys": "workflow", "ola": alert(1)} 
with domain set to the main domain the procemaker is on 

![ProcessMaker_POC (1)](https://github.com/proflamyt/300days-of-hacking/assets/53262578/7048ab3b-d8f2-4793-a6cc-d66400cadc57)


```javascript
// example payload
document.cookie='pm_sys_sys={"sys_sys": "workflow", "ola": alert(1)};domain=example.com;path=/;expires=2070-01-01'
```
Ones the infected user visits the vulnrable processmaker subdomain page "sys/en/*/login/login", the xss triggers 

Note: The exeploit could be a key logger as this is the login page
