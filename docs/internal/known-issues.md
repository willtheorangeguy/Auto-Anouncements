# Known Issues — Auto-Anouncements

Concrete defects and gaps found while writing this repository's documentation in
August 2026. **Nothing here was changed** — each one needs a code, configuration, or
licensing decision rather than a documentation one.

Ordered by severity. See [`docs/roadmap.md`](../roadmap.md) for the narrative version,
which also covers deliberate non-goals.


**5 open:** 2 high, 2 medium, 1 low.

## 1. The README described three features that do not exist

**Severity:** High  
**Where:** `README.md` (replaced in this pass), `send/send.py`, `message.html`

**What:** The Key Features list read: 'Automatically send file on a schedule or on dispatch', 'Customizable HTML email body', and 'Email addresses can be hard coded'. `send/send.py` is 38 lines containing no scheduler, no attachment handling, and no template loading -- the body is the literal string `<h1>A Heading</h1><p>Hello There!</p>`, and the addresses are `input()` prompts. The third item describes an editing procedure documented in `docs/CUSTOMIZATION.md`, whose instructions cite line numbers (8, 9, 10, 11) that no longer match the file.

**Why it matters:** Every headline claim about what the program does was false, and the gap is not marginal -- scheduling and attachments are the two things that would make an announcement mailer useful, and neither exists in any form. Someone evaluating this for a real job reads six bullet points, sees a Docker image and three packaging files, and reasonably concludes there is a system here. There are 38 lines. The supporting material -- changelog, planning document, container build, docs tree -- outweighs the program by a wide margin, which makes the overstatement harder to catch rather than easier.

**Suggested fix:** Replaced in this pass: the README now opens with a Status section stating what runs and what does not, and the feature list describes the actual behaviour. If the features are built, `docs/roadmap.md` argues configuration should come first -- a scheduler sending a fixed message to a fixed address from a fixed relay is not much of a feature.

## 2. Three packaging files declare three names, one of them misspelled

**Severity:** High  
**Where:** `setup.py`, `setup.cfg`, `pyproject.toml`, `README.md` (corrected in this pass)

**What:** `setup.py` declares `name="auto-announcements"`; `pyproject.toml` declares `name = "Auto-Announcements"`; `setup.cfg` declares `name = auto-annoucements` -- missing an `n`. The first two normalise to the same PyPI project. The third does not: it is a different distribution name. The old README's install link pointed at `pypi.org/project/Auto-Annoucements/`, the misspelled one, while its install command said `pip install auto-announcements`.

**Why it matters:** Which name a build publishes under depends on which file the backend reads, and that has changed with setuptools versions before. Publishing under `auto-annoucements` would put the package somewhere nobody following the install command can find it -- and squat a typo-adjacent name on PyPI, which is its own small problem. The README pointing at the misspelling while instructing the correct one meant that whichever the reader followed, one of the two was wrong.

**Suggested fix:** Consolidate on `pyproject.toml`, delete `setup.py` and `setup.cfg`, and settle on `auto-announcements`. The repository name itself is also misspelled (`Auto-Anouncements`), which is worth leaving alone -- renaming a repository breaks existing clones and links for a cosmetic gain.

## 3. SMTP is hardcoded to localhost, so the shipped Docker image cannot send

**Severity:** Medium  
**Where:** `send/send.py` -> `smtplib.SMTP("localhost")`, `Dockerfile`, `docker-compose.yml`

**What:** The SMTP host is the literal `"localhost"`, with no port, no `starttls()`, no `login()`, and no way to override any of it -- `main()` takes no parameters and there is no argument parsing in the program. The repository ships a `Dockerfile` and a `docker-compose.yml`, and the old README documented `docker run ... python send.py` as one of three supported installation routes.

**Why it matters:** A container has no mail server, so the documented Docker path prompts for both addresses and then raises `ConnectionRefusedError` at the final line -- it cannot work, and there is no configuration that would make it work short of editing the source and rebuilding. The same applies to any machine without its own relay, which is most of them. The failure is a bare traceback, since nothing catches it, so it reads as a broken program rather than a missing prerequisite.

**Suggested fix:** Take the host and port from environment variables or CLI flags, defaulting to `localhost` so existing behaviour is unchanged. Add `starttls()` and `login()` behind optional settings, and catch `ConnectionRefusedError` to print a sentence naming the relay requirement.

## 4. message.html is read by nothing

**Severity:** Medium  
**Where:** `message.html`, `send/send.py`

**What:** 57 lines of Word-exported HTML with the project's copyright header, sitting in the repository root. Grep across the repository finds no reference to it from any Python file, packaging file, or `MANIFEST`. The email body is instead the inline literal `MIMEText("<h1>A Heading</h1><p>Hello There!</p>", "html")`.

**Why it matters:** It is exactly what the README's 'customizable HTML email body' claim describes, and it appears to be the body a previous version loaded. Its presence is actively misleading: someone customising the message edits `message.html`, sends a test, and receives 'A Heading / Hello There!' with no indication why. The file looks maintained -- it carries the copyright header every other file has.

**Suggested fix:** Read it: four lines in `main()`, resolved against the module rather than the working directory, and packaged via `MANIFEST.in`. If the inline string is preferred, delete `message.html` so it stops implying otherwise.

## 5. msg is declared global for no reason, and a pylint disable hides it

**Severity:** Low  
**Where:** `send/send.py`

**What:** `main()` begins with `global msg`, and `msg` is used only inside that function. The file carries `# pylint: disable=global-variable-undefined` at the top, which exists to silence the warning the `global` statement produces.

**Why it matters:** The disable comment treats the symptom rather than the cause, and it is file-wide -- so it also suppresses the same warning for any genuine mistake added later. In a 38-line program the cost is small; the habit is what matters, since a per-file disable for a problem that is one deleted word away sets the wrong precedent for the rest of the repository.

**Suggested fix:** Delete the `global msg` line and the disable comment together. `msg` becomes an ordinary local and nothing else changes.


---

## Also, across every repository

**`.bandit` is present on disk but untracked in git.** Verified in PyWorkout, treklogger,
skyscanner-cli, booking-cli, piggy, and aibot — the config file exists locally in each but
`git ls-files` does not know about it, so none of it reached GitHub.

The August 2026 security sweep therefore looks complete locally and landed nowhere. Worth
checking across all 44 repositories it covered.
