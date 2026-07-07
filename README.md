# DevOps Agent Demo

This repository is intentionally designed to generate realistic GitHub Actions failure logs for DevOps investigation and root cause analysis.

## Failure scenarios

- `dependency_error.yml`
  - Installs dependencies from `requirements.txt`
  - `requirements.txt` contains an invalid package version (`pandas==99.0`)
  - Expected failure: pip install exits with a dependency resolution/install error

- `docker_error.yml`
  - Builds a Docker image from `Dockerfile`
  - `Dockerfile` references a non-existent base image (`ubuntu:latest123`)
  - Expected failure: docker build fails while pulling the base image

- `python_error.yml`
  - Runs `app.py`
  - `app.py` imports a module that does not exist (`missing_library`)
  - Expected failure: Python raises `ModuleNotFoundError`

- `permission_error.yml`
  - Requires the `DEMO_SECRET` GitHub secret
  - `DEMO_SECRET` is intentionally missing
  - Expected failure: workflow exits with an error because the required secret is not set

- `test_failure.yml`
  - Installs `pytest`
  - Writes a simple failing test at runtime
  - Expected failure: `pytest` runs and reports a failing assertion

## Notes

- This repository is intentionally simple and educational.
- None of the workflows are meant to succeed.
- The logs produced by these workflows are intended for an AI DevOps Investigation Agent.
