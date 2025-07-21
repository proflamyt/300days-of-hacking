# NGINX

### Misconfigurations 


#### Missing Root Location


missing root path location 

```bash
root /etc/nginx;

location /index.html {
...
}
```
files within the set root directory will be reachable to any user on the internet.

### Off By Slash

```bash

location /cats {
    alias /usr/share/nginx/html/;
}
```
```
$ ls /usr/share/nginx/html/
index.html ola.html
```
check if both http://frontend/cats/index.html and http://frontend/catsindex.html  resolves to thesame thing


## usage of $uri could lead to crlf 

$uri and $document_uri are already normalized , which implies that they are already decoded

appending %0d%0a  to url could cause crlf injection






Raw Backend response reading

#### merge_slashes set to off
