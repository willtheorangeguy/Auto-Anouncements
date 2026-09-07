# CLAUDE.md

## Project overview

Auto Announcements is a Python script that sends an HTML or plain-text email body
and optional attachments through SMTP, immediately or on a daily/weekly schedule.

## Repository structure

```text
__main__.py             Root script entry point
send/__main__.py        python -m send entry point
send/send.py            Configuration, message building, SMTP, scheduling, CLI
config.example.json     Example JSON configuration
message.html            Editable sample HTML body
tests/test_send.py      Mocked transport and scheduler tests
pyproject.toml          Build metadata and console entry point
setup.py, setup.cfg    Legacy packaging compatibility
Dockerfile             Container build
docker-compose.yml     Scheduler service with mounted data directory
```

## Development

Python >= 3.9 is required. Runtime dependencies are all in the standard library.

```bash
python -m pip install -r requirements.txt
python -m send --config config.example.json --dry-run
python -m pytest tests/ -v --cov=send --cov-report=term-missing
```

Unit tests mock SMTP and waiting. The CLI integration test uses a loopback SMTP
sink that never relays messages. Do not deliver external email during validation.

```bash
python -m pip install pylint build
python -m pylint send __main__.py __init__.py setup.py
python -m build
```

## Conventions

- Four-space indentation, double-quoted strings, snake_case functions, docstrings.
- Module docstring and copyright header on application modules.
- Keep the application logic in `send/send.py`, with focused helper functions.
- Package and console command: `auto-announcements`, version `0.2.0`.
- Keep SMTP passwords in environment variables, never JSON or source control.
- Configuration paths resolve relative to the JSON file.
- The scheduler uses the computer's local time and does not persist delivery history.
- Read `docs/docs.instructions.md` before editing documentation.
- License: MIT.
