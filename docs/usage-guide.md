# Usage

Run a configured announcement immediately, validate it, or keep the scheduler running.

| Flag | Type | Default | Description |
| --- | --- | --- | --- |
| `--config` | path | none | Load JSON settings; e.g. `config.json` |
| `--once` | flag | on | Submit one email and exit |
| `--dry-run` | flag | off | Read files and show a summary without contacting SMTP |
| `--schedule` | flag | off | Wait for the next configured daily or weekly time |
| `--help` | flag | off | Show command help |

## Validate and send once

```bash
python -m send --config config.example.json --dry-run
python -m send --help
```

After preparing your own configuration:

```bash
python -m send --config config.json --once
```

The root script and installed console command accept the same flags:

```bash
python __main__.py --config config.example.json --dry-run
auto-announcements --config config.example.json --dry-run
```

Without a configuration, `python -m send` prompts for addresses, reads
`message.html` in the current directory, and submits to `localhost:25`.

## Recurring delivery

```bash
python -m send --config config.json --schedule
```

Times follow the computer's local clock, including daylight saving changes.
The process waits for the next occurrence strictly after startup. It does not send
immediately, install a background service, or wake a sleeping computer.

The body and attachments are reread before every delivery, so you can replace the
files between runs. Restart the process after changing JSON settings.

A running process that resumes after a missed time attempts one delivery and
advances to the next future occurrence. It does not send a backlog. During a
spring clock change, a skipped time runs when the clock next passes it. During a
fall clock change, a completed daily slot is not repeated by that process.

No delivery history is stored. Run one scheduler per configuration. Restarting the
program schedules the next future occurrence and does not recover missed runs.

## Errors and stopping

Ctrl+C stops cleanly. One-shot file, configuration, or SMTP failures return exit
status 1. Invalid CLI arguments return status 2. Scheduled delivery failures print
to stderr and the process continues with the next scheduled occurrence.

Failed submissions are not retried automatically: a relay may have accepted mail
before a connection failed, or accepted only some recipients. Inspect the relay's
delivery log before deciding to send again. SMTP acceptance does not guarantee
inbox delivery.

## External schedulers

For cron or Windows Task Scheduler, invoke the one-shot command with an absolute
configuration path and arrange for the password environment variable to be
available. Use the built-in `--schedule` mode only when you intend to keep the
process running.
