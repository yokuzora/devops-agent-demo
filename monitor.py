import os
import time

from agent import investigate

WATCH_FOLDER = "logs"

processed = set()

print("=" * 50)
print("DEVOPS AGENT MONITOR")
print("=" * 50)
print("Watching logs folder...\n")

while True:

    files = os.listdir(WATCH_FOLDER)

    for file in files:

        if file.endswith(".log") and file not in processed:

            path = os.path.join(
                WATCH_FOLDER,
                file
            )

            print(f"New Log: {file}")

            investigate(path)

            processed.add(file)

    time.sleep(5)