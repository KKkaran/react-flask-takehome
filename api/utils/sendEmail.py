# #this file will send confirmation email for client and cleaner
import sched
import smtplib
import os
import datetime as dt
import time

from dotenv import dotenv_values
temp = dotenv_values(".env")
password = temp["passw"] 



# def testEmail(client, cleaner, schedule):
#     print("**************************************")
#     print(client , cleaner, schedule["start"] + " - ",schedule["end"] + " on ",schedule["date"]);
#     print("**************************************")

def sendConfirmationEmail(client, cleaner, schedule):
    print(schedule["date"].split("-")[0])
    print(schedule["date"].split("-")[1])
    print(schedule["date"].split("-")[2])


    print(int(schedule["start"].split(":")[0]) - 2)

    gmail_user = 'karanpreetsodhi1997@gmail.com'
    gmail_password = password

    sent_from = gmail_user
    to = [client,cleaner]
    subject = 'Testing 123'
    body = f'This is a CONFIRMATION email for the scheduled Cleaning shift on {schedule["date"]} starting at {schedule["start"]} for {schedule["end"]} hours.'

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
        print ("Email sent successfully!")

        to = [cleaner]
        body = f'This is a REMINDER email for the scheduled Cleaning shift on {schedule["date"]} starting at {schedule["start"]} for {schedule["end"]} hours.'

        email_text = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (sent_from, ", ".join(to), subject, body)
        #scheduling reminder email
        send_time = dt.datetime(int(schedule["date"].split("-")[0]),int(schedule["date"].split("-")[1]),int(schedule["date"].split("-")[2]),int(schedule["start"].split(":")[0]) - 2,int(schedule["start"].split(":")[1]),0) # set your sending time in UTC
        time.sleep(send_time.timestamp() - time.time())


        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print ("Reminder Email sent successfully!")

        smtp_server.close()

    except Exception as ex:
        print ("Something went wrong….",ex)
