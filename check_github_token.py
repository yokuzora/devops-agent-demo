import os

import requests


def main():

    token = os.getenv("GITHUB_TOKEN", "")

    if not token:

        print("Authentication Failed")
        print("Set GITHUB_TOKEN before running this check.")
        return 1

    response = requests.get(
        "https://api.github.com/user",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        },
        timeout=30
    )

    if response.status_code != 200:

        print("Authentication Failed")
        print(response.status_code)
        print(response.text)
        return 1

    user = response.json()

    print("=" * 40)
    print("Authentication Successful")
    print("=" * 40)
    print("Username :", user.get("login"))
    print("Name     :", user.get("name"))
    print("Repos    :", user.get("public_repos"))

    return 0


if __name__ == "__main__":

    raise SystemExit(main())
