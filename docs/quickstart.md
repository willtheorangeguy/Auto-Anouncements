# Quickstart

You need Python 3.9 or newer. SMTP access is required for delivery, but you can
validate the example without an account or network connection.

## Install

```bash
git clone https://github.com/willtheorangeguy/Auto-Anouncements
cd Auto-Anouncements
python -m send --config config.example.json --dry-run
```

The output starts with `Ready:` and lists the example recipient, attachment count,
and next Saturday at 18:00 in your computer's local timezone.

## Configure your announcement

Copy `config.example.json` to `config.json`. Set your sender, recipients, and SMTP
provider settings. Edit `message.html` with your announcement body. To send a PDF
or another file, put its path in `attachments`, for example
`["announcements.pdf"]`. Paths are relative to the configuration file.

Set the password in the environment when using authenticated SMTP:

<!-- markdownlint-disable MD046 -->

=== "Windows"

    ```powershell
    $env:AUTO_ANNOUNCEMENTS_PASSWORD = "your-app-password"
    ```

=== "macOS / Linux"

    ```bash
    export AUTO_ANNOUNCEMENTS_PASSWORD='your-app-password'
    ```

<!-- markdownlint-enable MD046 -->

Use the credentials and transport settings supplied by your email provider.

## Validate and send

```bash
python -m send --config config.json --dry-run
python -m send --config config.json --once
```

Successful submission prints `Message accepted by SMTP server on` followed by the
time. The relay still controls final inbox delivery.

## Start the schedule

```bash
python -m send --config config.json --schedule
```

The script waits for the next Saturday at 18:00 and repeats weekly. Keep the
process running and the computer awake. Press Ctrl+C to stop it. See
[Usage](usage-guide.md) for restart, sleep, and failure behavior, and
[Configuration](configuration.md) for daily schedules and other settings.
