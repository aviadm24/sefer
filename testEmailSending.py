import requests
creds = []
try:
    with open("mailgun.txt", "r") as f:
        for line in f.readlines():
            creds.append(line)
    EMAIL_HOST = creds[0].strip()
    EMAIL_PORT = creds[1].strip()
    EMAIL_HOST_USER = creds[2].strip()
    EMAIL_HOST_PASSWORD = creds[3].strip()
    TEST_API_KEY = creds[3].strip()
except FileNotFoundError:
    print("no mailgun.txt file found!")


def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/toracomments.com/messages",
        auth=("api", TEST_API_KEY),
        data={"from": "Excited User <mailgun@toracomments.com>",
              "to": ["aviadm24@gmail.com", "YOU@toracomments.com"],
              "subject": "Hello",
              "text": "Testing some Mailgun awesomness!"})

res = send_simple_message()
print(res)