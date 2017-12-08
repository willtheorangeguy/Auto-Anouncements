from email.mime.text import MIMEText
import smtplib

msg = MIMEText(
   "<h1>A Heading</h1><p>Hello There!</p>","html")

msg['Subject'] = 'A Test HTML Message'
msg['From']='SenderAddress'
msg['To'] = 'RecipientAddress'

s = smtplib.SMTP('localhost')
s.sendmail('SenderAddress',
           ['RecipientAddress'],
           msg.as_string())

print("Message Sent!")
