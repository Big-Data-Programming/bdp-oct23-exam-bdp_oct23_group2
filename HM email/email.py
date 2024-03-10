import os
import re
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText

SENDER = os.getenv('HH_SENDER_EMAIL')
PASSWORD = os.getenv('HH_EMAIL_ID_PASSWORD')


def send_email(receiver, subject, body):
    message = MIMEText(body, "html")
    message["From"] = SENDER
    message["To"] = receiver
    message["Subject"] = subject

    try:
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.ehlo()

        smtp_server.starttls()
        smtp_server.ehlo()
        smtp_server.login(SENDER, PASSWORD)

        smtp_server.sendmail(SENDER, receiver, message.as_string())

        smtp_server.quit()

        print(f"Successfully sent email to {receiver}")
    except Exception as e:
        print(f"Unsuccessful in sending email. Error: {e}.")


def create_email(display_name):
    email_id = re.sub(r'[^\w\s]', '_', display_name)
    email_id = re.sub(r'\s', '_', email_id)

    email_id = email_id + "@yopmail.com"

    return email_id.lower()


def send_exam_link(account_id, email_id):
    new_time = datetime.now() + timedelta(days=1)

    subject = 'Congratulations...!!!'

    test_link = f"http://localhost:63342/bdp_oct_2022-group_04/views/coding.html?account_id={account_id}" \
                f"&time_limit={round(new_time.timestamp())}"

    message = f'''\
               <html>
                   <head></head>
                   <body>
                       Hello Candidate,
                       <p>We are glad to inform you that you have been shortlisted to attend a coding challenge.</p>
                       <p>Click this link to attempt a coding challenge: <u><a href="{test_link}">Click Here</a></u></p>
                       <br>
                       <p>Thanks and regards</p>
                       <p>Doodle Dude</p>
                   </body>
               </html> 
               '''

    send_email(email_id, subject, message)


def send_interview_invitation(email_id):
    meeting_time = datetime.now() + timedelta(days=15)

    subject = 'Congratulations on passing the coding challenge.'

    meeting_link = "https://www.microsoft.com/en/microsoft-teams/log-in"

    message = f'''\
               <html>
                   <head></head>
                   <body>
                       Hello Candidate,
                       <p>We are glad to inform you that you have cleared the coding challenge.</p>
                       <p>
                           The interview will be held on {meeting_time.strftime('%Y-%m-%d')}
                           from 10:00 to 10:30.
                       </p>
                       <p>Interview Link: <u><a href="{meeting_link}" target="_blank">Join meeting</a></u></p>
                       <p>Thanks and regards</p>
                       <p>Doodle Dude</p>
                   </body>
               </html> 
               '''

    send_email(email_id, subject, message)


def send_test_response(email_id):
    subject = 'Thank you for your time.'

    message = f'''\
               <html>
                   <head></head>
                   <body>
                       Hello Candidate,
                       <p>We are sorry to inform you that you have not cleared the coding challenge.</p>
                       <p>Better luck next time.</p>
                       <p>Thanks and regards</p>
                       <p>Doodle Dude</p>
                   </body>
               </html> 
               '''

    send_email(email_id, subject, message)


if __name__ == '__main__':
    to = 'praveenbm1997@gmail.com'

    send_exam_link("1", to)
    send_interview_invitation(to)
    send_test_response(to)