# Testing

Tests cover configuration validation, MIME contents and attachments, TLS and SMTP
failures, and daily and weekly scheduling. Unit tests mock SMTP and waiting.
An integration test submits to a loopback SMTP sink that stores messages in memory
and never relays them. No test delivers external email or waits for a schedule.

## Running the tests

```bash
python -m pip install -r requirements.txt
python -m pytest tests/ -v --cov=send --cov-report=term-missing --cov-report=xml
```

A successful run returns zero and writes `coverage.xml`.

## Running one test

```bash
python -m pytest tests/test_send.py::TestDelivery::test_main_successful_send -v
```

## Writing tests

Use temporary files for the body, attachments, and JSON configuration. Patch
`send.send.smtplib.SMTP` or `SMTP_SSL`, then inspect the `EmailMessage` passed to
the context-managed server's `send_message()`. Pass an explicit argument list to
`main()` so pytest arguments are not parsed by the application.

Calendar tests pass a fixed datetime to `next_run()`. Loop tests mock the clock,
sleep, and delivery function to verify that sending happens only when due.
