import subprocess
from config import MODEL_NAME
from config import OLLAMA_PATH


def analyze(error_log):

    prompt = f"""
You are an expert Senior DevOps Engineer.

Your job is to analyze ONLY the provided GitHub Actions failure log.

STRICT RULES:
- Do NOT invent information.
- Do NOT generate YAML.
- Do NOT generate code.
- Do NOT mention technologies not present in the log.
- Do NOT guess if information is missing.
- Base your answer ONLY on the provided log.

Return EXACTLY in this format:

Root Cause:
<one sentence>

Evidence:
<copy the relevant log lines>

Suggested Actions:
- action 1
- action 2
- action 3

Confidence:
<number between 0 and 100>

GitHub Actions Log:

{error_log}
"""

    result = subprocess.run(
        [
            OLLAMA_PATH,
            "run",
            MODEL_NAME,
            prompt
        ],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )

    return result.stdout


if __name__ == "__main__":

    sample_log = """
ERROR: Could not find a version that satisfies the requirement pandas==99.0
ERROR: No matching distribution found
Build Failed
Process completed with exit code 1
"""

    print(analyze(sample_log))  
