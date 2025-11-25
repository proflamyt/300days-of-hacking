#### How I Stopped Everyone from Accessing My Web App Without a Browser

There’s nothing like ending the year with a good ol’ CTF. For me, it’s not just about finding flags it’s about bringing the team together, sharpening skills, and getting that rush of solving real problems under pressure. 
This year, I had the task of creating the CyberSOC CTF, and trust me, it was a wild ride.

Our team isn’t one-dimensional. We have security analysts, engineers, red teamers, and threat intelligence specialists. That meant any challenge I designed had to play to everyone’s strengths and expose some weaknesses without leaving anyone behind.
That’s when I decided this isn’t going to be a typical Jeopardy-style CTF. We were going full attack-and-defense mode, just like real-world scenarios.

Here’s how it played out:

Teams had to keep their systems online to earn points ( uptime really mattered). But there’s a twist: being online also made them fair game. Other teams could attack them, draining their defense points, while scoring attack points for themselves.

The clock was ticking, and every vulnerability mattered. Teams had to dive into logs, figure out how they were being hacked, and patch the issues fast. A weak patch? Other teams would find new ways in. A bad patch? Your system could go down entirely, cutting off uptime points and leaving your team scrambling.

It became a game of strategy, skill, and adaptability. One moment, you’re frantically patching a vulnerability; the next, you’re planning a precise attack on another team. It wasn’t just about finding flags — it was about thinking like a hacker and a defender, all at the same time. And the best part? Watching everyone try to outsmart each other, learning, adapting, and laughing along the way.


### The Game
So this is how it works, each team had a secret(Flags) that rotated periodically (uptick time). Stealing another team’s secret and submitting it earned you points. But you cant be doing that manually for 2 weeks straight, 24/7, that would be insane. So of course they were expected to find vulnerabilities and automate their exploitation. We also set up CI/CD for rapid deployments because CTFs always have that one last‑minute fix or restriction that pops up out of nowhere.

The problem?
Each vulnerability in the challenge came with its own metrics, but one challenge in particular relied heavily on the browser.

And knowing how smart my colleagues are (they love shortcuts way too much, lol), I had to find a way to keep them inside the browser to update their uptime. If they automated their uptime checks outside the browser — say with Python scripts or custom clients — other teams wouldnt be able to attack them easily as there are client side vulnerabilities. That wasn’t the experience I wanted.

So this left me with one big question:
How do I stop them from automating uptime without a browser?


### The Solution
I had to force them to use a real browser — not Python requests, not curl, not Go HTTP clients.

I needed the server to instantly know:
**“Who exactly is talking to me?”**

Is it Chrome?

Firefox?

A bot?

A script?

A custom TLS client?

And then it clicked.

TLS fingerprinting !!!!

More specifically:

### JA4 Fingerprinting

I decided to build a bot‑prevention solution using one of the solutions from the JA4+ network fingerprinting suite (created by John Althouse — the project lives here: [FoxIO‑LLC/ja4](https://github.com/FoxIO-LLC/ja4)).
My goal was simple:

If I can reliably tell a real browser apart from everything else, I can block everything else.

**No Python scripts.**

**No curl.**

**No custom Go clients.**

.... **Just real browsers, exactly the way I wanted.**

The JA4+ suite is used for all sorts of serious stuff — spotting threat actors, malware detection, preventing session hijacking, compliance automation, location fingerprinting, DDoS detection, grouping attacker behavior, reverse‑shell detection…the list goes on.

Me?
I only needed JA4 (the TLS fingerprint) — nothing fancy — just enough information to identify the type of client talking to my server based on its TLS connection behavior.

### Who is Who?


#### TLS Connection

A TLS connection is how two parties (client ↔ server) create a secure, encrypted channel. It happens in phases:

- Server → Client: “Here’s what we’ll use, plus my certificate.”

- Key exchange: Both sides derive shared encryption keys.

- Encrypted communication begins.

The very first message the client sends we call  the **ClientHello**, this is usually in clear text (except when the client uses ECH). This message is packed with a lot of information:


- TLS version

- Random bytes

- Session ID

- Cipher suites

- Compression methods

- Various extensions

Because most clients — whether it’s Chrome, Python requests, curl, Go’s http.Client, or a reverse shell — populate these fields differently, the **ClientHello** is effectively unique per application or TLS library. They may have Different cipher suites, Different extensions, Different order of fields, Different behavior depending on OS, browser version, or SSL library. The **clientHello** for chrome browser on windows may be diffrent from that of thesame browser on linux.Those patterns are like a fingerprint.

This is where JA4 comes in. It combines these variables into a single fingerprint, essentially a hash that uniquely identifies each client. That fingerprint lets the server say:

And that was the key. Using JA4, I could reliably say:
“Yep, this is Chrome”
or
“Nope, this is a Python script. Block it.”



