"""
Exercise the complete CLI against a local SMTP sink without external delivery.
Copyright (C) 2017-2026 willtheorangeguy
"""

from email import policy
from email.parser import BytesParser
import json
from pathlib import Path
import socketserver
import subprocess
import sys
import threading


class MailSink(socketserver.StreamRequestHandler):
    """Accept a single SMTP message into memory and never relay it."""

    def handle(self):
        """Implement the SMTP commands needed for a plain local submission."""
        self.connection.settimeout(5)
        self.wfile.write(b"220 localhost test sink\r\n")
        while True:
            command = self.rfile.readline()
            if not command:
                return
            self.server.commands.append(command)
            if command.upper().startswith(b"DATA"):
                self.wfile.write(b"354 Send message\r\n")
                lines = []
                while True:
                    line = self.rfile.readline()
                    if line == b".\r\n":
                        break
                    if not line:
                        return
                    lines.append(line[1:] if line.startswith(b"..") else line)
                self.server.messages.append(b"".join(lines))
                self.wfile.write(b"250 Accepted\r\n")
            elif command.upper().startswith(b"QUIT"):
                self.wfile.write(b"221 Goodbye\r\n")
                return
            else:
                self.wfile.write(b"250 OK\r\n")


def test_cli_sends_to_local_sink(tmp_path):
    """A subprocess loads relative files and submits intact MIME over a real socket."""
    body = tmp_path / "message.html"
    body.write_text("<h1>Latest announcements</h1>", encoding="utf-8")
    attachment = tmp_path / "announcements.pdf"
    attachment.write_bytes(b"%PDF-1.4\n\x00\xff")
    with socketserver.TCPServer(("127.0.0.1", 0), MailSink) as server:
        server.commands = []
        server.messages = []
        config = tmp_path / "config.json"
        config.write_text(json.dumps({
            "sender": "sender@example.org",
            "recipients": ["first@example.org", "second@example.org"],
            "attachments": ["announcements.pdf"],
            "smtp": {"host": "127.0.0.1", "port": server.server_address[1], "timeout": 5},
        }), encoding="utf-8")
        thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.05})
        thread.start()
        try:
            result = subprocess.run(
                [sys.executable, "-m", "send", "--config", str(config), "--once"],
                cwd=Path(__file__).resolve().parents[1],
                capture_output=True, text=True, timeout=20, check=False,
            )
        finally:
            server.shutdown()
            thread.join(timeout=5)
        assert result.returncode == 0, result.stderr
        assert "accepted by SMTP server" in result.stdout
        assert len(server.messages) == 1
        msg = BytesParser(policy=policy.default).parsebytes(server.messages[0])
        assert msg.get_body().get_content().strip() == "<h1>Latest announcements</h1>"
        assert list(msg.iter_attachments())[0].get_payload(decode=True) == attachment.read_bytes()
        recipients = [line for line in server.commands if line.lower().startswith(b"rcpt to:")]
        assert len(recipients) == 2
