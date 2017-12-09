from email.mime.text import *
import smtplib
import time
import datetime

date = 'Dec/8/2017'
print(date)

msg = MIMEText(
   "<h1>A Heading</h1><p>Hello There!</p>","html")

msg['Subject'] = 'Announcements for', date
msg['From']='SenderAddress'
msg['To'] = 'RecipientAddress'

s = smtplib.SMTP('localhost')
s.sendmail('SenderAddress',
           ['RecipientAddress'],
           msg.as_string())

print("Message Sent on", date)
