import os
import subprocess

import pytest

from config import MODEL_NAME
from config import OLLAMA_PATH


def test_ollama_responds():

    if os.getenv("RUN_OLLAMA_TESTS") != "1":

        pytest.skip("Set RUN_OLLAMA_TESTS=1 to run Ollama integration tests.")

    if not os.path.exists(OLLAMA_PATH):

        pytest.skip("Ollama executable is not configured.")

    result = subprocess.run(
        [OLLAMA_PATH, "run", MODEL_NAME, "What is DevOps?"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=60
    )

    assert result.returncode == 0
    assert result.stdout.strip()
