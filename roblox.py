import json
import requests
from pathlib import Path

CACHE_FILE = Path("cache.json")

API_URL = "https://users.roblox.com/v1/usernames/users"


def load_cache():

    if CACHE_FILE.exists():

        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    return {}


cache = load_cache()


def save_cache():

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            cache,
            f,
            indent=4,
            ensure_ascii=False
        )


def lookup(username: str):

    username = username.strip()

    if username in cache:

        print(f"[CACHE] {username}")

        return cache[username]

    print(f"[LOOKUP] {username}")

    payload = {
        "usernames": [username],
        "excludeBannedUsers": False
    }

    r = requests.post(
        API_URL,
        json=payload,
        timeout=10
    )

    r.raise_for_status()

    data = r.json()["data"]

    if not data:

        print(f"[NOT FOUND] {username}")

        return None

    user_id = data[0]["id"]

    profile = f"https://www.roblox.com/users/{user_id}/profile"

    cache[username] = profile

    save_cache()

    print(f"[CACHED] {username}")

    return profile
