import pytest
import datetime
from unittest.mock import MagicMock

# Get out of the test directory
import sys
sys.path.append('../send')

# Import file to test
import send

def test_main(mocker):
    mock_input = mocker.patch('builtins.input', side_effect=['sender@example.com', 'receiver@example.com'])
    mock_smtp = mocker.patch('smtplib.SMTP')
    mock_print = mocker.patch('builtins.print')

    mock_smtp_instance = MagicMock()
    mock_smtp.return_value = mock_smtp_instance

    send.main()

    mock_input.assert_any_call("YOUR email address:")
    mock_input.assert_any_call("RECIPIENT's email address:")
    mock_smtp.assert_called_once_with("localhost")
    mock_smtp_instance.sendmail.assert_called_once_with(
        'sender@example.com', 
        ['receiver@example.com'], 
        send.msg.as_string()  # assuming msg is a global variable
    )
    date_today = str(datetime.datetime.today())
    mock_print.assert_called_with("Message sent successfully on", date_today, "!")
    