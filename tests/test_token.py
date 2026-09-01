import os

import pytest
import requests


def test_github_token_authenticates():

    token = os.getenv("GITHUB_TOKEN", "")

    if not token:

        pytest.skip("GITHUB_TOKEN is not configured.")

    response = requests.get(
        "https://api.github.com/user",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        },
        timeout=30
    )

    response.raise_for_status()

    assert response.json()["login"]
