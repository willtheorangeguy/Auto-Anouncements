# Troubleshooting

## Connection refused or timeout

Check `smtp.host`, `smtp.port`, and whether the relay is reachable. The default
`localhost:25` requires a local relay. For Docker, use a relay reachable from the
container. Configuration does not create a mail server.

## Set the password environment variable

Set the environment variable named by `smtp.password_env` before starting the
script. The default is `AUTO_ANNOUNCEMENTS_PASSWORD`. An interactive shell's
variables may not be available to cron, Task Scheduler, or a service.

## Authentication or certificate failure

Match the host, port, and `security` to your provider's settings. Authentication
requires `starttls` or `ssl`. Use your provider's SMTP credentials or app password.
Certificate validation stays enabled.

## Missing body or attachment

Paths are relative to the JSON configuration file. Check spelling, permissions,
and that every configured file exists. Validate without submitting email:

```bash
python -m send --config config.json --dry-run
```

## The scheduler has not sent

Check the printed next occurrence and the computer's local timezone. Scheduled
mode waits until the next future occurrence. It must remain running, and it
cannot send while the computer is asleep. Compose defaults to UTC unless `TZ`
is set.

## Recipient refused or no inbox delivery

A relay can refuse some recipients while accepting others. The script reports
partial refusal as a failure and does not retry automatically. Check the relay's
logs before resending. A success message means SMTP acceptance, not inbox delivery.

## The body has not changed

Confirm `message_file` points at the file you edited. File contents are reread
at delivery time. Changes to configuration values require a process restart.
