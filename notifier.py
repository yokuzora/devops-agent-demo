
def send_alert(category, root_cause, suggestions):

    print()

    print("=" * 60)
    # Keep terminal alerts compatible with legacy Windows encodings (for
    # example CP1252), which cannot render the original emoji safely.
    print("[ALERT] DEVOPS ALERT")
    print("=" * 60)

    print()

    print("Category:")
    print(category)

    print()

    print("Root Cause:")
    print(root_cause)

    print()

    print("Suggested Actions:")

    for item in suggestions:
        print("-", item)

    print()

    print("=" * 60)
