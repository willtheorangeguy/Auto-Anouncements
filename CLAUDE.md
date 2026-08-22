# CLAUDE.md

## Project Overview

Auto Announcements is a Python bot framework that automatically sends HTML email announcements to a specified email address via SMTP. Originally designed for church announcements, it can be customized for any recurring email use case.

## Repository Structure

```
__main__.py          # Entry point, imports and calls send.send.main()
send/send.py         # Core logic: prompts for email addresses, builds MIMEText, sends via SMTP
message.html         # Sample HTML email template (Microsoft Word-generated)
setup.py             # Legacy setuptools config
pyproject.toml       # Modern build config (setuptools backend)
requirements.txt     # Dev/test dependencies only (pytest, pytest-mock, pytest-cov)
Dockerfile           # Container build
docker-compose.yml   # Container orchestration
tests/test_send.py   # Pytest suite for send module
```

## Development

### Prerequisites

- Python >= 3.9

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
python __main__.py
```

The app prompts interactively for sender and recipient email addresses, then sends an HTML email via `localhost` SMTP.

### Run tests

```bash
pytest tests/ -v --cov=send --cov-report=term-missing
```

All tests mock SMTP and user input — no network or mail server needed.

### Lint

```bash
pylint $(git ls-files '*.py' ':!tests/**')
```

Pylint runs on all Python files except tests. The codebase uses `pylint: disable` comments for `invalid-name`, `import-error`, and `global-variable-undefined`.

## CI/CD

- **Pytest**: Runs on push and PR, Python 3.9-3.12
- **Pylint**: Runs on push, Python 3.9 only, excludes `tests/`
- **CodeQL**: Security analysis
- **Docker publish**: Builds and publishes container image
- **PyPI publish**: Publishes package to PyPI

## Key Conventions

- Package name: `auto-announcements` (with hyphen), version `0.2.0`
- Single module structure: `send/send.py` contains all logic in one `main()` function
- SMTP connects to `localhost` — no authentication configured
- Email body is hardcoded HTML in `send.py`; `message.html` is a reference template not loaded at runtime
- No runtime dependencies beyond the Python standard library
- Test dependencies are in `requirements.txt` (not in `pyproject.toml`)
- License: MIT
