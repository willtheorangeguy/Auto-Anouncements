# Auto Announcements — FAQ

### `ConnectionRefusedError` when I run it.

Nothing is listening on `localhost:25`. The SMTP host is hardcoded, so the program needs a local
mail relay that accepts unauthenticated mail.

There is no option to point it elsewhere — see [Configuration](./configuration.md).

### Can I use Gmail, or any real provider?

Not without editing the code. You would need a host, a port, `starttls()`, and `login()`, none of
which exist here, plus somewhere to keep the password.

### Does it schedule anything?

No. Earlier documentation said "automatically send file on a schedule or on dispatch"; there is
no scheduler in the codebase. Run it from `cron` or Task Scheduler if you want that.

### Can it attach a file?

No. Despite the wording above, there is no attachment code — the message is a single `MIMEText`.

### What is `message.html` for?

Nothing reads it. It looks like the email body from an earlier design, left behind when the body
became a hardcoded string. Recorded in
[`internal/known-issues.md`](./internal/known-issues.md).

### How do I change the message?

Edit the `MIMEText(...)` call in `send/send.py`. [Configuration](./configuration.md) shows how,
including how to make it read `message.html`.

### Why does the subject say "Church Announcements"?

A literal left over from the original use. Change it in `send/send.py`.

### `cd Auto-Announcements` fails.

The repository is `Auto-Anouncements` — one `n`. The name is misspelled and the old README
compounded it by telling you to `cd` into the correctly-spelled version.

### `python send.py` fails.

The file is `send/send.py`. Use `python -m send`.

### Which name is it on PyPI?

`auto-announcements`, per `setup.py`. `setup.cfg` says `auto-annoucements` — a different name,
missing an `n` — and the old README linked to that one. Recorded in the known-issues file.

### Does the Docker image work?

It builds and runs, and it cannot send: there is no mail server in the image and the code
connects to `localhost`. See [Installation](./installation.md).

### Are the emails sent securely?

No. Plain SMTP to `localhost`, no TLS and no authentication. That is acceptable for a relay on
the same machine and for nothing else.

### Is anything stored?

No. No log, no queue, no config. The program prompts, sends, and exits.
