def extract_errors(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    keywords = [
        "ERROR",
        "FAILED",
        "Exception",
        "Traceback",
        "exit code"
    ]

    output = []

    for i, line in enumerate(lines):

        for keyword in keywords:

            if keyword.lower() in line.lower():

                start = max(0, i - 5)
                end = min(len(lines), i + 6)

                output.extend(lines[start:end])

                return "".join(output)

    return ""