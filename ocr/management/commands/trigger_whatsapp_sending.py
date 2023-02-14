from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from ocr.models import TaharaImage, WaitTime, Comment
from datetime import timedelta, datetime
import time
import os
from twilio.rest import Client


def send_whatsapp(user, media_url, tahara_image_id):
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID', '')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN', '')
    client = Client(account_sid, auth_token)
    milui = "לפסוק על"
    # body = 'שלום אביעד זוהי תזכורת להשתתפות במחקר, ניתן לשלוח עדים'
    body = f""" שלום{user.username} נא {milui}תמונה \n{media_url}\n, נא לענות במס' 1 טמא ברור, 2 טמא מסובך, 3 טהור מסובך, 4 טהור ברור"""
    body = f"""שלום {user.username} נא {milui} תמונה 
{media_url}
, נא לענות במס' 1 טמא ברור, 2 טמא מסובך, 3 טהור מסובך, 4 טהור ברור"""

    message = client.messages.create(
                                body=body,
                                from_='whatsapp:+972521210174',
                                to='whatsapp:+972'+user.first_name,
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
            MIN_WAITING_TIME = 1  # to delete
            qs = TaharaImage.objects.filter(rabbi_name=user). \
                filter(release_date__lte=datetime.now() - timedelta(days=MIN_WAITING_TIME)).filter(
                second_pesak__exact=None)
            # print('yesterdy: ', timezone.now() - timedelta(days=1))
            print('qs.count() : ', qs.count())
            for image in qs:
                print(image)
                print(image.image2)
            self.stdout.write(self.style.SUCCESS(f'qs.count() : {qs.count()}'))
            if qs.count() > 0 and user.first_name == '547573120':
                print("phone: ", user.first_name)
                send_whatsapp(user, qs[0].image2, qs[0].id)

        # except:
        #     self.stdout.write(self.style.ERROR('an exception has acourred'))
        #     return
        obj, created = Comment.objects.update_or_create(
            id=1,
            choice=str(qs[0].id),
            )

        self.stdout.write(self.style.SUCCESS('Successfully sent whatsapp'))
        return
