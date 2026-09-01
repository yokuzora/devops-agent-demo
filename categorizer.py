CATEGORIES = {

    "Dependency Error": [
        "No matching distribution found",
        "Could not find a version",
        "pip install",
        "ModuleNotFoundError",
        "ImportError",
        "requirements.txt"
    ],

    "Docker Error": [
        "docker build",
        "docker.io",
        "Dockerfile",
        "manifest",
        "load metadata",
        "failed to solve",
        "pull access denied",
        "not found"
    ],

    "Permission Error": [
        "permission denied",
        "access denied",
        "forbidden",
        "unauthorized",
        "403",
        "401"
    ],

    "Python Error": [
        "Traceback",
        "SyntaxError",
        "NameError",
        "TypeError",
        "ValueError",
        "ModuleNotFoundError"
    ],

    "Test Failure": [
        "FAILED",
        "AssertionError",
        "pytest",
        "JUnit",
        "test failed"
    ],

    "Kubernetes Error": [
        "CrashLoopBackOff",
        "OOMKilled",
        "kubectl",
        "FailedScheduling",
        "ImagePullBackOff"
    ]
}


def categorize(error_log):

    text = error_log.lower()

    # ---------- Dependency ----------
    if (
        "no matching distribution found" in text
        or "could not find a version" in text
        or "requirements.txt" in text
    ):
        return "Dependency Error"

    # ---------- Docker ----------
    if (
        "docker.io" in text
        or "dockerfile" in text
        or "load metadata" in text
        or "failed to solve" in text
        or "manifest" in text
        or ("docker" in text and "not found" in text)
    ):
        return "Docker Error"

    # ---------- Permission ----------
    if (
        "permission denied" in text
        or "access denied" in text
        or "forbidden" in text
        or "unauthorized" in text
        or "401" in text
        or "403" in text
    ):
        return "Permission Error"

    # ---------- Python ----------
    if (
        "traceback" in text
        or "syntaxerror" in text
        or "nameerror" in text
        or "typeerror" in text
        or "valueerror" in text
    ):
        return "Python Error"

    # ---------- Tests ----------
    if (
        "assertionerror" in text
        or "pytest" in text
        or "test failed" in text
    ):
        return "Test Failure"

    # ---------- Kubernetes ----------
    if (
        "crashloopbackoff" in text
        or "oomkilled" in text
        or "kubectl" in text
        or "failedscheduling" in text
        or "imagepullbackoff" in text
    ):
        return "Kubernetes Error"

    return "Unknown"