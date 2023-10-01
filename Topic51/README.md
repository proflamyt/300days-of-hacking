# Shodan Dorking 

## Favicon Hash

```python3
import mmh3
import requests
import codecs
 
response = requests.get('https://cybersecurity.wtf/favicon.ico')
favicon = codecs.encode(response.content,"base64")
hash = mmh3.hash(favicon)
print(hash)
```
```
http.favicon.hash
```

## check ASN

```
asn:ASxxxx
```

## CidR

```
net: IP/
```

## Organization 

```
org:microsoft
```

## Expired certificates
```
ssl.cert.expired:true
```
## CN
```
ssl.cert.subject.cn:example.com
```


```
http.html:"* The wp-config.php creation script uses this file"
```

## Jenkins

```
"X-Jenkins" "Set-Cookie: JSESSIONID" http.title:"Dashboard"
x-jenkins 200
```

## Port

```
port:"port"
```


