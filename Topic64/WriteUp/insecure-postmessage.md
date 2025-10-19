# How We Got Admin Tokens via Insecure PostMessage

We’ve all heard it before — *“client-side validation and authentication don’t count.”* If you want real security, it has to be on the server.

That’s true in many cases (emphasis on many), but not always. As I’ll show later, some types of validation actually depend entirely on the client.

Here’s a quick breakdown of what I mean by client in the context of a web application:

```
[ Server (backend code) ]  ->  [ Browser (frontend code) ]  <-  User
```


What is referrred to as the **server-side** (or backend) is usually a black box — it handles logic, data processing, and serving responses for the web app.

Also, what can be considered as **client-side** refers to the code that runs in the browser — typically HTML, CSS, and JavaScript — responsible for rendering, interaction, and the user interface. That’s the part users directly interact with.

It’s worth noting that architecture can vary. In some setups, a proxy may be in a position to be referred to  as the client depending on the situation. But in our case, when we say client, we’re strictly talking about the code running inside the browser.


## Client-Side Validation (Why It Matters)

Let’s start with one of the basics of browser security — the **Same Origin Policy (SOP)**. One of the browser’s main jobs is to protect *you*, the user, and your system from the wild west of the internet.  

Without those protections, imagine visiting some random site like `example.com` and it could just read files from your computer or peek into other tabs you have open. Maybe one of those tabs has a private chat or sensitive info. That would be a total nightmare, right?  

That’s exactly why SOP exists. It’s basically a rule that says: a website can’t freely interact with another website that has a *different origin*.  

In this context, **“origin”** is very specific — it includes the **protocol**, **host**, and **port**. So, if any of those don’t match, they’re considered different origins. This is why your Facebook tab has no idea what you’re reading or typing on X (Twitter), even though both are open in the same browser.  

And here’s where it really makes sense: your browser can technically open local files using something like the `file://` protocol (for example, `file:///etc/hosts`). But when you visit a site like `https://evil[.]com`, it can’t reach into your local files — even if both are open at the same time.  

That’s the Same Origin Policy doing its job. It keeps websites in their own little sandbox and stops them from crossing into places they shouldn’t — like your system files or other sites you’re logged into.


For example, Chrome enforces this by running each website inside a tightly controlled **sandbox**. This sandbox stops the page from directly touching your files or any sensitive system resources. Whenever a page needs to access something local — like a file or the network — it has to go through Chrome’s trusted **browser kernel process** using **Inter-Process Communication (IPC)**. In short, even if a site tries to break out, it’s stuck talking through Chrome’s security gate.

## Communicating Across Origins and Domains

The Same Origin Policy is pretty awesome as it’s one of the main things keeping attackers from messing with our data or stealing info between sites. But there’s a catch: while SOP keeps us safe, it also makes it harder for different sites to talk to each other when they actually *need* to.

Pretty soon, web developers and users realized that for the internet to feel seamless, websites sometimes need a way to share resources or send messages across domains. A common example is **signing in across different sites** — say you’re logged into Website A, and Website B needs to confirm that without asking you to log in again.

To make that possible (and still keep things secure), browsers introduced controlled ways for cross-domain communication, mainly through:

- **CORS (Cross-Origin Resource Sharing)**
- **PostMessage API**

In this writeup, we’ll be focusing on the **PostMessage** part and how it was used insecurely.


### Posting Messages

The **PostMessage** API works kind of like a broadcast system. One origin can “shout” a message to another origin — or even to *anyone* who’s listening. On the other end, an origin can choose to listen for incoming messages or send out its own broadcasts. It’s basically an open communication channel within the browser world.

But here’s the catch — shouting to *everyone* isn’t always a great idea. In practice, a site should only send messages to a **specific, trusted origin**. The same goes for receiving messages: blindly accepting data from any random source is risky, especially if you’re going to use that data in your page or UI. That’s how things can get messy (and sometimes, exploitable).

### Origin A sending a message to Origin B

The model for sending and receiving messages with `postMessage` is pretty simple:  
- **Origin A** sends a message using the `window.postMessage()` API.  
- **Origin B** listens for it with the `window.onmessage` event handler.  

When the message is received, the `onmessage` callback gets an **event object** that includes:  
- `data` → the actual content being sent, and  
- `origin` → the domain of whoever sent the message.
- `source` ->  message emitter
- `port` ->  objects  associated with the channel the message is being sent through
- `lasteventid` -> unique ID for the event.

  https://developer.mozilla.org/en-US/docs/Web/API/Worker/message_event

Here’s a simple example:

```js
// ---- Origin A (sender) ----
const popup = window.open("https://example-b.com", "_blank");

// Send a message to Origin B
popup.postMessage({ action: "getAdminToken" }, "https://example-b.com");


// ---- Origin B (receiver) ----
window.addEventListener("message", (event) => {
  // Always check who sent the message
  if (event.origin !== "https://example-a.com") return;

  console.log("Message received:", event.data);
  // respond if needed
  event.source.postMessage({ token: "admin-123" }, event.origin);
});
```

### Vulnerability Discovered

A coworker spotted a weird feature in a common web app: when you click **“Login as Admin”**, a popup briefly appears shows authentication failed and sends the user that wants to authenticate as the admin to a login page that asks for a username and password. We wondered — how was the site trying to authenticate in the first place?

Digging through the frontend code, we found the code that opens the popup and discovered it waits for a postmessage `message` event. Once it receives a message, the code checks that `event.origin` matches the origin it opened (good — that prevents blindly accepting any postMessage broadcast). If the origin matches, it takes the `data` from the message and uses that data to set the user session.


<img width="1320" height="169" alt="image" src="https://github.com/user-attachments/assets/0400040f-27ee-4bb2-a4ce-520022b4914a" />


So — is this exploitable?

First, we checked whether we controlled the validation URL. If we did, that would’ve been ideal — we could send a cross-origin message that the site would accept. We decided not to pursue that path because we couldn’t find a way to bypass the validation. Even if there wasn’t a strict check, we’d also need to find a **sink** — somewhere the app actually *uses* the data insecurely. Without a vulnerable sink, the best we could do was force the user to use our session if there were self xss and we couldn’t make the site accept arbitrary validation responses from us.


