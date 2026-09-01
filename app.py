"""
app.py — a small, self-contained, intentionally vulnerable web app built
for CTF-style practice. It is NOT connected to the internet and contains
no real user data — every "vulnerability" here is a deliberate teaching
example of a common OWASP Top 10 category.

Challenges:
  1. Hidden page via URL guessing (Security Misconfiguration / Broken
     Access Control — an unlinked admin page with no auth check)
  2. IDOR (Insecure Direct Object Reference) — changing a numeric ID in
     the URL exposes another user's private data
  3. Sensitive data left in an HTML comment (client-side info exposure)

Each challenge yields a flag in the format FLAG{...}.
"""
from flask import Flask, request, render_template_string, abort

app = Flask(__name__)

USERS = {
    1: {"name": "jsmith", "email": "jsmith@example.com", "note": "Nothing interesting here."},
    2: {"name": "admin", "email": "admin@example.com", "note": "FLAG{idor_exposes_other_users_data}"},
    3: {"name": "mkoenig", "email": "mkoenig@example.com", "note": "Reminder: rotate API key Friday."},
}

HOME = """
<h1>Acme Corp Internal Portal</h1>
<p>Welcome. Log in to view your profile.</p>
<a href="/profile?id=1">View my profile</a>
<!-- TODO: remove before prod -- staging admin panel is at /admin_9f3a -->
"""

PROFILE = """
<h1>Profile: {{ user.name }}</h1>
<p>Email: {{ user.email }}</p>
<p>Note: {{ user.note }}</p>
<a href="/">Back</a>
"""

ADMIN = """
<h1>Admin Panel</h1>
<p>You found the hidden admin page.</p>
<p>FLAG{unlinked_pages_are_not_access_control}</p>
"""


@app.route("/")
def home():
    return HOME


@app.route("/profile")
def profile():
    # VULNERABLE: no check that the requester owns this id (IDOR)
    user_id = int(request.args.get("id", 1))
    user = USERS.get(user_id)
    if not user:
        abort(404)
    return render_template_string(PROFILE, user=user)


@app.route("/admin_9f3a")
def admin():
    # VULNERABLE: "security through obscurity" — reachable by anyone who
    # finds/guesses the URL, no authentication check at all.
    return ADMIN


@app.route("/robots.txt")
def robots():
    # A real-world way this kind of hidden path often leaks: it's listed
    # here to keep search engines out, which ironically documents it.
    return "User-agent: *\nDisallow: /admin_9f3a\n", 200, {"Content-Type": "text/plain"}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050)
