from __future__ import print_function
import time
import os
import clicksend_client
from clicksend_client import SmsMessage
from clicksend_client.rest import ApiException
from pprint import pprint
import ast
# Configure HTTP basic authorization: BasicAuth
configuration = clicksend_client.Configuration()
configuration.username = os.environ.get('CLICKSEND_USERNAME', '')
configuration.password = os.environ.get('CLICKSEND_PASSWORD', '')

# create an instance of the API class
# api_instance = clicksend_client.AccountApi(clicksend_client.ApiClient(configuration))
api_instance = clicksend_client.SMSApi(clicksend_client.ApiClient(configuration))
# If you want to explictly set from, add the key _from to the message.
sms_message = SmsMessage(source="toracomments",
                        body="test",
                        to="+972{}".format("547573120"))

sms_messages = clicksend_client.SmsMessageCollection(messages=[sms_message])

try:
    # Send sms message(s)
    api_response = api_instance.sms_send_post(sms_messages)
    print(api_response)
except ApiException as e:
    print("Exception when calling SMSApi->sms_send_post: %s\n" % e)
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