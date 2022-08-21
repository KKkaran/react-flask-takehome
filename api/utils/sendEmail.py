# #this file will send confirmation email for client and cleaner
import smtplib
import os

from dotenv import dotenv_values
temp = dotenv_values(".env")
password = temp["passw"] 



# def testEmail(client, cleaner, schedule):
#     print("**************************************")
#     print(client , cleaner, schedule["start"] + " - ",schedule["end"] + " on ",schedule["date"]);
#     print("**************************************")

def sendConfirmationEmail(client, cleaner, schedule):
    gmail_user = 'karanpreetsodhi1997@gmail.com'
    gmail_password = password

    sent_from = gmail_user
    to = [client,cleaner]
    subject = 'Testing 123'
    body = f'This is a confirmation email for the scheduled Cleaning shift on {schedule["date"]} starting at {schedule["start"]} for {schedule["end"]} hours.'

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
