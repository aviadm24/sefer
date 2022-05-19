from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from ocr.models import TaharaImage, WaitTime
from datetime import timedelta, datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(user):
    message = Mail(
        from_email='aviadm32@gmail.com',
        to_emails='aviadm24@gmail.com',
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

    # subject = "מחקר מראות מכון פועה"
    # from_email, to = "email@www.torracomments.com", user.email
    # text_content = 'Text'
    # html_content = render_to_string(
    #     'ocr/email.html')
    # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    # msg.attach_alternative(html_content, "text/html")
    # msg.send(fail_silently=False)
    # print('sending mail')


# https://devcenter.heroku.com/articles/scheduling-custom-django-management-commands
class Command(BaseCommand):
    help = 'sends email to all users if 7 days passed'

    # https://stackoverflow.com/questions/41401202/django-command-throws-typeerror-handle-got-an-unexpected-keyword-argument
    def handle(self, *args, **options):
        # try:
        for user in User.objects.all():
            if user.email in ['aviadm24@gmail.com']:
                send_email(user)
        self.stdout.write(self.style.SUCCESS('sent email'))
        # except:
        #     self.stdout.write(self.style.ERROR('an exception has acourred'))
        #     return

        self.stdout.write(self.style.SUCCESS('Successfully sent email'))
        return