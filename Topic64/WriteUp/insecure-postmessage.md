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
