# Development guide

## Setup

```bash
python -m pip install -r requirements.txt
python -m pip install pylint build
python -m send --config config.example.json --dry-run
```

## Style

Keep four-space indentation, double-quoted strings, snake_case functions, and
module/function docstrings. New modules carry the copyright header. Application
code uses the Python standard library and remains compatible with Python 3.9.

The core remains in `send/send.py`, split into functions for configuration,
message construction, transport, scheduling, and CLI handling. See
[Architecture](architecture.md) before changing the delivery flow.

## Validation

```bash
python -m pytest tests/ -v --cov=send --cov-report=term-missing
python -m pylint send __main__.py __init__.py setup.py
python -m build
```

The build produces a source distribution and wheel in `dist`. Packaging files
use the name `auto-announcements`; the public console entry point is `send:main`.

## Recording defects

Record unresolved implementation gaps in
[Known issues](internal/known-issues.md). Update usage and configuration
documentation when behavior changes.
