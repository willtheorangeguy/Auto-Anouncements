# Auto Announcements

Auto Announcements sends an email body and optional files through SMTP, immediately
or on a daily or weekly schedule. It runs on Python 3.9 or newer with no runtime
dependencies.

## Key features

- Read an HTML or plain-text announcement body from a file.
- Attach PDFs, presentations, or other files without changing their contents.
- Configure recipients, SMTP authentication, and TLS through JSON.
- Wait for a daily or weekly time in the computer's local timezone.
- Validate settings and files without sending email.

## Quick start

From the source checkout:

```bash
python -m send --config config.example.json --dry-run
```

Follow [Quickstart](quickstart.md) to configure your own SMTP account and schedule.

## Where to next

- [Installation](installation.md)
- [Usage](usage-guide.md)
- [Configuration](configuration.md)
- [Architecture](architecture.md)
- [Development guide](development.md)
- [Troubleshooting](troubleshooting.md)

## Support

Open a [GitHub issue](https://github.com/willtheorangeguy/Auto-Anouncements/issues/new/choose)
with the command, error output, and relevant settings. Remove passwords and
private announcement contents before sharing diagnostics.
