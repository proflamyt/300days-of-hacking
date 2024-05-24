# NGINX

### Misconfigurations 


#### Missing Root Location


missing root path location 

```bash
location / {
...
}
```
files within the set root directory will be reachable to any user on the internet.

### Off By Slash

```bash
location /api {
}
```

check static too
check http://frontend/api/user resolves to  http://frontend/apiuser 


## crlf 

append %0d%0a  to url

Unsafe variable use

Raw Backend response reading

#### merge_slashes set to off
