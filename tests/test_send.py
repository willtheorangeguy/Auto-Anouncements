"""Test the send.py file."""

# Get out of the test directory
import os
import sys
import datetime
from unittest.mock import MagicMock
import send

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(os.path.join(parent_dir, "send"))


def test_main(mocker):
    """Test the main function."""
    mock_input = mocker.patch(
        "builtins.input", side_effect=["sender@example.com", "receiver@example.com"]
    )
    mock_smtp = mocker.patch("smtplib.SMTP")
    mock_print = mocker.patch("builtins.print")

    mock_smtp_instance = MagicMock()
    mock_smtp.return_value = mock_smtp_instance

    send.main()

    mock_input.assert_any_call("YOUR email address:")
    mock_input.assert_any_call("RECIPIENT's email address:")
    mock_smtp.assert_called_once_with("localhost")
    mock_smtp_instance.sendmail.assert_called_once_with(
        "sender@example.com",
        ["receiver@example.com"]
    )
    date_today = str(datetime.datetime.today())
    mock_print.assert_called_with("Message sent successfully on", date_today, "!")
