"""
Tests for announcement configuration, delivery, and scheduling.
Copyright (C) 2017-2026 willtheorangeguy
"""

import datetime
import json
import smtplib
from unittest.mock import patch

import pytest

from send.send import build_message, load_config, main, next_run, run_schedule, send_announcement


@pytest.fixture
def config_file(tmp_path):
    """Create a complete local-relay configuration with a binary attachment."""
    (tmp_path / "message.html").write_text("<h1>Announcements — café</h1>", encoding="utf-8")
    (tmp_path / "announcements.pdf").write_bytes(b"%PDF-1.4\n\x00\xff")
    path = tmp_path / "config.json"
    path.write_text(json.dumps({
        "sender": "sender@example.org",
        "recipients": ["first@example.org", "second@example.org"],
        "attachments": ["announcements.pdf"],
    }), encoding="utf-8")
    return path


@pytest.fixture
def smtp_server():
    """Mock SMTP without making network connections."""
    with patch("send.send.smtplib.SMTP") as smtp:
        server = smtp.return_value.__enter__.return_value
        server.send_message.return_value = {}
        yield smtp, server


class TestConfiguration:
    """Check unattended settings and actionable validation failures."""

    def test_paths_relative_to_config(self, config_file, tmp_path, monkeypatch):
        """Launching from another directory must still use the configured files."""
        elsewhere = tmp_path / "elsewhere"
        elsewhere.mkdir()
        monkeypatch.chdir(elsewhere)
        config = load_config(config_file)
        assert config["message_file"] == config_file.parent / "message.html"
        assert config["attachments"] == [config_file.parent / "announcements.pdf"]

    @pytest.mark.parametrize("values", [
        [], {"smtp": None}, {"schedule": []}, {"recipient": ["someone@example.org"]},
        {"recipients": []}, {"recipients": "someone@example.org"},
        {"sender": "invalid"}, {"sender": "bad\r\nBcc: x@example.org"},
        {"sender": "@example.org"}, {"sender": "me@"},
        {"subject": "Hi\nBcc: x@example.org"}, {"attachments": "file.pdf"},
        {"attachments": [None]}, {"message_file": ""},
        {"smtp": {"port": 0}}, {"smtp": {"port": True}},
        {"smtp": {"timeout": -1}}, {"smtp": {"security": "tls"}},
        {"smtp": {"username": "me"}}, {"smtp": {"password": "do-not-store"}},
        {"schedule": {"day": "Saturday"}}, {"schedule": {"time": "25:00"}},
        {"schedule": {"time": "9:00"}}, {"schedule": {"time": None}},
    ])
    def test_invalid_config(self, values, config_file, smtp_server, capsys):
        """Invalid settings fail before contacting SMTP."""
        original = json.loads(config_file.read_text(encoding="utf-8"))
        config_file.write_text(
            json.dumps({**original, **values} if isinstance(values, dict) else values),
            encoding="utf-8",
        )
        assert main(["--config", str(config_file)]) == 1
        smtp_server[0].assert_not_called()
        assert "Announcement failed:" in capsys.readouterr().err

    def test_invalid_json(self, config_file):
        """Malformed JSON produces a nonzero exit status."""
        config_file.write_text("{", encoding="utf-8")
        assert main(["--config", str(config_file)]) == 1

    def test_schedule_requires_config(self):
        """An unattended scheduler never falls back to prompts."""
        with pytest.raises(SystemExit) as error:
            main(["--schedule"])
        assert error.value.code == 2


class TestDelivery:
    """Verify real MIME contents and SMTP connection behavior."""

    def test_main_successful_send(self, config_file, smtp_server, capsys):
        """Send current UTF-8 HTML, dated headers, and exact attachment bytes."""
        smtp, server = smtp_server
        assert main(["--config", str(config_file), "--once"]) == 0
        smtp.assert_called_once_with("localhost", 25, timeout=30)
        server.send_message.assert_called_once()
        msg = server.send_message.call_args.args[0]
        assert msg["Subject"] == "Church Announcements for " + str(datetime.date.today())
        assert msg["From"] == "sender@example.org"
        assert msg["To"] == "first@example.org, second@example.org"
        assert msg["Date"] and msg["Message-ID"]
        assert "Announcements — café" in msg.get_body().get_content()
        attachment = list(msg.iter_attachments())[0]
        assert attachment.get_filename() == "announcements.pdf"
        assert attachment.get_payload(decode=True) == b"%PDF-1.4\n\x00\xff"
        assert server.send_message.call_args.kwargs["to_addrs"] == [
            "first@example.org", "second@example.org",
        ]
        smtp.return_value.__exit__.assert_called_once()
        assert "accepted by SMTP server" in capsys.readouterr().out

    @pytest.mark.parametrize("security,port", [("starttls", 587), ("ssl", 465)])
    def test_authenticated_delivery(self, security, port, config_file, monkeypatch):
        """TLS is established before login and the password comes from the environment."""
        config = load_config(config_file)
        config["smtp"].update(security=security, port=port, username="sender@example.org")
        monkeypatch.setenv("AUTO_ANNOUNCEMENTS_PASSWORD", "test-password")
        with patch("send.send.smtplib.SMTP") as plain, patch("send.send.smtplib.SMTP_SSL") as secure:
            connection = secure if security == "ssl" else plain
            server = connection.return_value.__enter__.return_value
            server.send_message.return_value = {}
            send_announcement(config)
            server.login.assert_called_once_with("sender@example.org", "test-password")
            if security == "starttls":
                assert [call[0] for call in server.method_calls] == [
                    "starttls", "login", "send_message",
                ]
                assert server.starttls.call_args.kwargs["context"].check_hostname
                secure.assert_not_called()
            else:
                assert connection.call_args.kwargs["context"].check_hostname
                plain.assert_not_called()

    def test_missing_password(self, config_file, smtp_server, monkeypatch):
        """Missing credentials fail before a network connection."""
        config = load_config(config_file)
        config["smtp"].update(security="starttls", username="sender@example.org")
        monkeypatch.delenv("AUTO_ANNOUNCEMENTS_PASSWORD", raising=False)
        with pytest.raises(ValueError, match="password environment variable"):
            send_announcement(config)
        smtp_server[0].assert_not_called()

    def test_partial_refusal_is_failure(self, config_file, smtp_server, capsys):
        """Partial delivery must not print a blanket success or retry accepted recipients."""
        smtp_server[1].send_message.return_value = {"second@example.org": (550, b"Refused")}
        assert main(["--config", str(config_file)]) == 1
        smtp_server[1].send_message.assert_called_once()
        assert "accepted by SMTP server" not in capsys.readouterr().out

    def test_connection_failure(self, config_file, smtp_server, capsys):
        """An unavailable relay produces a readable error and a failing exit status."""
        smtp_server[0].side_effect = ConnectionRefusedError("Connection refused")
        assert main(["--config", str(config_file)]) == 1
        assert "Connection refused" in capsys.readouterr().err

    def test_send_failure_closes_connection(self, config_file, smtp_server):
        """SMTP errors still close the connection."""
        smtp_server[1].send_message.side_effect = smtplib.SMTPDataError(554, b"Rejected")
        assert main(["--config", str(config_file)]) == 1
        smtp_server[0].return_value.__exit__.assert_called_once()

    def test_missing_attachment(self, config_file, smtp_server):
        """No email is submitted if any configured attachment is missing."""
        config = load_config(config_file)
        config["attachments"] = [config_file.parent / "missing.pdf"]
        with pytest.raises(FileNotFoundError):
            send_announcement(config)
        smtp_server[0].assert_not_called()

    def test_reload_files(self, config_file):
        """Each message uses the latest body and attachment contents."""
        config = load_config(config_file)
        first = build_message(config)
        config["message_file"].write_text("New announcement", encoding="utf-8")
        config["attachments"][0].write_bytes(b"updated")
        second = build_message(config)
        assert first["Message-ID"] != second["Message-ID"]
        assert second.get_body().get_content().strip() == "New announcement"
        assert list(second.iter_attachments())[0].get_payload(decode=True) == b"updated"

    def test_plain_text_and_unknown_attachment(self, config_file):
        """Text bodies and unrecognized binary attachments get appropriate MIME types."""
        config = load_config(config_file)
        path = config_file.parent / "body.txt"
        path.write_text("News", encoding="utf-8")
        binary = config_file.parent / "file.unknown-extension"
        binary.write_bytes(b"\x00\xff")
        config.update(message_file=path, attachments=[binary])
        msg = build_message(config)
        assert msg.get_body().get_content_type() == "text/plain"
        assert list(msg.iter_attachments())[0].get_content_type() == "application/octet-stream"

    def test_dry_run_does_not_connect(self, config_file, smtp_server):
        """Validation works without SMTP credentials or network access."""
        assert main(["--config", str(config_file), "--dry-run"]) == 0
        smtp_server[0].assert_not_called()

    def test_interactive_send(self, config_file, smtp_server, monkeypatch):
        """The original two-address interactive workflow remains available."""
        monkeypatch.chdir(config_file.parent)
        with patch("send.send.input", side_effect=["sender@example.org", "first@example.org"]):
            assert main([]) == 0
        smtp_server[1].send_message.assert_called_once()


class TestSchedule:
    """Exercise calendar boundaries and the waiting loop without sleeping."""

    @pytest.mark.parametrize("day,now,expected", [
        ("saturday", "2026-09-07T12:00", "2026-09-12T18:00"),
        ("saturday", "2026-09-12T17:59", "2026-09-12T18:00"),
        ("saturday", "2026-09-12T18:00", "2026-09-19T18:00"),
        ("saturday", "2026-09-12T19:00", "2026-09-19T18:00"),
        ("daily", "2026-12-31T19:00", "2027-01-01T18:00"),
        ("daily", "2024-02-28T19:00", "2024-02-29T18:00"),
        ("daily", "2026-09-07T12:00", "2026-09-07T18:00"),
    ])
    def test_next_run(self, day, now, expected):
        """Daily and weekly schedules advance to the next future calendar slot."""
        assert next_run(
            {"day": day, "time": "18:00"}, datetime.datetime.fromisoformat(now),
        ) == datetime.datetime.fromisoformat(expected)

    @pytest.mark.parametrize("failure", [None, OSError("offline")])
    def test_wait_send_and_continue(self, failure, config_file, capsys):
        """Wait until due, attempt once, then keep running even after a send failure."""
        config = load_config(config_file)
        clock = datetime.datetime(2026, 9, 12, 17, 59, 30)
        target = clock + datetime.timedelta(seconds=30)
        with patch("send.send.datetime") as dates, patch("send.send.time.sleep") as sleep:
            dates.datetime.now.side_effect = [clock, target, target]
            with patch("send.send.next_run", wraps=next_run) as upcoming:
                with patch("send.send.send_announcement", side_effect=failure) as send:
                    upcoming.side_effect = [target, KeyboardInterrupt]
                    with pytest.raises(KeyboardInterrupt):
                        run_schedule(config)
        sleep.assert_called_once_with(30)
        send.assert_called_once_with(config)
        assert upcoming.call_count == 2
        if failure:
            assert "offline" in capsys.readouterr().err

    def test_resume_skips_backlog(self, config_file):
        """After a long suspension, send once and schedule the next future occurrence."""
        config = load_config(config_file)
        target = datetime.datetime(2026, 9, 12, 18)
        resumed = datetime.datetime(2026, 9, 28, 12)
        with patch("send.send.datetime") as dates, patch("send.send.next_run") as upcoming:
            dates.datetime.now.return_value = resumed
            upcoming.side_effect = [target, KeyboardInterrupt]
            with patch("send.send.send_announcement") as send:
                with pytest.raises(KeyboardInterrupt):
                    run_schedule(config)
        send.assert_called_once()
        assert upcoming.call_args.args[1] == resumed

    def test_main_schedule_and_interrupt(self, config_file):
        """The CLI starts the schedule without sending immediately and exits cleanly."""
        with patch("send.send.run_schedule", side_effect=KeyboardInterrupt) as schedule:
            assert main(["--config", str(config_file), "--schedule"]) == 0
        schedule.assert_called_once()
