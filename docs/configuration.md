# Configuration

## Precedence

Command-line flags select the configuration and run mode. JSON settings override
built-in defaults. The password comes only from the environment variable named by
`smtp.password_env`; other environment variables do not override JSON settings.
Unknown options, invalid values, and missing files are fatal at startup.

File paths are relative to the configuration file's directory, including when you
launch from another directory. Without `--config`, the script prompts for two
addresses and reads `message.html` from the current directory using a local relay.

## Configuration file

Copy `config.example.json` to `config.json`, then edit the copy. Local
`config.json` files are ignored by Git.

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `sender` | string | required | One bare ASCII address, e.g. `announcements@example.org` |
| `recipients` | list | required | Bare addresses, e.g. `["recipient@example.org"]` |
| `subject` | string | `Church Announcements for {date}` | Replaces `{date}` with the local send date |
| `message_file` | path | `message.html` | UTF-8 body; `.html` and `.htm` produce HTML, other extensions produce plain text |
| `attachments` | list | `[]` | Files to attach, e.g. `["announcements.pdf"]`; binary contents are preserved |
| `smtp.host` | string | `localhost` | Relay hostname, e.g. `smtp.example.org` |
| `smtp.port` | integer | `25` | Explicit port from 1 to 65535; e.g. `587` for STARTTLS or `465` for SSL |
| `smtp.security` | string | `none` | One of `none`, `starttls`, `ssl`; TLS verifies certificates |
| `smtp.username` | string | `""` | Login name, e.g. `announcements@example.org`; empty disables authentication |
| `smtp.password_env` | string | `AUTO_ANNOUNCEMENTS_PASSWORD` | Name of the environment variable containing the SMTP password |
| `smtp.timeout` | integer | `30` | Positive connection/socket timeout in seconds |
| `schedule.day` | string | `saturday` | `daily`, `monday`, `tuesday`, `wednesday`, `thursday`, `friday`, `saturday`, or `sunday` |
| `schedule.time` | string | `18:00` | Computer local time in 24-hour `HH:MM` format |

Authentication requires `starttls` or `ssl`. Set the port explicitly to match your
provider. The dry run validates the message and files without requiring a password
or opening an SMTP connection.

## Environment variables

| Option                        | Type   | Default | Description                                                                 |
| ----------------------------- | ------ | ------- | --------------------------------------------------------------------------- |
| `AUTO_ANNOUNCEMENTS_PASSWORD` | string | unset   | SMTP password, e.g. `your-app-password`; rename through `smtp.password_env` |

The script does not load `.env` files. Docker Compose passes
`AUTO_ANNOUNCEMENTS_PASSWORD` into the container and uses `TZ` for the container
timezone, defaulting to `UTC`. For a renamed password variable, update Compose too.

## Command-line flags

| Flag | Type | Default | Description |
| --- | --- | --- | --- |
| `--config` | path | none | JSON file, e.g. `config.json` |
| `--once` | flag | on | Send immediately and exit |
| `--schedule` | flag | off | Wait for recurring delivery; requires `--config` |
| `--dry-run` | flag | off | Validate files and show recipients, attachment count, and next time |
| `--help` | flag | off | Print usage |

The three run modes are mutually exclusive.

## Examples

The repository example uses authenticated STARTTLS and Saturday at 18:00:

```bash
python -m send --config config.example.json --dry-run
```

For a local unauthenticated relay, a complete configuration is:

```json title="config.json"
{
    "sender": "sender@example.org",
    "recipients": ["recipient@example.org"],
    "message_file": "message.html",
    "attachments": [],
    "smtp": {"host": "localhost", "port": 25, "security": "none"},
    "schedule": {"day": "daily", "time": "09:00"}
}
```

Send once or start the scheduler after configuring your addresses and relay:

```bash
python -m send --config config.json --once
python -m send --config config.json --schedule
```

```bash
python -m send --help
```
