def calculate_confidence(error_log):

    score = 50

    keywords = [
        "ERROR",
        "FAILED",
        "Exception",
        "Traceback",
        "No matching distribution found",
        "permission denied",
        "ModuleNotFoundError",
        "exit code"
    ]

    for keyword in keywords:

        if keyword.lower() in error_log.lower():
            score += 10

    if score > 100:
        score = 100

    return score