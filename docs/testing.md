# Testing

The pytest suite exercises `send.main()` with the input, date, and SMTP dependencies mocked.
It verifies address handling, message headers and HTML, subject dates, and the success output
without connecting to a mail server.

## Test stack

| Tool | Purpose |
|---|---|
| pytest | Discovers and runs the 13 tests in `tests/test_send.py` |
| `unittest.mock` | Replaces input, date, output, and SMTP dependencies |
| pytest-cov | Measures coverage for the `send` package in CI |

## Running the tests

Install the repository requirements, then run the same command as CI:

```bash
pip install -r requirements.txt
pytest tests/ -v --cov=send --cov-report=term-missing --cov-report=xml
```

A successful run ends with 13 passing tests and writes `coverage.xml`.

## Running one test

```bash
pytest tests/test_send.py::TestMain::test_main_successful_send -v
```

## Test layout

```text
tests/
├── __init__.py
└── test_send.py
```

## Writing tests

Patch `send.send.input`, `send.send.datetime`, and `send.send.smtplib.SMTP` before calling
`main()`. Assert against the mock SMTP server's `sendmail` arguments to inspect the generated
message without sending mail.
