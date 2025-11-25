## How I Stopped Everyone from Accessing My Web App Without a Browser

There’s nothing like ending the year with a good ol’ CTF. For me, it’s not just about finding flags it’s about bringing the team together, sharpening skills, and getting that rush of solving real problems under pressure. 
This year, I had the task of creating the CyberSOC CTF, and trust me, it was a wild ride.

Our team isn’t one-dimensional. We have security analysts, engineers, red teamers, and threat intelligence specialists. That meant any challenge I designed had to play to everyone’s strengths and expose some weaknesses without leaving anyone behind.
That’s when I decided this isn’t going to be a typical Jeopardy-style CTF. We were going full attack-and-defense mode, just like real-world scenarios.

Here’s how it played out:

Teams had to keep their systems online to earn points ( uptime really mattered). But there’s a twist: being online also made them fair game. Other teams could attack them, draining their defense points, while scoring attack points for themselves.

The clock was ticking, and every vulnerability mattered. Teams had to dive into logs, figure out how they were being hacked, and patch the issues fast. A weak patch? Other teams would find new ways in. A bad patch? Your system could go down entirely, cutting off uptime points and leaving your team scrambling.

It became a game of strategy, skill, and adaptability. One moment, you’re frantically patching a vulnerability; the next, you’re planning a precise attack on another team. It wasn’t just about finding flags — it was about thinking like a hacker and a defender, all at the same time. And the best part? Watching everyone try to outsmart each other, learning, adapting, and laughing along the way.


### The Game
So this is how it works, each team had a secret(Flags) that rotated periodically (uptick time). Stealing another team’s secret and submitting it earned you points. But you cant be doing that manually for 2 weeks straight, 24/7, that would be insane. So of course they were expected to find vulnerabilities and automate their exploitation. We also set up CI/CD for rapid deployments because CTFs always have that one last‑minute fix or restriction that pops up out of nowhere. After deploying the challenges, there was a **foreseen problem** I had been thinking about from the start

The problem?

There is one challenge in particular that relied heavily on the browser and knowing how smart my colleagues are (they love shortcuts way too much, lol), I had to find a way to keep them inside the browser to update their uptime. If they automated their uptime checks outside the browser, say with Python scripts or custom clients, other teams wouldnt be able to attack them easily as these are client side vulnerabilities. That wasn’t the experience I wanted.

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

This is where JA4 comes in. It combines these variables into a single fingerprint, essentially a hash that uniquely identifies each client.
And that was the key. Using JA4, I could reliably say:
“Yep, this is Chrome, Allow it”
or
“Nope, this is a Python script, Block it.”



### The Bot Protection Implementation

Building the CTF infra architecture, I decided to use a reverse proxy to handle the TLS connections before passing traffic to the upstream application.

Here’s the idea:

Since the reverse proxy terminates the TLS connection, it can see the **ClientHello** during the TLS handshake.

We can extract this **ClientHello** and generate a JA4 fingerprint.

That fingerprint can then be sent as an internal header to the upstream server application, which can make access decisions based on it.

In practice, it looked like this:

```
[HAProxy] -> [Gunicorn] -> [Django application]
```

With this setup, my upstream application doesn’t need to worry about TLS — it just trusts the fingerprint header coming from the reverse proxy. And because the fingerprint is unique per client, I could enforce browser-only access and keep any automated scripts out.
I wanted to see if anyone else had already tried something like this. A quick search paid off, I found a Lua plugin for HAProxy that extracts and computes JA4 TLS fingerprints [here](https://github.com/O-X-L/haproxy-ja4-fingerprint/tree/latest). Perfect.



Now that we have everything we need we can proceed to implementation 

First, I had to create an HAProxy configuration that loads the Lua plugin I mentioned earlier. The Lua script handles all the heavy lifting. it reads the TLS ClientHello, computes the JA4 fingerprint, and attaches it to the request as an HTTP headers (I only used X-JA4-Fingerprint):

```
X-JA4-Fingerprint
X-JA4-Raw
```

From there, HAProxy forwards the request upstream to the Django server, now carrying the fingerprint we can validate against.

I also exposed a small utility endpoint, /check-browserprint, which returns the caller’s browser fingerprint. This was my fallback in case the whitelist ever missed a browser and I needed to manually add it.
(*I never actually had to use it, but it was good to have a safety net.*)

```
# /etc/haproxy/haproxy.cfg

defaults
    option httplog
    mode http
    log stdout format raw local0
    timeout client 10s
    timeout connect 10s
    timeout server 10s

global
    tune.ssl.capture-buffer-size 192
    lua-load /home/dev/ja4.lua

frontend test_ja4
    bind *:443 ssl crt /etc/ssl/private/haproxy.pem

    # create fingerprint
    http-request lua.fingerprint_ja4

    # check for related user-agent/application

    # set fingerprint header
    http-request set-header X-JA4-Fingerprint %[var(txn.fingerprint_ja4)]
    http-request set-header X-JA4-Raw %[var(txn.fingerprint_ja4_raw)]


    http-request return status 200 content-type "application/json" lf-string "{\"fingerprint\": \"%[var(txn.fingerprint_ja4)]\", \"details\": \"%[var(txn.fingerprint_ja4_raw)]\", \"app\": \"%[var(txn.fingerprint_app)]\"}" if { path -i /check-browserprint }
    default_backend gunicorn_backend

backend gunicorn_backend
    mode http
    option httpclose
    option forwardfor
    server gunicorn unix@/run/gunicorn.sock check
```


### Getting to the Django Backend

Since we only wanted a subset of clients to reach certain endpoints, i decided to go with a whitelist approach instead of a blacklist. Only clients on the whitelist would be allowed access to the system.

The next step was to build the whitelist. We needed fingerprints for all the common browsers. Luckily, FoxIO‑LLC provides an API that lists known browser fingerprints, which we could query here:

https://ja4db.com/api/read/


By comparing incoming fingerprints against this list, our Django application could allow only legitimate browsers through, blocking any scripts, bots, or custom clients that tried to bypass the system.


Here I wrote a script to extract the common browsers we need and store it in a json format on disk.

```
import requests
import json
import sys

URL = "https://ja4db.com/api/read/"

def fetch_ja4_data():
    print(f"Fetching {URL} ...")
    resp = requests.get(URL, timeout=60)
    resp.raise_for_status()
    return resp.json()


def extract_fingerprints(data):
    chrome_fps = set()
    firefox_fps = set()

    for entry in data:
        ua = (entry.get("user_agent_string") or "").lower()
        ja4 = entry.get("ja4_fingerprint")

        if not ja4 or not ua:
            continue

        if any(k in ua for k in ["chrome", "chromium", "edge", "brave"]):
            chrome_fps.add(ja4)
        elif "firefox" in ua:
            firefox_fps.add(ja4)

    return {
        "chrome": sorted(chrome_fps),
        "firefox": sorted(firefox_fps)
    }

if __name__ == "__main__":
    data = fetch_ja4_data()
    fingerprints = extract_fingerprints(data)

    # Print summary
    print(f"✅ Chrome-like fingerprints: {len(fingerprints['chrome'])}")
    print(f"✅ Firefox fingerprints: {len(fingerprints['firefox'])}")

    # Save only the JA4 fingerprint lists
    with open("ja4_chrome_firefox.json", "w") as f:
        json.dump(fingerprints, f, indent=2)
        print("\n💾 Saved to ja4_chrome_firefox.json")


```



After extracting the fingerprints, the next step was simple: enforce them in our Django application.

I then created a Python decorator that checks incoming requests against the JSON file of known browser fingerprints.

If the client’s JA4 fingerprint is in the whitelist → request is allowed.

If not → request is blocked.

This way, we could easily protect specific endpoints without changing the core logic of our application. Only legitimate browsers could reach the sensitive parts of the system, and any automated scripts or custom clients were effectively stopped in their tracks.


```
import os
import json
from django.conf import settings


JA4_FILE_PATH = os.path.join(settings.BASE_DIR, "ja4_chrome_firefox.json")

try:
    with open(JA4_FILE_PATH) as f:
        JA4_ALLOWED = json.load(f)
except FileNotFoundError:
    JA4_ALLOWED = {"chrome": [], "firefox": []}

# Flatten all allowed fingerprints into a set
JA4_ALLOWED_SET = set(JA4_ALLOWED.get("chrome", []) + JA4_ALLOWED.get("firefox", []))

```




Django decorator
```
from django.http import JsonResponse
from functools import wraps
from .ja4_allowed import JA4_ALLOWED_SET
import logging

logger = logging.getLogger(__name__)

def ja4_required(view_func):
    """
    Decorator that allows only requests with JA4 fingerprint in the allowed set.
    Expects 'X-JA4-Fingerprint' header from HAProxy.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        ja4 = request.headers.get("X-JA4-Fingerprint")
        logging.info(f"Allowing:  {ja4}")
        if not ja4:
            return JsonResponse({"error": "Missing JA4 fingerprint header"}, status=400)

        if ja4 not in JA4_ALLOWED_SET:
            logging.info(f"Rejected Bot:  {ja4}")
            return JsonResponse({"error": "Access denied: unrecognized User"}, status=403)

        return view_func(request, *args, **kwargs)
    return wrapper

```


<img width="500" height="152" alt="Screenshot 2025-11-25 153344" src="https://github.com/user-attachments/assets/e67d4920-c169-46c0-9c6b-7b9cc96c30b0" />

Implementing The Decorator




### A player that says the CTF Creator will not sleep will also have no peace ..... 

<img width="225" height="225" alt="image" src="https://github.com/user-attachments/assets/c742c4ec-ade7-4bd1-9f46-b4a0e72656db" />

About 12 hours before the end of the challenge, I decided to tighten things even further and restrict the remaining endpoints as well.

The moment I pushed the update…
boom — every team’s automation broke.

All the scripts they had relied on for days suddenly stopped working, and the panic set in. But in true CTF fashion, everyone adapted quickly. Teams scrambled, analyzed the new fingerprinting behavior, and came up with their own creative bypasses and browser-based automation solutions.

Honestly, watching them pivot under pressure was fun and exactly the kind of real-world problem-solving we wanted from this challenge.

If any team writes a post-CTF write-up, this last-minute twist will definitely be a chapter in theirs.

### Other Use Case

You can extend this approach to mobile applications as well. By creating a custom TLS ClientHello and whitelisting its JA4 fingerprint, you can ensure only your mobile client can access the backend.


Ciao.
