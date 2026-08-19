# Auto Announcements — Installation

## Requirements

| | |
|---|---|
| Python | 3.x |
| Dependencies | None |
| **An SMTP relay on `localhost:25`** | Not optional — the host is hardcoded |

The last row is the one that decides whether this works for you. There is no host, port,
username, password, or TLS option anywhere in the code.

## From source

```bash
git clone https://github.com/willtheorangeguy/Auto-Anouncements
cd Auto-Anouncements
python -m send
```

The directory is `Auto-Anouncements` — the repository name is missing an `n`. Earlier
documentation said `cd Auto-Announcements` and `python send.py`; neither path exists.

## From PyPI

```bash
pip install auto-announcements
auto-announcements
```

Three packaging files declare three different names:

| File | Name |
|---|---|
| `setup.py` | `auto-announcements` |
| `pyproject.toml` | `Auto-Announcements` |
| `setup.cfg` | `auto-annoucements` |

The first two normalise to the same PyPI project. The third is a **different name** — missing an
`n` — and the old README linked to it. Recorded in
[`internal/known-issues.md`](./internal/known-issues.md).

## Docker

```bash
docker pull ghcr.io/willtheorangeguy/auto-announcements:master
docker run -i -t ghcr.io/willtheorangeguy/auto-announcements:master python -m send
```

**This will not send anything.** The image contains no mail server, and the code connects to
`localhost`. It will prompt for both addresses and then raise `ConnectionRefusedError`.

To make the container work you would need to point the SMTP host at a reachable relay, which
means editing the code — there is no environment variable for it. Same known-issues file.

## Verify

```bash
python -m send
```

If you get as far as the two prompts, the install is fine; anything after that is the relay.

## Uninstall

```bash
pip uninstall auto-announcements
```

Nothing is written to disk at any point — no config, no log, no queue.
