<!-- Logo -->
<h1 align="center">
  <img src="https://raw.githubusercontent.com/willtheorangeguy/.github/main/icons/Auto-Anouncements/logo.png" height="250px" width="400px" alt="Auto Announcements">
  <br>
  Auto Announcements
  <br>
</h1>

<!-- Copy -->
<h4 align="center">A small script that sends an HTML announcement email through a local SMTP relay.</h4>

<!-- Badges -->
<div align="center">
  <img alt="GitHub Version" src="https://img.shields.io/github/v/release/willtheorangeguy/Auto-Anouncements?include_prereleases">
  <img alt="GitHub Issues" src="https://img.shields.io/github/issues/willtheorangeguy/Auto-Anouncements">
  <img alt="GitHub Pull Requests" src="https://img.shields.io/github/issues-pr/willtheorangeguy/Auto-Anouncements">
  <img alt="License" src="https://img.shields.io/github/license/willtheorangeguy/Auto-Anouncements">
</div>

<!-- Navigation -->
<p align="center">
  <a href="#status">Status</a> •
  <a href="#key-features">Key Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#support">Support</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>

<!-- Screenshot -->
<div align="center">
  <img alt="Auto Announcements" src="https://raw.githubusercontent.com/willtheorangeguy/.github/main/icons/Auto-Anouncements/welcome.png">
</div>

## Status

**Early, and smaller than it looks.** The whole program is 38 lines: it prompts for two email addresses, builds a fixed one-line HTML message, and hands it to an SMTP server on `localhost`.

There is **no scheduler, no file attachment, and no message-template loading** — earlier versions of this README described all three. `message.html` sits in the repository and nothing reads it. See [`docs/roadmap.md`](docs/roadmap.md) for what is intended, and [`docs/internal/known-issues.md`](docs/internal/known-issues.md) for what was documented but never built.

## Key Features

- Prompts for the sender and recipient addresses at run time.
- Sends a `text/html` message with the date in the subject line.
- Runs anywhere Python does, with no dependencies.

It requires an SMTP server listening on `localhost` — see [Installation](#installation).

## Installation

```bash
git clone https://github.com/willtheorangeguy/Auto-Anouncements
cd Auto-Anouncements
python -m send
```

**You also need a mail relay on `localhost:25`.** The SMTP host is hardcoded, with no authentication and no TLS, so this works on a machine with a configured relay and nowhere else. See [`docs/installation.md`](docs/installation.md).

## Usage

```
$ python -m send
YOUR email address: me@example.org
RECIPIENT's email address: them@example.org
Message sent successfully on 2026-08-18 …!
```

Changing the message body, or fixing the addresses so it stops asking, means editing `send/send.py` — see [`docs/configuration.md`](docs/configuration.md).

## Documentation

Full documentation lives in [`docs/`](docs/README.md):
[Quickstart](docs/quickstart.md) · [Installation](docs/installation.md) · [Configuration](docs/configuration.md) · [Architecture](docs/architecture.md) · [Development](docs/development.md) · [FAQ](docs/faq.md) · [Troubleshooting](docs/troubleshooting.md) · [Roadmap](docs/roadmap.md)

## Support

Open a [GitHub Discussion](https://github.com/willtheorangeguy/Auto-Anouncements/discussions), file an [issue](https://github.com/willtheorangeguy/Auto-Anouncements/issues/new/choose), or join the [Discord](https://discord.gg/XVBj6WGjap).

## Contributing

Please contribute using [GitHub Flow](https://guides.github.com/introduction/flow). Create a branch, add commits, and [open a pull request](https://github.com/willtheorangeguy/Auto-Anouncements/compare).

See the org-wide [Contributing Guide](https://github.com/willtheorangeguy/.github/blob/main/CONTRIBUTING.md) and [Code of Conduct](https://github.com/willtheorangeguy/.github/blob/main/CODE_OF_CONDUCT.md).

## Credits

Standard library only — `smtplib`, `email.mime`, and `datetime`.

## License

MIT — see [`LICENSE.md`](LICENSE.md).
