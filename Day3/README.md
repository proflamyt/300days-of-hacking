# Understanding-HTTP-Hyper-Text-Transfer-Protocol-Secure-for-dummies 



## What is HTTP?
HTTP is the fundamental of data exchange on the web
It is a set of agreed rules on how data is being transmitted on the web. The client (in this case you)
and the web server (try hackme.com) must agree on how communications is to be exchanged
between in order to have a meaningful conversation.
Clients and servers communicate by exchanging individual messages (as opposed to a stream of
data). The messages sent by the client, usually a Web browser, are called requests and the messages
sent by the server as an answer are called responses.
What most websites use nowadays is the http, an upgrade of http. This S -meaning (secure)- added
an encryption layer to the data in transit, this way anyone between you and the server you are
communicating with will only see jumbled, rubbish and un-meaningful data , also, won’t be able
to change it in transit , thus affecting your data integrity.
For you to understand the ways data are transmitted and received you have to understand these;
• Request and
• Responses.
Earlier, it was mentioned, that data being transferred to and from you to a webserver, in this case
“tryhackme.com”, these data are in form of request and responses, most times you access a website
through a browser, your browser underneath the hood has to get the images, texts, html from the
server you want to access, this way you can see a nicely rendered page which you make sense of.
These exchange is possible due to your browser asking your website for these resource
(REQUEST) and the webserver understanding this language (since you both speak http), replies
with the resource you requested for (RESPONSE).

## URLS (Uniform Resource Locator)
There is high likelihood you’ve come across URLS, if you've visited websites before , you might
not have made sense of it till now.
A URL is predominantly an instruction on how to access a resource on the internet. You want your
profile on tryhackme you have to tell the website where to look for it, if you want to check a
different part of the website, you have to tell this website where to look for them. You have to tell
it the protocol you would like, where you want to access , how you want to access it , what you
want to access from it

### Making a request
Now let us talk about request. You've been making requests all your life, asking for resources from
servers, giving them resources to save or use. Now hackers, let us look at how these requests are
made.

#### HTTP Methods
HTTP methods are a way for the client to show their intended action when making an HTTP
request. There are a lot of HTTP methods but we'll cover the most common ones, although mostly
you'll deal with the GET and POST method.
• GET Request: This is used when requesting information from a web server
• POST Request: This is used when submitting data to the web server and potentially
creating new records.
• PUT Request: This is used when you want to modify a single resource which is already
part of a resource collection.
• DELETE Request: This is used for deleting information/records from a web server.

#### HTTP Status code
When surfing the web there is a high probability that you have come across the word “404-page
not found” and this is a response telling you that you have no permission to view this page whether
logged in on not. In this case we will go through the possible http response you are most likely to
come across.
Table showing the popular http status code
S/n Responses Meaning
1. 200 - OK The request was completed successfully
2. 201 - Created A resource has been created (for example a new user or new

blog post).

3. 302 - Temporary
Redirect

Similar to the above permanent redirect, but as the name
suggests, this is only a temporary change and it may change
again in the near future.

4. 301 - Permanent
Redirect

This redirects the client's browser to a new webpage or tells
search engines that the page has moved somewhere else and to
look there instead.

5. 400 - Bad Request This tells the browser that something was either wrong or
missing in their request. This could sometimes be used if the
web server resource that is being requested expected a certain
parameter that the client didn't send.

6. 401 - Not Authorized You are not currently allowed to view this resource until you
have authorized with the web application, most commonly with
a username and password.

7. 403 - Forbidden You do not have permission to view this resource whether you

are logged in or not.

8. 404- Page Not Found The page/resource you requested does not exist.
9. 405 - Method Not
Allowed

The resource does not allow this method request, for example,
you send a GET request to the resource /create-account when it
was expecting a POST request instead.

10. 500 - Internal Service
Error

The server has encountered some kind of error with your request
that it doesn't know how to handle properly.

11. 503 - Service
Unavailable

This server cannot handle your request as it's either overloaded
or down for maintenance

12. 504 Gateway Timeout The server was acting as a gateway or proxy and did not
receive a timely response from the upstream server.

13. 505 HTTP Version Not
Supported

The server does not support the HTTP protocol version used in
the request

## Headers
Headers are additional bit of information you send to the servers when making request. An HTTP
header consists of its case-insensitive name followed by a colon (:), then by its value.
Request header
A request header is an HTTP header that can be used in an HTTP request to provide information
about the request context, so that the server can tailor the response. Common request headers are
• Host: Some web servers host multiple websites so by providing the host headers you can
tell it which one you require, otherwise you'll just receive the default website for the server.
• Authorization: Authorization headers are used to control caching, or to get information
about the user agent or referrer.
• Accept-Encoding: Tells the web server what types of compression methods the browser
supports so the data can be made smaller for transmitting over the internet.
• Content- type: This is a way to specify the media type of request being sent from the client
to the server.
• User-Agent: This is your browser software and version number, telling the web server your
browser software helps it format the website properly for your browser and also some
elements of HTML, JavaScript and CSS are only available in certain browsers.
Response header

These are the headers that are returned to the client from the server after a request. A response
header is an HTTP header that can be used in an HTTP response and that doesn't relate to the
content of the message. Response headers, like Age , Location or Server are used to give a more
detailed context of the response. Common response headers are:
• Content-Type: This is a representation header that tells the client what type of data is being
returned, i.e., HTML, CSS, JavaScript, Images, PDF, Video, etc. Using the content-type
header the browser then knows how to process the data.
• Content-Encoding: What method has been used to compress the data to make it smaller
when sending it over the internet.
• Set-Cookie: Information to store which gets sent back to the web server on each request.
• Cache-Control: How long to store the content of the response in the browser's cache before
it requests it again.

Cookies
A cookie is a small piece of data that a server sends to the user's web browser. The browser may
store it and send it back with later requests to the same server. Typically, it's used to tell if two
requests came from the same browser keeping a user logged-in. Because HTTP is stateless (doesn't
keep track of your previous requests), cookies can be used to remind the web server who you are,
some personal settings for the website or whether you've been to the website before. Cookies are
used mainly for three purposes:
• Session management i.e. logins, game scores, or anything else the server should remember
• Personalization like user preferences, themes, and other settings
• Tracking i.e. recording and analyzing user behavior
Viewing Your Cookies
You can easily view what cookies your browser is sending to a website by using the developer
tools, in your browser. If you're not sure how to get to the developer tools in your browser, click
on the "View Site" button at the top of this task for a how-to guide.

Once you have developer tools open, click on the "Network" tab. This tab will show you a list of
all the resources your browser has requested. You can click on each one to receive a detailed
breakdown of the request and response. If your browser sent a cookie, you will see these on the
"Cookies" tab of the request.
