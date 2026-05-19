---
title: "Understanding HTTP"
topic: "understanding-http"
tags: [http, https, web, protocols, headers, cookies]
difficulty: beginner
day: 3
layout: default
parent: Topics
nav_order: 3
---

# Understanding HTTP (Hyper Text Transfer Protocol)

## What You Will Learn
- What HTTP is and how it works
- The difference between HTTP and HTTPS
- How requests and responses are structured
- What HTTP methods, status codes, and headers are
- What cookies are and why they matter for security
- How HTTP has evolved from version 1.0 to HTTP/3

## What is HTTP?

HTTP is the foundation of data exchange on the web. It is a set of agreed rules on how data is transmitted between a client and a server. The client (in this case, you) and the web server (e.g., tryhackme.com) must agree on how communication is to be exchanged in order to have a meaningful conversation.

Clients and servers communicate by exchanging individual messages (as opposed to a stream of data). The messages sent by the client, usually a web browser, are called **requests** and the messages sent by the server as an answer are called **responses**.

What most websites use nowadays is **HTTPS**, an upgrade of HTTP. The "S" stands for "Secure" — it adds an encryption layer to data in transit. Anyone between you and the server you are communicating with will only see jumbled, meaningless data and will not be able to change it in transit, which protects your data integrity.

For you to understand the ways data is transmitted and received, you have to understand:

- Requests
- Responses

When you access a website through a browser, your browser underneath the hood has to get the images, text, and HTML from the server. These exchanges are possible because your browser asks the website for these resources (**REQUEST**), and the web server (which speaks the same language) replies with the resource requested (**RESPONSE**).

## URLs (Uniform Resource Locator)

A URL is essentially an instruction on how to access a resource on the internet. You want your profile on TryHackMe? You have to tell the website where to look for it. You have to tell it:

- The protocol you want to use
- Where you want to access
- What you want to access

## Making a Request

Now let's talk about requests. You've been making requests all your life — asking for resources from servers, giving them resources to save or use. Let's look at how these requests are made.

### HTTP Methods

HTTP methods are a way for the client to show their intended action when making an HTTP request. There are a lot of HTTP methods but we'll cover the most common ones — although mostly you'll deal with GET and POST.

- **GET Request**: Used when requesting information from a web server.
- **POST Request**: Used when submitting data to the web server and potentially creating new records.
- **PUT Request**: Used when you want to modify a single resource that is already part of a resource collection.
- **DELETE Request**: Used for deleting information or records from a web server.

### HTTP Status Codes

When surfing the web there is a high probability that you have come across "404 Page Not Found." Status codes are responses that tell you what happened to your request.

| Code | Name | Meaning |
|------|------|---------|
| 200 | OK | The request was completed successfully. |
| 201 | Created | A resource has been created (e.g., a new user or blog post). |
| 301 | Permanent Redirect | This redirects the client's browser to a new webpage or tells search engines the page has moved. |
| 302 | Temporary Redirect | A temporary change; it may change again in the near future. |
| 400 | Bad Request | Something was either wrong or missing in the request. |
| 401 | Not Authorized | You are not currently allowed to view this resource until you have authorized with the web application. |
| 403 | Forbidden | You do not have permission to view this resource whether you are logged in or not. |
| 404 | Page Not Found | The page/resource you requested does not exist. |
| 405 | Method Not Allowed | The resource does not allow this method request (e.g., you sent a GET request when it expected POST). |
| 500 | Internal Server Error | The server has encountered some kind of error it doesn't know how to handle properly. |
| 503 | Service Unavailable | The server cannot handle your request as it's either overloaded or down for maintenance. |
| 504 | Gateway Timeout | The server was acting as a gateway or proxy and did not receive a timely response from the upstream server. |
| 505 | HTTP Version Not Supported | The server does not support the HTTP protocol version used in the request. |

## Headers

Headers are additional bits of information you send to the server when making a request. An HTTP header consists of its case-insensitive name followed by a colon (`:`), then by its value.

### Request Headers

A request header provides information about the request context so the server can tailor the response. Common request headers:

- **Host**: Some web servers host multiple websites, so providing the host header tells it which one you require.
- **Authorization**: Used to control caching or to pass user credentials.
- **Accept-Encoding**: Tells the web server what types of compression the browser supports so data can be made smaller for transmission.
- **Content-Type**: Specifies the media type of the request being sent from the client to the server.
- **User-Agent**: Your browser software and version number, helping the web server format the website properly for your browser.

### Response Headers

These headers are returned to the client from the server after a request. Common response headers:

- **Content-Type**: Tells the client what type of data is being returned (HTML, CSS, JavaScript, Images, PDF, Video, etc.).
- **Content-Encoding**: What compression method has been used on the data.
- **Set-Cookie**: Information to store which gets sent back to the web server on each subsequent request.
- **Cache-Control**: How long to store the content of the response in the browser's cache before requesting it again.

## Cookies

A cookie is a small piece of data that a server sends to the user's web browser. The browser may store it and send it back with later requests to the same server. Because HTTP is stateless (it doesn't keep track of your previous requests), cookies are used to remind the web server who you are, some personal settings for the website, or whether you've been to the website before.

Cookies are used mainly for three purposes:

- **Session management**: Logins, game scores, or anything else the server should remember.
- **Personalization**: User preferences, themes, and other settings.
- **Tracking**: Recording and analyzing user behavior.

### Viewing Your Cookies

You can view what cookies your browser is sending to a website by using the browser's developer tools. Open developer tools, click on the **Network** tab, then click on a request. If your browser sent a cookie, you will see it on the **Cookies** tab of the request.



# HTTP Versions

### HTTP/0.9

This is the beginning of HTTP versioning. In this version, only one method was available — the GET request. There were no HTTP headers, so only HTML files could be transmitted.

### HTTP/1.0

The protocol became more evolved and the concept of HTTP headers was introduced for both requests and responses. Metadata could be transmitted and the protocol became extremely flexible and extensible. Documents other than HTML files could be transmitted.

### HTTP/1.1

- **Connection Reuse**: Prior to this version, every HTTP request required a new TCP connection. HTTP/1.1 allows connection reuse — after the initial handshake, requests and responses can continue without closing the connection. Both parties include a `Connection: keep-alive` header to indicate their intention to reuse the TCP connection. The connection stays open until either side explicitly closes it with `Connection: close` or a timeout occurs.

- **HTTP Pipelining**: Before a response to one request is complete, HTTP/1.1 supports sending another request.

- **Chunked Responses**: This feature allows the server to send a response as a series of "chunks" instead of sending the entire response at once. Particularly useful when the server cannot determine the total response size in advance, or when the response needs to be streamed progressively.

### HTTP/2

HTTP/2 has several improvements:

- It is a binary protocol.
- Parallel requests can be made over the same connection.
- It compresses headers.
- It allows a server to populate data in a client cache through server push.

### HTTP/3

HTTP/3 uses the QUIC protocol for data exchange, which runs over UDP instead of TCP, reducing latency.

---

Reference: https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Evolution_of_HTTP
