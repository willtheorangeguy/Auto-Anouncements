# FAQ

???+ question "Can I send a PDF or presentation?"
    Yes. Put its path in the `attachments` list. The email body comes from
    `message_file`, independently of the attachments.

??? question "Which schedule is used?"
    The example sends on Saturday at 18:00 in the computer's local timezone.
    Set `schedule.day` to another lowercase weekday or `daily`, and set
    `schedule.time` in 24-hour format.

??? question "Will it run after I close the terminal?"
    The built-in scheduler requires a running process. Use a service or Docker
    Compose to keep it running, or use cron or Task Scheduler with `--once`.
    It does not install a service or wake the computer.

??? question "Can I use an authenticated SMTP provider?"
    Yes. Configure its host, port, `starttls` or `ssl`, username, and password
    environment variable. See [Configuration](configuration.md).

??? question "Can I test without sending?"
    Run `python -m send --config config.example.json --dry-run`. It reads the
    files and prints a summary without opening an SMTP connection.

??? question "What happens if delivery fails?"
    One-shot mode returns status 1. Scheduled mode reports the error and waits
    for the next occurrence. There are no automatic retries or stored delivery
    history.

??? question "Do I need to edit the Python code?"
    No. Edit the JSON configuration, body, and attachment files. Restart the
    scheduler after changing JSON settings.
