from datetime import datetime
import os

from database import save_incident


def save_report(
    repository,
    workflow,
    run_id,
    workflow_url,
    category,
    errors,
    root_cause,
    suggestions,
    log_path=""
):

    os.makedirs("reports", exist_ok=True)

    filename = datetime.now().strftime(
        "reports/report_%Y%m%d_%H%M%S.txt"
    )

    with open(filename, "w", encoding="utf-8") as f:

        f.write("=" * 60 + "\n")
        f.write("DEVOPS INVESTIGATION REPORT\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"Timestamp      : {datetime.now()}\n")
        f.write(f"Repository     : {repository}\n")
        f.write(f"Workflow       : {workflow}\n")
        f.write(f"Run ID         : {run_id}\n")
        f.write(f"Workflow URL   : {workflow_url}\n")
        f.write(f"Category       : {category}\n\n")

        f.write("Detected Errors\n")
        f.write("-" * 60 + "\n")
        f.write(errors + "\n\n")

        f.write("Root Cause\n")
        f.write("-" * 60 + "\n")
        f.write(root_cause + "\n\n")

        f.write("Suggested Actions\n")
        f.write("-" * 60 + "\n")

        for action in suggestions:
            f.write(f"- {action}\n")

    save_incident(
        str(datetime.now()),
        category,
        root_cause,
        errors,
        "\n".join(suggestions),
        workflow_url,
        log_path,
        repository,
        workflow,
        "Open"
    )

    return filename
