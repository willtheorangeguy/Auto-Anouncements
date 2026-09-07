# Known issues

## Current limitations

- The scheduler uses the computer's local timezone. Set the operating system
  timezone, or `TZ` in Compose, before starting it.
- Delivery history is not persisted. Keep one scheduler process per configuration.
- There is no automatic retry policy. A failed connection can occur after SMTP
  acceptance, and partial recipient refusal can coexist with successful delivery.
- Configuration is loaded at startup. Restart after changing settings.
- Packaged installations require user-supplied message and configuration files.
  The source checkout provides examples.

See [Usage](../usage-guide.md) for scheduling and failure behavior.

## Resolved implementation gaps

The earlier audit's missing scheduler, attachment handling, template loading,
SMTP configuration, package-name mismatch, and global message variable have been
addressed. The module entry point and container command now invoke the same CLI.
