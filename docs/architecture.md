# Auto Announcements — Architecture

One function, thirty-eight lines.

```
main()
 ├── input()  × 2          sender and recipient
 ├── datetime.today()      for the subject and the log line
 ├── MIMEText(html)        a hardcoded body
 ├── msg["Subject"|"From"|"To"]
 └── smtplib.SMTP("localhost").sendmail(...)
```

## `send/send.py`

The entire program. It prompts, builds a `MIMEText` with subtype `html`, sets three headers, and
calls `sendmail`.

Two details worth naming:

**`global msg`** — `msg` is declared global for no reason; it is used only within `main()`. The
file carries `# pylint: disable=global-variable-undefined` to silence the resulting warning,
which is the wrong way round: the disable comment is treating the symptom.

**No error handling.** `smtplib.SMTP("localhost")` raises `ConnectionRefusedError` when nothing
is listening, and `sendmail` raises on a rejected recipient. Neither is caught, so the failure is
a traceback. For a script this size that is defensible; for one whose most likely failure is a
missing relay, a caught exception with a sentence of explanation would be worth more than the
stack trace.

## `send/__init__.py`

```python
from send.send import main
__all__ = ["main"]
```

Seven lines, and it is what makes the console script work: `setup.py` declares
`auto-announcements=send:main`, which resolves through this re-export rather than needing
`send.send:main`.

## `message.html`

57 lines of HTML exported from Microsoft Word, with a copyright header. **Nothing imports or
reads it** — verified by grep across the repository.

Given the README's claim of a "customizable HTML email body", this looks like the body a
previous version loaded, left behind when the message became a hardcoded string. See
[`internal/known-issues.md`](./internal/known-issues.md).

## What is absent

No scheduler, no attachment handling, no template loading, no configuration, no argument parsing,
no logging, and no tests of the sending path.

The `tests/` directory and the `docs/` tree, the Dockerfile, the three packaging files, the
changelog and the planning document together outweigh the program by a wide margin. That is worth
knowing before reading the repository top-down and expecting to find a system.

## Packaging

`setup.py`, `setup.cfg`, and `pyproject.toml` all describe the package, all at version `0.2.0`,
and all under **different names** — including one with a typo. See [Installation](./installation.md).

## Docker

The `Dockerfile` and `docker-compose.yml` build and run the script. Neither provides a mail
server, and the code connects to `localhost`, so the containerised path cannot send.
