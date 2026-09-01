# Mini CTF: Broken Access Control & IDOR

A small, self-contained, intentionally vulnerable Flask web app built as a CTF-style practice challenge, plus a full walkthrough of finding and fixing each vulnerability.

## Why I built it

I wanted hands-on practice both finding and explaining real web vulnerability classes (not just running a scanner), and building the vulnerable app myself meant I understood exactly why each flaw exists and how to fix it.

## What's in it

- app.py: the intentionally vulnerable Flask app, with each vulnerability commented and explained in the code
- solve.py: actually solves all three steps against the running app via real HTTP requests, printing what it finds
- WALKTHROUGH.md: full writeup covering finding, flag, root cause, and remediation for each challenge

## Challenges

1. Broken access control: an unlinked admin page reachable with no authentication, discoverable via robots.txt
2. IDOR: changing a numeric ID in the URL exposes another user's private data

## How to run

```bash
pip install flask requests
python3 app.py &
python3 solve.py
```

## Safety

This app only listens on 127.0.0.1 and was never exposed to the public internet. It contains no real user data, and all names, emails, and notes are fictional placeholders.
