# DevOps Investigation Agent

A local DevOps failure investigation tool for GitHub Actions logs.

## What It Does

- Fetches failed GitHub Actions workflow logs.
- Extracts relevant error blocks.
- Categorizes failures.
- Matches known errors from a SQLite-backed knowledge base.
- Falls back to local Ollama analysis for unknown failures.
- Saves incident history in SQLite.
- Tracks incident lifecycle as `Open` or `Resolved`.
- Displays incidents, mitigation, charts, and GitHub workflow links in Streamlit.

## Setup

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt