# Auto Announcements — Roadmap

Direction, not a schedule. Defects are in
[`internal/known-issues.md`](./internal/known-issues.md); `PLANNING.md` holds the version
checklist.

## Where it is

Thirty-eight lines that prompt for two addresses and send one hardcoded HTML message through a
local relay. That is the whole program.

## Considered

**Configurable SMTP.** The single change that would make this usable anywhere but a machine with
its own relay: host, port, TLS, and credentials. Everything else on this list is less useful
until it exists.

**Reading `message.html`.** The file is already in the repository and already looks like the
intended body. Four lines of code.

**Configuration at all.** Addresses, subject, and body are literals; editing source is currently
the only way to change them. A config file or a few CLI flags would replace the whole
"customization" procedure.

**Attachments and scheduling.** Both were described in earlier documentation and neither exists.
They belong after configuration — a scheduler that sends a fixed message to a fixed address from
a fixed relay is not much of a feature.

**One package name.** Three files, three names, one typo.

**A test of the sending path**, with `smtplib.SMTP` patched.

## Non-goals

**Becoming a mailing-list manager.** Subscriber lists, bounce handling, and unsubscribe links are
a different product, and a much more serious one — sending bulk mail badly has consequences for
the sending domain.

**Bundling an SMTP server.** Relaying is the operating system's or the provider's job. The right
fix is to let the user point at theirs.

**Storing credentials.** If authentication is added, the password should come from the
environment or a keyring, not from a file in the repository.

**Rich templating.** A template engine for one message is more machinery than the problem needs;
reading an HTML file is enough.

## Contributing

Issues and pull requests welcome — see the
[Contributing Guide](https://github.com/willtheorangeguy/.github/blob/main/CONTRIBUTING.md) or
the [Discord](https://discord.gg/XVBj6WGjap).

Making the SMTP host configurable is the smallest change that most widens where this can run.
