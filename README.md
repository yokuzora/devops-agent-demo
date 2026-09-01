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
```

## Environment

```powershell
$env:GITHUB_TOKEN="your_github_token"
$env:GITHUB_OWNER="your-github-user-or-org"
$env:GITHUB_REPOSITORY="your-repository"
$env:OLLAMA_MODEL="qwen2.5:1.5b"
```

`GITHUB_TOKEN` is required only for GitHub sync.

## Run Dashboard

```powershell
streamlit run dashboard.py
```

The dashboard loads local SQLite data first for fast rendering. Use the sidebar
button to sync GitHub on demand, or enable auto-sync.

## Notes About Deployment

This project is a Streamlit app. Vercel's Python runtime is designed for Python
Functions such as FastAPI or Flask handlers, while Streamlit runs as a persistent
Python server. For the dashboard itself, Streamlit Community Cloud, Render,
Railway, or another service that supports long-running Python web processes is a
better fit.

Vercel can host a separate API or static frontend for this project, but deploying
the current Streamlit dashboard directly to Vercel is not recommended.
