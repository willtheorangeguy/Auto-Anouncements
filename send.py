# Copyright (C) 2017 - 2019 Dog Face Development Co.

from email.mime.text import *
import smtplib
import time
import datetime

sendaddress = input('YOUR email address:')
# replace above with your email address for direct delivery
receiveaddress = input('RECIPIENT\'s email address:')
# replace above with the reciptents email address for direct delivery

DATE = str(datetime.datetime.today())
DATEtoday = str(datetime.date.today())
print(DATE)

msg = MIMEText(
   '<h1>A Heading</h1><p>Hello There!</p>', 'html')

msg['Subject'] = 'Church Announcements for', DATEtoday
msg['From'] = sendaddress
msg['To'] = receiveaddress

s = smtplib.SMTP('localhost')
s.sendmail(sendaddress,
           [receiveaddress],
           msg.as_string())

print('Message sent successfully on', DATE, '!')
