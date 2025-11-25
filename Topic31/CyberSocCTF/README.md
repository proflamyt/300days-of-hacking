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
So this is how it works, each team had a secret(Flags) that rotated periodically (uptick time). Stealing another team’s secret and submitting it earned you points. But you cant be doing that manually for 2 weeks straight, 24/7, that would be insane. So of course they were expected to find vulnerabilities and automate their exploitation.

The problem?
I didn’t have the time or infrastructure to spin up separate environments for every team. I had to rely on one shared web application hosting three challenges, most of which were client-side exploit-heavy.

Each vulnerability in the challenge came with its own metrics, but one challenge in particular relied heavily on the browser.
And knowing how smart my colleagues are (they love shortcuts way too much, lol), I had to find a way to keep them inside the browser.

If they automated their uptime checks outside the browser — say with Python scripts or custom clients — other teams wouldnt be able to attack them easily as there are client side vulnerabilities. That wasn’t the experience I wanted.
