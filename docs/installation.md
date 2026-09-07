# Installation

## Requirements

Python 3.9 or newer runs the application with no runtime dependencies. Delivery
requires access to an SMTP relay or provider. Configure its host, port, transport,
and credentials in [Configuration](configuration.md).

## Install from source

```bash
git clone https://github.com/willtheorangeguy/Auto-Anouncements
cd Auto-Anouncements
python -m pip install .
```

The installation adds the `auto-announcements` command. Keep your configuration,
message body, and attachments outside the installed package. The source checkout
includes `config.example.json` and `message.html`.

## Docker

Create a `data` directory containing `config.json`, `message.html`, and any
attachments. Use paths relative to that configuration. Set an SMTP host reachable
from the container: `localhost` means the container itself.

Set `AUTO_ANNOUNCEMENTS_PASSWORD` in the host environment for authenticated SMTP.
Set `TZ` to your timezone, for example `America/Edmonton`; Compose defaults to UTC.

```bash
docker compose up --build -d
docker compose logs -f
```

The service runs the scheduler and mounts `data` read-only.

```bash
docker compose down
```

## Verify the installation

From the source checkout:

```bash
auto-announcements --config config.example.json --dry-run
```

The output lists the subject, example recipient, zero attachments, and next
scheduled time. No email is submitted.

## Upgrading

Update your checkout and reinstall:

```bash
git pull
python -m pip install --upgrade .
```

## Uninstalling

```bash
python -m pip uninstall auto-announcements
```

Your configuration and announcement files remain in their original locations.
