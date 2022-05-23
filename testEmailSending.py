import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email='aviadm32@gmail.com',
    to_emails='aviadm24@gmail.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient("os.environ.get('SENDGRID_API_KEY')")
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)


# import requests
# creds = []
# try:
#     with open("mailgun.txt", "r") as f:
#         for line in f.readlines():
#             creds.append(line)
#     EMAIL_HOST = creds[0].strip()
#     EMAIL_PORT = creds[1].strip()
#     EMAIL_HOST_USER = creds[2].strip()
#     EMAIL_HOST_PASSWORD = creds[3].strip()
#     TEST_API_KEY = creds[3].strip()
# except FileNotFoundError:
#     print("no mailgun.txt file found!")
#
#
# def send_simple_message():
#     return requests.post(
#         "https://api.mailgun.net/v3/toracomments.com/messages",
#         auth=("api", TEST_API_KEY),
#         data={"from": "Excited User <mailgun@toracomments.com>",
#               "to": ["aviadm24@gmail.com", "YOU@toracomments.com"],
#               "subject": "Hello",
#               "text": "Testing some Mailgun awesomness!"})
#
# # res = send_simple_message()
# # print(res)
# import smtplib, ssl
#
#
# message = """\
# Subject: Test from Python
# To: aviadm24@gmail.com
# From: email@www.torracomments.com
#
# This message is sent from Python."""
#
# server = smtplib.SMTP(hostname, 587)
# server.ehlo() # Can be omitted
# server.starttls(context=ssl.create_default_context()) # Secure the connection
# server.login(username, password)
# ans = server.sendmail("email@www.torracomments.com", "aviadm24@gmail.com", message)
# print(ans)
# server.quit