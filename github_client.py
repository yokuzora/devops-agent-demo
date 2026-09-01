import glob
import io
import os
import re
import zipfile

import requests

from agent import investigate
from config import GITHUB_TOKEN
from config import OWNER
from config import REPOSITORY
from database import incident_exists
from database import update_incident_status


TOKEN = GITHUB_TOKEN
LOG_DIR = "logs"


def github_headers():

    return {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json"
    }


def slugify(value):

    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)

    return value.strip("-") or "workflow"


def download_run_logs(run_id, workflow_name):

    log_url = (
        f"https://api.github.com/repos/"
        f"{OWNER}/{REPOSITORY}/actions/runs/"
        f"{run_id}/logs"
    )

    response = requests.get(
        log_url,
        headers=github_headers(),
        timeout=30
    )

    if response.status_code != 200:

        raise RuntimeError(
            f"Failed to download logs for run {run_id}: "
            f"HTTP {response.status_code}"
        )

    run_log_dir = os.path.join(
        LOG_DIR,
        f"{slugify(workflow_name)}-{run_id}"
    )

    os.makedirs(run_log_dir, exist_ok=True)

    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        z.extractall(run_log_dir)

    log_files = glob.glob(
        os.path.join(run_log_dir, "**", "*.txt"),
        recursive=True
    )

    if not log_files:

        raise RuntimeError(f"No log files found for run {run_id}.")

    return max(log_files, key=os.path.getctime)


def get_workflows():

    url = (
        f"https://api.github.com/repos/"
        f"{OWNER}/{REPOSITORY}/actions/workflows"
    )

    response = requests.get(
        url,
        headers=github_headers(),
        timeout=30
    )

    response.raise_for_status()

    return response.json().get("workflows", [])


def get_latest_workflow_run(workflow_id):

    url = (
        f"https://api.github.com/repos/"
        f"{OWNER}/{REPOSITORY}/actions/workflows/"
        f"{workflow_id}/runs"
    )

    response = requests.get(
        url,
        headers=github_headers(),
        params={
            "status": "completed",
            "per_page": 1
        },
        timeout=30
    )

    response.raise_for_status()

    runs = response.json().get("workflow_runs", [])

    if not runs:

        return None

    return runs[0]


def sync_failed_workflows():

    if not TOKEN or TOKEN == "paste_your_token_here":

        return {
            "synced": 0,
            "resolved": 0,
            "skipped": 0,
            "errors": ["GitHub token is not configured."]
        }

    synced = 0
    resolved = 0
    skipped = 0
    errors = []

    try:

        workflows = get_workflows()

    except Exception as exc:

        return {
            "synced": 0,
            "resolved": 0,
            "skipped": 0,
            "errors": [f"Could not fetch workflows: {exc}"]
        }

    for workflow in workflows:

        workflow_name = workflow["name"]

        try:

            latest_run = get_latest_workflow_run(workflow["id"])

        except Exception as exc:

            errors.append(
                f"{workflow_name}: could not fetch runs: {exc}"
            )
            continue

        if latest_run is None:

            skipped += 1
            continue

        conclusion = latest_run.get("conclusion")

        if conclusion == "success":

            resolved += update_incident_status(
                REPOSITORY,
                workflow_name,
                "Resolved"
            )
            continue

        if conclusion != "failure":

            skipped += 1
            continue

        workflow_url = latest_run["html_url"]

        if incident_exists(workflow_url):

            skipped += 1
            continue

        try:

            latest_log = download_run_logs(
                latest_run["id"],
                workflow_name
            )

            investigate(
                latest_log,
                repository=REPOSITORY,
                workflow=workflow_name,
                run_id=str(latest_run["id"]),
                workflow_url=workflow_url
            )

            synced += 1

        except Exception as exc:

            errors.append(
                f"{workflow_name}: {exc}"
            )

    return {
        "synced": synced,
        "resolved": resolved,
        "skipped": skipped,
        "errors": errors
    }


if __name__ == "__main__":

    print("=" * 60)
    print("GITHUB DEVOPS INVESTIGATION")
    print("=" * 60)

    result = sync_failed_workflows()

    print(f"Synced  : {result['synced']}")
    print(f"Resolved: {result['resolved']}")
    print(f"Skipped : {result['skipped']}")

    if result["errors"]:

        print("Errors:")

        for error in result["errors"]:
            print("-", error)

    print("\n" + "=" * 60)
    print("ALL WORKFLOWS PROCESSED")
    print("=" * 60)
