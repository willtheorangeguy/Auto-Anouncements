# Auto Announcements — Development

## Setup

```bash
git clone https://github.com/willtheorangeguy/Auto-Anouncements
cd Auto-Anouncements
pip install -r requirements.txt
python -m send
```

Note the misspelled directory name — `Anouncements`, one `n`.

## Layout

| Path | Contents |
|---|---|
| `send/send.py` | The program |
| `send/__init__.py` | Re-exports `main` for the console script |
| `message.html` | An email body nothing reads |
| `tests/` | The suite |
| `Dockerfile`, `docker-compose.yml` | Container build |
| `setup.py`, `setup.cfg`, `pyproject.toml` | Three descriptions of the package |

## Testing

The sending path cannot be tested without either a live SMTP server or a patched `smtplib`.
Patching is the right answer:

```python
@patch("send.send.smtplib.SMTP")
def test_sends(self, mock_smtp):
    ...
```

That makes the whole of `main()` assertable — the subject format, the headers, the body — without
a network or a relay. It also isolates the one thing this program does.

## Packaging

Three files, three names, one of them a typo (`auto-annoucements` in `setup.cfg`). Which one is
published depends on which the build backend reads.

Consolidating on `pyproject.toml` and deleting the other two would remove both the duplication
and the chance of publishing under the wrong name. See
[`internal/known-issues.md`](./internal/known-issues.md).

## Style

- **Module docstring and copyright header** on every file.
- **Pylint**, with per-file disables at the top. Note the existing
  `# pylint: disable=global-variable-undefined` exists to silence a warning about a `global` that
  serves no purpose — removing the `global` would be better than keeping the disable.

## If you implement the documented features

The README used to promise scheduling, attachments, and a configurable body. If you build them:

- **The body** should read `message.html`, which is already in the repository and already looks
  like the intended content.
- **Configuration** should come before scheduling — a scheduler that sends a hardcoded message to
  a hardcoded address is not much use, and the SMTP host needs to be settable first.

## Recording defects

Bugs found while working here go in [`internal/known-issues.md`](./internal/known-issues.md)
rather than being fixed in passing, unless fixing them is the job you are on.
