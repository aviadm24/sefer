from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from ocr.models import TaharaImage, WaitTime
from datetime import timedelta, datetime
import time
import os
from twilio.rest import Client


def send_whatsapp(to_number, media_url, tahara_image_id):
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID', '')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN', '')
    client = Client(account_sid, auth_token)
    # body = 'שלום אביעד זוהי תזכורת להשתתפות במחקר, ניתן לשלוח עדים'
    body = 'שלום אביעד זוהי תזכורת להשתתפות במחקר'
    message = client.messages.create(
                                body=body,
                                from_='whatsapp:+972521210174',
                                to=to_number,
                                media_url=[media_url],
                                )

    print(message.sid)


# https://devcenter.heroku.com/articles/scheduling-custom-django-management-commands
class Command(BaseCommand):
    help = 'sends whatsapp to all users if days passed'

    # https://stackoverflow.com/questions/41401202/django-command-throws-typeerror-handle-got-an-unexpected-keyword-argument
    def handle(self, *args, **options):
        # try:
        for user in User.objects.all():
            print('user name: ', user.email)
            try:
                MIN_WAITING_TIME = WaitTime.objects.all().first().days
                print('MIN_WAITING_TIME: ', MIN_WAITING_TIME)
            except:
                MIN_WAITING_TIME = 1

            qs = TaharaImage.objects.filter(rabbi_name=user). \
                filter(release_date__lte=datetime.now() - timedelta(days=MIN_WAITING_TIME)).filter(
                second_pesak__exact=None)
            # print('yesterdy: ', timezone.now() - timedelta(days=1))
            print('qs.count() : ', qs.count())
            for image in qs:
                print(image.image.url)
                # print(image.image2.url)
            print("phone: ", user.first_name)
            self.stdout.write(self.style.SUCCESS(f'qs.count() : {qs.count()}'))
            if qs.count() > 0 and user.first_name:
                send_whatsapp(user.first_name, qs[0].image.url, qs[0].id)

        self.stdout.write(self.style.SUCCESS('sent whatsapp'))
        # except:
        #     self.stdout.write(self.style.ERROR('an exception has acourred'))
        #     return

        self.stdout.write(self.style.SUCCESS('Successfully sent whatsapp'))
        return
