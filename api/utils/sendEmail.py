# #this file will send confirmation email for client and cleaner
import smtplib
import os

from dotenv import dotenv_values
temp = dotenv_values(".env")
password = temp["passw"] 



# password = config['passw']

gmail_user = 'karanpreetsodhi1997@gmail.com'
gmail_password = password

sent_from = gmail_user
to = ['karanpreetsodhi1996@gmail.com']
subject = 'Testing 123'
body = 'Hello from the other world again'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.ehlo()
    smtp_server.login(gmail_user, gmail_password)
    smtp_server.sendmail(sent_from, to, email_text)
    smtp_server.close()
    print ("Email sent successfully!")
except Exception as ex:
    print ("Something went wrong….",ex)