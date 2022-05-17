from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from ocr.models import TaharaImage, WaitTime
from datetime import timedelta, datetime
import time
import os
import clicksend_client
from clicksend_client import SmsMessage, MmsMessage
from clicksend_client.rest import ApiException
from pprint import pprint
import ast
MIN_WAITING_TIME = 1
# Configure HTTP basic authorization: BasicAuth
configuration = clicksend_client.Configuration()
configuration.username = os.environ.get('CLICKSEND_USERNAME', '')
configuration.password = os.environ.get('CLICKSEND_PASSWORD', '')
# create an instance of the API class
# api_instance = clicksend_client.AccountApi(clicksend_client.ApiClient(configuration))
api_instance = clicksend_client.SMSApi(clicksend_client.ApiClient(configuration))


def send_sms(image_url, rabbi_phone_num):
    sms_message = SmsMessage(source="toracomments",
                             body="{} \n 1 טמא ברור \n2 טמא מסובך\n3 טהור מסובך\n4 טהור ברור\n5 פצע".format(image_url),
                             to="+972{}".format(rabbi_phone_num))

    sms_messages = clicksend_client.SmsMessageCollection(messages=[sms_message])
    try:
        # Send sms message(s)
        api_response = api_instance.sms_send_post(sms_messages)
        print(api_response)
    except ApiException as e:
        print("Exception when calling SMSApi->sms_send_post: %s\n" % e)


# https://devcenter.heroku.com/articles/scheduling-custom-django-management-commands
class Command(BaseCommand):
    help = 'sends sms to all users if days passed'

    # https://stackoverflow.com/questions/41401202/django-command-throws-typeerror-handle-got-an-unexpected-keyword-argument
    def handle(self, *args, **options):
        # try:
        for user in User.objects.all():
            print('user name: ', user.email)
            try:
                MIN_WAITING_TIME = WaitTime.objects.all().first()
            except:
                MIN_WAITING_TIME = 1

            qs = TaharaImage.objects.filter(rabbi_name=user). \
                filter(release_date__lte=datetime.now() - timedelta(days=MIN_WAITING_TIME)).filter(
                second_pesak__exact=None)
            # print('yesterdy: ', timezone.now() - timedelta(days=1))
            print('qs.count() : ', qs.count())
            for image in qs:
                print(image.image.url)
                print(image.image2.url)
            print("phone: ", user.first_name)
            self.stdout.write(self.style.SUCCESS(f'qs.count() : {qs.count()}'))
            if qs.count() > 0 and user.first_name:
                send_sms(qs[0].image2.url, user.first_name)

        self.stdout.write(self.style.SUCCESS('sent sms'))
        # except:
        #     self.stdout.write(self.style.ERROR('an exception has acourred'))
        #     return

        self.stdout.write(self.style.SUCCESS('Successfully sent sms'))
        return
# try:
#     # Get account information
#     api_response = api_instance.account_get()
#     pprint(api_response)
# except ApiException as e:
#     print("Exception when calling AccountApi->account_get: %s\n" % e)
#
# sms_message = SmsMessage(source="api",
#                          body="message_body",
#                          to="+972{}".format("547573120")
#                          )
# sms_messages = clicksend_client.SmsMessageCollection(messages=[sms_message])
#
# try:
#     api_response = api_instance.sms_send_post(sms_messages)
#     print(api_response)
#     # api_response = ast.literal_eval(api_instance.sms_send_post(sms_messages))
#     # print("api response: ", api_response)
# except ApiException as e:
#     print("Exception when calling SMSApi->sms_send_post: {}\n".format(e))
#

# @csrf_exempt
# def send_sms(request):
#     if request.method == "POST":
#         data = json.loads(request.body.decode("utf-8"))
#         print("Sending SMS: {}".format(data))
#
#         sms_message = SmsMessage(source="api",
#                                  body=data["message_body"],
#                                  to="+972{}".format(data["number"]),
#                                  schedule=data["schedule"])
#         sms_messages = clicksend_client.SmsMessageCollection(messages=[sms_message])
#
#         try:
#             api_response = ast.literal_eval(api_instance.sms_send_post(sms_messages))
#             # save sms only if it is scheduled and we have project_id
#             if data["project_id"] and data["schedule"]:
#                 # first cancel any scheduled messages for this project_id
#                 cancel_sms_by_project_id(data["project_id"])
#                 # now save new scheduled sms
#                 message_id = api_response["data"]["messages"][0]["message_id"]
#                 Sms(number=data["number"], message_id=message_id, project_id=data["project_id"]).save()
#         except ApiException as e:
#             print("Exception when calling SMSApi->sms_send_post: {}\n".format(e))
#         return HttpResponse("")


# @csrf_exempt
# def cancel_sms(request):
#     if request.method == "POST":
#         data = json.loads(request.body.decode("utf-8"))
#         project_id = data["project_id"]
#         cancel_sms_by_project_id(project_id)
#         return HttpResponse("")
#
# @csrf_exempt
# def incoming_sms(request):
#     if request.method == "POST":
#         # parse body and get SMS data (id, status)
#         post_body_uft8 = request.body.decode("utf-8")
#         data = dict(pr.parse_qsl(post_body_uft8))
#         print("*** Testing new API ***")
#         print(post_body_uft8)
#         print(data)
#         print("*** End Test ***")
#         return HttpResponse("")
#         # project_id, status = get_project_id_and_message(data)
#         # update status in spreadsheet or exit if there"s a problem
#         # if id and status in ["טופל", "ממתין", "נוצר קשר", "וידוא משימה"]:
#             # print("Incoming SMS with ID: {}, Status: {}".format(project_id, status))
#             # update_spreadsheet(id=project_id, status=status)
#         # else:
#             # print("Invalid SMS")
#             # return HttpResponse("")
#
#         # if task was completed - cancel an SMS reminder (if exists)
#         # if status == "טופל":
#             # cancel_sms_by_project_id(project_id)
#         # return HttpResponse("")