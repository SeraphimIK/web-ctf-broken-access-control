# CTF Challenge Walkthrough & Remediation

**Analyst:** Seraphim Ikuomola

## Challenge 1 + 2: Broken Access Control via Hidden Page

**Finding:** `/robots.txt` disallows `/admin_9f3a`, which tells a search engine not to index it — but ironically documents the existence of a hidden admin page to anyone who checks. Visiting `/admin_9f3a` directly returns the admin panel with no login required at all.

**Flag:** `FLAG{unlinked_pages_are_not_access_control}`

**Root cause:** The app relies on "security through obscurity" — assuming a page is safe because it isn't linked anywhere — instead of an actual authentication/authorization check.

**Remediation:** Every sensitive page needs a real server-side check (e.g., verify a valid admin session) regardless of whether the URL is publicly linked. `robots.txt` should never be used to "hide" sensitive paths, since it's publicly readable by design.

## Challenge 3: IDOR (Insecure Direct Object Reference)

**Finding:** `/profile?id=1` shows the logged-in-as user's own profile. Simply changing the URL to `/profile?id=2` returns a completely different user's profile and private note, with no ownership check at all.

**Flag:** `FLAG{idor_exposes_other_users_data}`

**Root cause:** The endpoint trusts the `id` parameter from the client and looks up that record directly, without verifying the requester is actually authorized to view it.

**Remediation:** Never trust a client-supplied ID to determine access. The server should check that the requested resource belongs to (or is otherwise permitted for) the authenticated user before returning it — for example, deriving the user from a validated session token rather than a URL parameter.

## Takeaway

Both vulnerabilities fall under **OWASP Top 10 — A01:2021 Broken Access Control**, the most common category in the current OWASP Top 10. Neither required exploiting a bug in the code in the traditional sense — both were the app doing exactly what it was told, just without an authorization check that should have been there. This is a big part of why access control review matters as much as looking for classic bugs like injection.
