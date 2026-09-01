import os


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
OWNER = os.getenv("GITHUB_OWNER", "your-company-or-username")
REPOSITORY = os.getenv("GITHUB_REPOSITORY", "devops-agent-demo")

MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")
OLLAMA_PATH = os.getenv(
    "OLLAMA_PATH",
    r"C:\Users\HP\AppData\Local\Programs\Ollama\ollama.exe"
)
