# Auto Announcements — Troubleshooting

## `ConnectionRefusedError: [Errno 111] Connection refused`

The most common failure. `smtplib.SMTP("localhost")` found nothing listening on port 25.

| Situation | What to do |
|---|---|
| No relay on this machine | Install one (Postfix, or your platform's equivalent) |
| Relay on another host | Edit the `smtplib.SMTP(...)` call — there is no option for it |
| Just testing | Run a debug server and point the code at its port |

```bash
pip install aiosmtpd
python -m aiosmtpd -n -l localhost:8025
# then change smtplib.SMTP("localhost") to smtplib.SMTP("localhost", 8025)
```

## It fails inside Docker

Expected. The image has no mail server, and the code connects to `localhost`. Nothing in the
containerised path can send. See [Installation](./installation.md).

## `SMTPRecipientsRefused`

The relay accepted the connection and rejected the address — a typo, or a relay configured not to
send to external domains. Check the address, then the relay's own policy.

## `python: can't open file 'send.py'`

The file is `send/send.py`. Use:

```bash
python -m send
```

## `cd: Auto-Announcements: No such file or directory`

The repository is misspelled: `Auto-Anouncements`, one `n`.

```bash
cd Auto-Anouncements
```

## `pip install Auto-Annoucements` finds nothing

Also a spelling problem, and this one is in the packaging rather than your typing:

```bash
pip install auto-announcements
```

`setup.cfg` declares the misspelled name and the old README linked to it. Recorded in
[`internal/known-issues.md`](./internal/known-issues.md).

## The email arrived with the wrong content

The body is `<h1>A Heading</h1><p>Hello There!</p>`, hardcoded in `send/send.py`. It is not read
from `message.html`, whatever that file's presence suggests. See
[Configuration](./configuration.md).

## The subject mentions a church

A leftover literal. Same file.

## It asks for addresses every time

By design — they are `input()` calls. Replacing them with literals is the documented
customisation; [Configuration](./configuration.md) names the symbols, since the old instructions
cited line numbers that no longer match.

## No error, but no email

The relay accepted it and dropped it, or delivered it somewhere unexpected. Check the relay's
logs — the script prints "Message sent successfully" as soon as `sendmail` returns, which only
means the relay took responsibility for it.

## Still stuck

[Open an issue](https://github.com/willtheorangeguy/Auto-Anouncements/issues/new/choose) or ask
on the [Discord](https://discord.gg/XVBj6WGjap), with the traceback and what mail relay you are
using.
