# Roadmap

## Implemented

Auto Announcements loads message files, sends attachments, accepts JSON
configuration, supports authenticated SMTP with TLS, and runs daily or weekly
schedules. Script, module, and installed console entry points share the same CLI.

```bash
python -m send --config config.example.json --dry-run
```

## Future work

Persistent delivery history, explicit per-schedule timezones, and retry policies
remain possible extensions. Current limitations are documented in
[Known issues](internal/known-issues.md) and [Usage](usage-guide.md).

## Non-goals

The application does not provide a mail server or mailing-list management.
