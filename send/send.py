"""
Auto Announcements - A bot framework that automatically sends announcements.
Copyright (C) 2017-2026 willtheorangeguy
"""

import argparse
import datetime
from email.message import EmailMessage
from email.utils import formatdate, make_msgid, parseaddr
import json
import mimetypes
import os
from pathlib import Path
import smtplib
import ssl
import sys
import time


DAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
DEFAULTS = {
    "sender": "",
    "recipients": [],
    "subject": "Church Announcements for {date}",
    "message_file": "message.html",
    "attachments": [],
    "smtp": {
        "host": "localhost", "port": 25, "security": "none",
        "username": "", "password_env": "AUTO_ANNOUNCEMENTS_PASSWORD", "timeout": 30,
    },
    "schedule": {"day": "saturday", "time": "18:00"},
}


def check_keys(values, defaults, section):
    """Reject misspelled options instead of silently using defaults."""
    if not isinstance(values, dict):
        raise ValueError(section + " must be a JSON object")
    unknown = values.keys() - defaults.keys()
    if unknown:
        raise ValueError(section + " has unknown options: " + ", ".join(sorted(unknown)))


def check_text(value, name, allow_empty=False):
    """Validate a single-line setting before using it in an email or connection."""
    if not isinstance(value, str) or "\n" in value or "\r" in value:
        raise ValueError(name + " must be a single-line string")
    if not allow_empty and not value.strip():
        raise ValueError(name + " must not be empty")


def check_address(value):
    """Require one bare email address per sender or recipient setting."""
    check_text(value, "email address")
    if parseaddr(value)[1] != value or value.count("@") != 1:
        raise ValueError("Invalid email address: " + value)
    if any(char.isspace() for char in value) or not all(value.split("@")):
        raise ValueError("Invalid email address: " + value)
    if not value.isascii():
        raise ValueError("Use ASCII email addresses (including the domain)")


def validate_config(config):
    """Validate mail, SMTP, and schedule options before opening a connection."""
    check_address(config["sender"])
    recipients = config["recipients"]
    if not isinstance(recipients, list) or not recipients:
        raise ValueError("recipients must be a non-empty list of email addresses")
    for address in recipients:
        check_address(address)
    check_text(config["subject"], "subject")
    check_text(config["message_file"], "message_file")
    if not isinstance(config["attachments"], list):
        raise ValueError("attachments must be a list of file paths")
    for filename in config["attachments"]:
        check_text(filename, "attachment")
    validate_smtp(config["smtp"])
    schedule = config["schedule"]
    if schedule["day"] not in (*DAYS, "daily"):
        raise ValueError("schedule.day must be a lowercase weekday or daily")
    clock = schedule["time"]
    if not isinstance(clock, str) or len(clock) != 5:
        raise ValueError("schedule.time must use HH:MM (24-hour time)")
    try:
        datetime.datetime.strptime(clock, "%H:%M")
    except ValueError as error:
        raise ValueError("schedule.time must use HH:MM (24-hour time)") from error


def validate_smtp(smtp):
    """Check transport settings and require encryption for authentication."""
    for name in ("host", "password_env"):
        check_text(smtp[name], "smtp." + name)
    check_text(smtp["username"], "smtp.username", allow_empty=True)
    if (not isinstance(smtp["port"], int) or isinstance(smtp["port"], bool)
            or not 1 <= smtp["port"] <= 65535):
        raise ValueError("smtp.port must be an integer between 1 and 65535")
    if (not isinstance(smtp["timeout"], int) or isinstance(smtp["timeout"], bool)
            or smtp["timeout"] <= 0):
        raise ValueError("smtp.timeout must be a positive integer in seconds")
    if smtp["security"] not in ("none", "starttls", "ssl"):
        raise ValueError("smtp.security must be none, starttls, or ssl")
    if smtp["username"] and smtp["security"] == "none":
        raise ValueError("SMTP authentication requires starttls or ssl")


def load_config(filename=None) -> dict:
    """Load JSON settings, resolving file paths relative to the configuration.

    Args:
        filename (str or pathlib.Path, optional): Configuration path, or None
            for interactive local-relay mode.

    Returns:
        dict: Validated settings with absolute message and attachment paths.
    """
    values = {}
    base = Path.cwd()
    if filename is not None:
        path = Path(filename).resolve()
        with path.open(encoding="utf-8") as config_file:
            values = json.load(config_file)
        base = path.parent
    check_keys(values, DEFAULTS, "configuration")
    config = {**DEFAULTS, **values}
    for section in ("smtp", "schedule"):
        options = values.get(section, {})
        check_keys(options, DEFAULTS[section], section)
        config[section] = {**DEFAULTS[section], **options}
    if filename is None:
        config["sender"] = input("YOUR email address:").strip()
        config["recipients"] = [input("RECIPIENT's email address:").strip()]
    validate_config(config)
    config["message_file"] = base / config["message_file"]
    config["attachments"] = [base / name for name in config["attachments"]]
    return config


def build_message(config):
    """Read the current body and attachments and return a MIME email message."""
    path = config["message_file"]
    body = path.read_text(encoding="utf-8")
    subtype = "html" if path.suffix.lower() in (".html", ".htm") else "plain"
    msg = EmailMessage()
    msg.set_content(body, subtype=subtype)
    msg["Subject"] = config["subject"].replace("{date}", str(datetime.date.today()))
    msg["From"] = config["sender"]
    msg["To"] = ", ".join(config["recipients"])
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain=config["sender"].rsplit("@", 1)[1])
    for attachment in config["attachments"]:
        content_type, encoding = mimetypes.guess_type(str(attachment))
        if content_type is None or encoding is not None:
            content_type = "application/octet-stream"
        maintype, subtype = content_type.split("/", 1)
        msg.add_attachment(
            attachment.read_bytes(), maintype=maintype, subtype=subtype,
            filename=attachment.name,
        )
    return msg


def send_announcement(config):
    """Send current files via SMTP and close the connection on success or failure."""
    msg = build_message(config)
    smtp = config["smtp"]
    password = os.environ.get(smtp["password_env"])
    if smtp["username"] and not password:
        raise ValueError("Set the password environment variable " + smtp["password_env"])
    connection = smtplib.SMTP_SSL if smtp["security"] == "ssl" else smtplib.SMTP
    options = {"timeout": smtp["timeout"]}
    if smtp["security"] == "ssl":
        options["context"] = ssl.create_default_context()
    with connection(smtp["host"], smtp["port"], **options) as server:
        if smtp["security"] == "starttls":
            server.starttls(context=ssl.create_default_context())
        if smtp["username"]:
            server.login(smtp["username"], password)
        refused = server.send_message(
            msg, from_addr=config["sender"], to_addrs=config["recipients"],
        )
        if refused:
            raise smtplib.SMTPRecipientsRefused(refused)
    print("Message accepted by SMTP server on", datetime.datetime.now(), "!", flush=True)


def next_run(schedule, now=None):
    """Return the next daily or weekly local time strictly after now."""
    if now is None:
        now = datetime.datetime.now()
    hour, minute = map(int, schedule["time"].split(":"))
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if schedule["day"] != "daily":
        target += datetime.timedelta(days=(DAYS.index(schedule["day"]) - now.weekday()) % 7)
    if target <= now:
        target += datetime.timedelta(days=1 if schedule["day"] == "daily" else 7)
    return target


def run_schedule(config):
    """Send at each scheduled local time until interrupted, skipping missed slots."""
    target = next_run(config["schedule"])
    while True:
        print("Next announcement:", target, "(computer local time)", flush=True)
        while True:
            remaining = (target - datetime.datetime.now()).total_seconds()
            if remaining <= 0:
                break
            time.sleep(min(remaining, 30))
        try:
            send_announcement(config)
        except (OSError, ValueError, smtplib.SMTPException) as error:
            print("Announcement failed:", error, file=sys.stderr, flush=True)
        # Advance from at least the previous slot, even if the clock moved back.
        target = next_run(config["schedule"], max(target, datetime.datetime.now()))


def main(argv=None) -> int:
    """Run the command-line mailer and return an exit status.

    Args:
        argv (list[str], optional): Arguments, or None to read the command line.

    Returns:
        int: Zero on success or interruption, one on file, configuration, or SMTP errors.

    Raises:
        SystemExit: Invalid command-line arguments exit with status two.
    """
    parser = argparse.ArgumentParser(description="Send announcement files by email.")
    parser.add_argument("--config", type=Path, help="JSON configuration file")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--schedule", action="store_true", help="wait and send on the schedule")
    mode.add_argument("--once", action="store_true", help="send immediately (the default)")
    mode.add_argument("--dry-run", action="store_true", help="validate files without sending")
    args = parser.parse_args(argv)
    if args.schedule and args.config is None:
        parser.error("--schedule requires --config for unattended delivery")
    try:
        config = load_config(args.config)
        if args.dry_run:
            msg = build_message(config)
            print("Ready:", msg["Subject"])
            print("Recipients:", msg["To"])
            print("Attachments:", len(config["attachments"]))
            print("Next announcement:", next_run(config["schedule"]), "(computer local time)")
        elif args.schedule:
            build_message(config)  # Fail early when a configured file is unavailable.
            smtp = config["smtp"]
            if smtp["username"] and not os.environ.get(smtp["password_env"]):
                raise ValueError("Set the password environment variable " + smtp["password_env"])
            run_schedule(config)
        else:
            send_announcement(config)
    except (OSError, ValueError, EOFError, smtplib.SMTPException) as error:
        print("Announcement failed:", error, file=sys.stderr, flush=True)
        return 1
    except KeyboardInterrupt:
        print("\nAnnouncement sender stopped.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
