"""
Comprehensive test suite for Auto Announcements send module.
Tests the email sending functionality with mocked dependencies.
"""
import datetime
from unittest.mock import Mock, patch, MagicMock
from email.mime.text import MIMEText
import pytest
from send.send import main


class TestMain:
    """Test suite for the main email sending function."""

    @patch('send.send.input')
    @patch('send.send.smtplib.SMTP')
    @patch('send.send.datetime')
    def test_main_successful_send(self, mock_datetime, mock_smtp, mock_input):
        """Test that main successfully sends an email with valid inputs."""
        # Setup mocks
        mock_input.side_effect = ['sender@example.com', 'recipient@example.com']
        
        # Mock datetime
        mock_date = datetime.datetime(2024, 1, 15, 10, 30, 45)
        mock_date_today = datetime.date(2024, 1, 15)
        mock_datetime.datetime.today.return_value = mock_date
        mock_datetime.date.today.return_value = mock_date_today
        
        # Mock SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        # Run main
        main()
        
        # Verify SMTP was called correctly
        mock_smtp.assert_called_once_with('localhost')
        mock_server.sendmail.assert_called_once()
        
        # Verify sendmail was called with correct parameters
        call_args = mock_server.sendmail.call_args
        assert call_args[0][0] == 'sender@example.com'  # from address
        assert call_args[0][1] == ['recipient@example.com']  # to address
        assert isinstance(call_args[0][2], str)  # message string

    @patch('send.send.input')
    @patch('send.send.smtplib.SMTP')
    @patch('send.send.datetime')
    def test_main_email_addresses_used(self, mock_datetime, mock_smtp, mock_input):
        """Test that the correct email addresses are used."""
        mock_input.side_effect = ['test@sender.com', 'test@recipient.com']
        
        mock_date = datetime.datetime(2024, 1, 15, 10, 30, 45)
        mock_date_today = datetime.date(2024, 1, 15)
        mock_datetime.datetime.today.return_value = mock_date
        mock_datetime.date.today.return_value = mock_date_today
        
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        main()
        
        # Check that sendmail was called with the correct addresses
        call_args = mock_server.sendmail.call_args[0]
        assert call_args[0] == 'test@sender.com'
        assert call_args[1] == ['test@recipient.com']

    @patch('send.send.input')
    @patch('send.send.smtplib.SMTP')
    @patch('send.send.datetime')
    def test_main_message_format(self, mock_datetime, mock_smtp, mock_input):
        """Test that the email message is properly formatted."""
        mock_input.side_effect = ['sender@test.com', 'recipient@test.com']
        
        mock_date = datetime.datetime(2024, 1, 15, 10, 30, 45)
        mock_date_today = datetime.date(2024, 1, 15)
        mock_datetime.datetime.today.return_value = mock_date
        mock_datetime.date.today.return_value = mock_date_today
        
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        main()
        
        # Verify that message contains HTML
        call_args = mock_server.sendmail.call_args[0]
        message_str = call_args[2]
        assert 'Content-Type: text/html' in message_str
        assert '<h1>A Heading</h1>' in message_str
        assert '<p>Hello There!</p>' in message_str

    @patch('send.send.input')
    @patch('send.send.smtplib.SMTP')
    @patch('send.send.datetime')
    def test_main_date_in_message(self, mock_datetime, mock_smtp, mock_input):
        """Test that the date is properly included in the message."""
        mock_input.side_effect = ['sender@test.com', 'recipient@test.com']
        
        mock_date = datetime.datetime(2024, 3, 20, 14, 25, 30)
        mock_date_today = datetime.date(2024, 3, 20)
        mock_datetime.datetime.today.return_value = mock_date
        mock_datetime.date.today.return_value = mock_date_today
        
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        main()
        
        # Verify message contains date information
        call_args = mock_server.sendmail.call_args[0]
        message_str = call_args[2]
        assert '2024-03-20' in message_str

    @patch('send.send.input')
    @patch('send.send.smtplib.SMTP')
    @patch('send.send.datetime')
    def test_main_smtp_connection(self, mock_datetime, mock_smtp, mock_input):
        """Test that SMTP connection is established correctly."""
        mock_input.side_effect = ['sender@test.com', 'recipient@test.com']
        
        mock_date = datetime.datetime(2024, 1, 15, 10, 30, 45)
        mock_date_today = datetime.date(2024, 1, 15)
        mock_datetime.datetime.today.return_value = mock_date
        mock_datetime.date.today.return_value = mock_date_today
        
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        main()
        
        # Verify SMTP was initialized with localhost
        mock_smtp.assert_called_once_with('localhost')

    @patch('send.send.input')
    @patch('send.send.smtplib.SMTP')
    @patch('send.send.datetime')
    def test_main_input_prompts(self, mock_datetime, mock_smtp, mock_input):
        """Test that the correct input prompts are used."""
        mock_input.side_effect = ['user@example.com', 'receiver@example.com']
        
        mock_date = datetime.datetime(2024, 1, 15, 10, 30, 45)
        mock_date_today = datetime.date(2024, 1, 15)
        mock_datetime.datetime.today.return_value = mock_date
        mock_datetime.date.today.return_value = mock_date_today
        
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        main()
        
        # Verify input was called twice (for sender and recipient)
        assert mock_input.call_count == 2
        
    @patch('send.send.input')
    @patch('send.send.smtplib.SMTP')
    @patch('send.send.datetime')
    def test_main_with_different_dates(self, mock_datetime, mock_smtp, mock_input):
        """Test main function with various dates to ensure date handling works."""
        mock_input.side_effect = ['sender@test.com', 'recipient@test.com']
        
        # Test with leap year date
        mock_date = datetime.datetime(2024, 2, 29, 12, 0, 0)
        mock_date_today = datetime.date(2024, 2, 29)
        mock_datetime.datetime.today.return_value = mock_date
        mock_datetime.date.today.return_value = mock_date_today
        
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        main()
        
        # Verify the date was used
        call_args = mock_server.sendmail.call_args[0]
        message_str = call_args[2]
        assert '2024-02-29' in message_str

    @patch('send.send.input')
    @patch('send.send.smtplib.SMTP')
    @patch('send.send.datetime')
    @patch('builtins.print')
    def test_main_prints_confirmation(self, mock_print, mock_datetime, mock_smtp, mock_input):
        """Test that success message is printed after sending."""
        mock_input.side_effect = ['sender@test.com', 'recipient@test.com']
        
        mock_date = datetime.datetime(2024, 1, 15, 10, 30, 45)
        mock_date_today = datetime.date(2024, 1, 15)
        mock_datetime.datetime.today.return_value = mock_date
        mock_datetime.date.today.return_value = mock_date_today
        
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        main()
        
        # Verify print was called with success message
        assert mock_print.call_count >= 2  # At least date print and success print
        
        # Check that success message was printed
        success_call_found = False
        for call in mock_print.call_args_list:
            if len(call[0]) > 0 and 'Message sent successfully' in str(call[0][0]):
                success_call_found = True
                break
        assert success_call_found, "Success message should be printed"


class TestEmailMessage:
    """Test suite for email message creation and formatting."""
    
    @patch('send.send.input')
    @patch('send.send.smtplib.SMTP')
    @patch('send.send.datetime')
    def test_message_has_subject(self, mock_datetime, mock_smtp, mock_input):
        """Test that the email message has a subject line."""
        mock_input.side_effect = ['sender@test.com', 'recipient@test.com']
        
        mock_date = datetime.datetime(2024, 1, 15, 10, 30, 45)
        mock_date_today = datetime.date(2024, 1, 15)
        mock_datetime.datetime.today.return_value = mock_date
        mock_datetime.date.today.return_value = mock_date_today
        
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        main()
        
        # Verify message has subject
        call_args = mock_server.sendmail.call_args[0]
        message_str = call_args[2]
        assert 'Subject:' in message_str
        assert 'Church Announcements' in message_str

    @patch('send.send.input')
    @patch('send.send.smtplib.SMTP')
    @patch('send.send.datetime')
    def test_message_has_from_field(self, mock_datetime, mock_smtp, mock_input):
        """Test that the email message has a From field."""
        mock_input.side_effect = ['sender@test.com', 'recipient@test.com']
        
        mock_date = datetime.datetime(2024, 1, 15, 10, 30, 45)
        mock_date_today = datetime.date(2024, 1, 15)
        mock_datetime.datetime.today.return_value = mock_date
        mock_datetime.date.today.return_value = mock_date_today
        
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        main()
        
        # Verify message has From field
        call_args = mock_server.sendmail.call_args[0]
        message_str = call_args[2]
        assert 'From:' in message_str
        assert 'sender@test.com' in message_str

    @patch('send.send.input')
    @patch('send.send.smtplib.SMTP')
    @patch('send.send.datetime')
    def test_message_has_to_field(self, mock_datetime, mock_smtp, mock_input):
        """Test that the email message has a To field."""
        mock_input.side_effect = ['sender@test.com', 'recipient@test.com']
        
        mock_date = datetime.datetime(2024, 1, 15, 10, 30, 45)
        mock_date_today = datetime.date(2024, 1, 15)
        mock_datetime.datetime.today.return_value = mock_date
        mock_datetime.date.today.return_value = mock_date_today
        
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        main()
        
        # Verify message has To field
        call_args = mock_server.sendmail.call_args[0]
        message_str = call_args[2]
        assert 'To:' in message_str
        assert 'recipient@test.com' in message_str


class TestErrorHandling:
    """Test suite for error handling scenarios."""
    
    @patch('send.send.input')
    @patch('send.send.smtplib.SMTP')
    @patch('send.send.datetime')
    def test_smtp_connection_with_localhost(self, mock_datetime, mock_smtp, mock_input):
        """Test SMTP connection uses localhost as expected."""
        mock_input.side_effect = ['sender@test.com', 'recipient@test.com']
        
        mock_date = datetime.datetime(2024, 1, 15, 10, 30, 45)
        mock_date_today = datetime.date(2024, 1, 15)
        mock_datetime.datetime.today.return_value = mock_date
        mock_datetime.date.today.return_value = mock_date_today
        
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        main()
        
        # Ensure localhost is used for SMTP connection
        args, kwargs = mock_smtp.call_args
        assert args[0] == 'localhost'


class TestIntegration:
    """Integration tests for the complete email flow."""
    
    @patch('send.send.input')
    @patch('send.send.smtplib.SMTP')
    @patch('send.send.datetime')
    def test_complete_email_flow(self, mock_datetime, mock_smtp, mock_input):
        """Test the complete flow from input to sending."""
        # Setup all mocks
        mock_input.side_effect = ['complete@sender.com', 'complete@recipient.com']
        
        mock_date = datetime.datetime(2024, 5, 10, 15, 45, 0)
        mock_date_today = datetime.date(2024, 5, 10)
        mock_datetime.datetime.today.return_value = mock_date
        mock_datetime.date.today.return_value = mock_date_today
        
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        # Run the complete flow
        main()
        
        # Verify all components worked together
        assert mock_input.call_count == 2
        mock_smtp.assert_called_once()
        mock_server.sendmail.assert_called_once()
        
        # Verify the complete message
        call_args = mock_server.sendmail.call_args[0]
        assert call_args[0] == 'complete@sender.com'
        assert call_args[1] == ['complete@recipient.com']
        
        message_str = call_args[2]
        assert 'complete@sender.com' in message_str
        assert 'complete@recipient.com' in message_str
        assert '2024-05-10' in message_str
        assert 'Church Announcements' in message_str
        assert '<h1>A Heading</h1>' in message_str
