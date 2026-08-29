# Auto Announcements — Quickstart

## You need a local mail relay first

```python
s = smtplib.SMTP("localhost")
```

The SMTP host is hardcoded. Without something listening on `localhost:25` and willing to accept
unauthenticated mail, the program raises `ConnectionRefusedError` at the last line.

To try it without a real relay, Python's built-in debugging server prints messages instead of
sending them:

```bash
python -m aiosmtpd -n -l localhost:8025    # note: port 8025, not 25
```

That needs `pip install aiosmtpd`, and you would still have to edit the port in `send/send.py` —
there is no flag for it.

## Run it

```bash
git clone https://github.com/willtheorangeguy/Auto-Anouncements
cd Auto-Anouncements
python -m send
```

Note the directory is `Auto-Anouncements` — one `n` in "Anouncements". The repository name is
misspelled, and earlier documentation told you to `cd Auto-Announcements`, which does not exist.

```text
YOUR email address: me@example.org
RECIPIENT's email address: them@example.org
2026-08-18 14:02:11.123456
Message sent successfully on 2026-08-18 14:02:11.123456 !
```

## What arrives

| Field | Value |
|---|---|
| Subject | `Church Announcements for 2026-08-18` |
| From | Whatever you typed |
| To | Whatever you typed |
| Body | `<h1>A Heading</h1><p>Hello There!</p>` |

The subject prefix and the body are literals in `send/send.py`. `message.html` in the repository
root looks like the intended body and is not read by anything.

## Changing any of that

Edit `send/send.py` — see [Configuration](./configuration.md), which names each string by symbol
rather than by line number.

## Installed as a command

```bash
pip install auto-announcements
auto-announcements
```

The console script resolves through `send/__init__.py`, which re-exports `main`. Note the three
packaging files disagree about the project's name — see
[`internal/known-issues.md`](./internal/known-issues.md).
