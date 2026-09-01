import os
from agent import investigate

folder = "samples"

for file in os.listdir(folder):

    if file.endswith(".log"):

        print("\n" + "="*70)
        print(file)
        print("="*70)

        investigate(
            os.path.join(folder, file)
        )