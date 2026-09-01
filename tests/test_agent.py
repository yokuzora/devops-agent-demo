import os

import pytest

from analyzer import analyze
from config import OLLAMA_PATH
from parser import extract_errors


def test_agent_analysis_with_ollama():

    if os.getenv("RUN_OLLAMA_TESTS") != "1":

        pytest.skip("Set RUN_OLLAMA_TESTS=1 to run Ollama integration tests.")

    if not os.path.exists(OLLAMA_PATH):

        pytest.skip("Ollama executable is not configured.")

    errors = extract_errors("samples/github_failure.log")
    response = analyze(errors)

    assert response.strip()
