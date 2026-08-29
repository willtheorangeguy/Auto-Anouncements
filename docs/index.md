# Auto Announcements — Documentation

A 38-line script that sends an HTML announcement email through a local SMTP relay.

```text
Auto-Anouncements/
├── send/
│   ├── send.py       the whole program
│   └── __init__.py   re-exports main() for the console script
├── message.html      an HTML email body — read by nothing
├── Dockerfile
└── docs/             this documentation
```

## Pages

- [Quickstart](./quickstart.md) — run it, once you have a relay
- [Installation](./installation.md) — the SMTP requirement, and the naming mess
- [Configuration](./configuration.md) — what to edit, by symbol not line number
- [Architecture](./architecture.md) — all 38 lines of it
- [Development](./development.md) — packaging and tests
- [FAQ](./faq.md) — why it fails, what is not implemented
- [Troubleshooting](./troubleshooting.md) — connection refused, and the rest
- [Roadmap](./roadmap.md) — direction and non-goals
- [Known issues](./internal/known-issues.md) — recorded defects

## What it actually does

1. Prompts for a sender address.
2. Prompts for a recipient address.
3. Builds a `MIMEText` with the body `<h1>A Heading</h1><p>Hello There!</p>`.
4. Sets the subject to `Church Announcements for <today>`.
5. Connects to `smtplib.SMTP("localhost")` and sends.

That is the complete program.

## What earlier documentation claimed

| Claimed | Reality |
|---|---|
| "Automatically send file on a schedule or on dispatch" | No scheduler and no attachment code exists |
| "Customizable HTML email body" | The body is a hardcoded string; `message.html` is read by nothing |
| "Email addresses can be hard coded" | An editing procedure, not a feature — and its instructions cite line numbers that no longer match |

Recorded in [`internal/known-issues.md`](./internal/known-issues.md). The README now describes
what runs.

## The SMTP requirement

```python
s = smtplib.SMTP("localhost")
```

No host option, no port, no authentication, no TLS. It needs a mail relay listening on
`localhost:25` that will accept unauthenticated mail.

That is a reasonable assumption on a configured server and an unreasonable one everywhere else —
including inside the Docker image this repository ships, which contains no mail server. See
[Installation](./installation.md).
