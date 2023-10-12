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
