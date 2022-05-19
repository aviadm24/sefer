from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from ocr.models import TaharaImage, WaitTime
from datetime import timedelta, datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os


def send_mail(user):
    message = Mail(
        from_email='aviadm32@gmail.com',
        to_emails=user.email,
        subject="מחקר מראות מכון פועה",
        html_content=render_to_string('ocr/email.html') )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

# def send_email(user):
#     subject = "מחקר מראות מכון פועה"
#     from_email, to = "email@www.torracomments.com", user.email
#     text_content = 'Text'
#     html_content = render_to_string(
#         'ocr/email.html')
#     msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#     msg.attach_alternative(html_content, "text/html")
#     msg.send(fail_silently=False)
#     print('sending mail')


# https://devcenter.heroku.com/articles/scheduling-custom-django-management-commands
class Command(BaseCommand):
    help = 'sends email to all users if 7 days passed'

    # https://stackoverflow.com/questions/41401202/django-command-throws-typeerror-handle-got-an-unexpected-keyword-argument
    def handle(self, *args, **options):
        # try:
        for user in User.objects.all():
            print('user name: ', user.email)
            try:
                MIN_WAITING_TIME = WaitTime.objects.all().first().days
            except:
                MIN_WAITING_TIME = 1
            self.stdout.write(self.style.SUCCESS(f'user email: {user.email}'))
            qs = TaharaImage.objects.filter(rabbi_name=user). \
                filter(release_date__lte=datetime.now() - timedelta(days=MIN_WAITING_TIME)).filter(
                second_pesak__exact=None)
            # print('yesterdy: ', timezone.now() - timedelta(days=1))
            # print('last login: ', user.last_login)
            print('qs.count() : ', qs.count())
            self.stdout.write(self.style.SUCCESS(f'qs.count() : {qs.count()}'))
            if qs.count() > 0:
                send_email(user)

        self.stdout.write(self.style.SUCCESS('sent email'))
        # except:
        #     self.stdout.write(self.style.ERROR('an exception has acourred'))
        #     return

        self.stdout.write(self.style.SUCCESS('Successfully sent email'))
        return