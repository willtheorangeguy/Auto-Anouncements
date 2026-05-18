"""
Auto Announcements - A bot framework that automatically sends announcements.
Copyright (C) 2017-2026 willtheorangeguy
"""

# pylint: disable=global-variable-undefined

from email.mime.text import MIMEText
import smtplib
import datetime


def main():
    """Main function for sending emails."""
    global msg
    sendaddress = input("YOUR email address:")
    # replace above with your email address for direct delivery
    receiveaddress = input("RECIPIENT's email address:")
    # replace above with the recipients email address for direct delivery

    date = str(datetime.datetime.today())
    date_today = str(datetime.date.today())
    print(date)

    msg = MIMEText("<h1>A Heading</h1><p>Hello There!</p>", "html")

    msg["Subject"] = "Church Announcements for " + date_today
    msg["From"] = sendaddress
    msg["To"] = receiveaddress

    s = smtplib.SMTP("localhost")
    s.sendmail(sendaddress, [receiveaddress], msg.as_string())

    print("Message sent successfully on", date, "!")


if __name__ == "__main__":
    main()
