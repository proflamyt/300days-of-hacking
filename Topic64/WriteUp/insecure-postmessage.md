### How We Got Admin Tokens via Insecure PostMessage

We’ve all heard it before — *“client-side validation and authentication don’t count.”* If you want real security, it has to be on the server.

That’s true in many cases (emphasis on many), but not always. As I’ll show later, some types of validation actually depend entirely on the client.

Here’s a quick breakdown of what I mean by client in the context of a web application:

```
[ Server (backend code) ]  ->  [ Browser (frontend code) ]  <-  User
```


What is referrred to as the **server-side** (or backend) is usually a black box — it handles logic, data processing, and serving responses for the web app.

Also, what can be considered as **client-side** refers to the code that runs in the browser — typically HTML, CSS, and JavaScript — responsible for rendering, interaction, and the user interface. That’s the part users directly interact with.

It’s worth noting that architecture can vary. In some setups, a proxy may be in a position to be referred to  as the client depending on the situation. But in our case, when we say client, we’re strictly talking about the code running inside the browser.


### Client-Side Validation (Why It Matters)

Let’s start with one of the basics of browser security — the **Same Origin Policy (SOP)**. One of the browser’s main jobs is to protect *you*, the user, and your system from the wild west of the internet.  

Without those protections, imagine visiting some random site like `example.com` and it could just read files from your computer or peek into other tabs you have open. Maybe one of those tabs has a private chat or sensitive info. That would be a total nightmare, right?  

That’s exactly why SOP exists. It’s basically a rule that says: a website can’t freely interact with another website that has a *different origin*.  

In this context, **“origin”** is very specific — it includes the **protocol**, **host**, and **port**. So, if any of those don’t match, they’re considered different origins. This is why your Facebook tab has no idea what you’re reading or typing on X (Twitter), even though both are open in the same browser.  

And here’s where it really makes sense: your browser can technically open local files using something like the `file://` protocol (for example, `file:///etc/hosts`). But when you visit a site like `https://evil[.]com`, it can’t reach into your local files — even if both are open at the same time.  

That’s the Same Origin Policy doing its job. It keeps websites in their own little sandbox and stops them from crossing into places they shouldn’t — like your system files or other sites you’re logged into.


For example, Chrome enforces this by running each website inside a tightly controlled **sandbox**. This sandbox stops the page from directly touching your files or any sensitive system resources. Whenever a page needs to access something local — like a file or the network — it has to go through Chrome’s trusted **browser kernel process** using **Inter-Process Communication (IPC)**. In short, even if a site tries to break out, it’s stuck talking through Chrome’s security gate.

### Communicating Across Origins and Domains

The Same Origin Policy is pretty awesome as it’s one of the main things keeping attackers from messing with our data or stealing info between sites. But there’s a catch: while SOP keeps us safe, it also makes it harder for different sites to talk to each other when they actually *need* to.

Pretty soon, web developers and users realized that for the internet to feel seamless, websites sometimes need a way to share resources or send messages across domains. A common example is **signing in across different sites** — say you’re logged into Website A, and Website B needs to confirm that without asking you to log in again.

To make that possible (and still keep things secure), browsers introduced controlled ways for cross-domain communication, mainly through:

- **CORS (Cross-Origin Resource Sharing)**
- **PostMessage API**

In this writeup, we’ll be focusing on the **PostMessage** part and how it was used insecurely.


### Posting Messages


