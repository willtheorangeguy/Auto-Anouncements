from email.mime.text import MIMEText
import smtplib

msg = MIMEText("Hello There!")

msg['Subject'] = 'A Test Message'
msg['From']='SenderAddress'
msg['To'] = 'RecipientAddress>'

s = smtplib.SMTP('localhost')
s.sendmail('SenderAddress',
           ['RecipientAddress'],
           msg.as_string())

print("Message Sent!")
