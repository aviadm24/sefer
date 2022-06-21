from django.shortcuts import render, redirect
from django.template.loader import render_to_string
import pytesseract
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
import difflib
import os
from django.conf import settings
from django.http import JsonResponse, HttpResponse
import base64
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from datetime import timedelta, datetime
from django.views.generic import TemplateView, CreateView
from .models import TaharaImage, Answers
from django.contrib.auth.models import User
from .forms import TaharaImageForm
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from io import StringIO
from PIL import Image
import json
from .ocr_functions import data, word_list_dict, heb_digit
from cloudinary.forms import cl_init_js_callbacks
import six
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
import urllib.parse as pr
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
import clicksend_client
from clicksend_client import SmsMessage, MmsMessage
from clicksend_client.rest import ApiException
from pprint import pprint
import ast


def send_mail(user):
    context = {
        'image_url': "image_url",
    }
    message = Mail(
        from_email='aviadm32@gmail.com',
        to_emails=user.email,
        subject="מחקר מראות מכון פועה",
        html_content=render_to_string('ocr/email.html', context))
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

MIN_WAITING_TIME = 1


# def send_email(user):
#     subject = "מחקר מראות מכון פועה"
#     from_email, to = None, user.email
#     text_content = 'Text'
#     html_content = render_to_string(
#         'ocr/email.html')
#     msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()
#     print('sending mail')


def image_to_color_percentage(image_file):
    img = Image.open(image_file)
    size = w, h = img.size
    pixel_num = {
        'redAVG': 0,
        'dark<40': 0,
        '240<red<255,green<40,blue<40': 0,
        '240<red<255,green<100,blue<40': 0,
        '240<red<255,green<150,blue<40': 0,
        '220<red<240,green<40,blue<40': 0,
        '220<red<240,green<100,blue<40': 0,
        '220<red<240,green<150,blue<40': 0,
        '200<red<220,green<40,blue<40': 0,
        '200<red<220,green<100,blue<40': 0,
        '200<red<220,green<150,blue<40': 0,
    }
    # https: // stackoverflow.com / questions / 47520048 / how - to - count - bright - pixels - in -an - image
    # https://stackoverflow.com/questions/50545192/count-different-colour-pixels-python
    for pixel in img.getdata():
        r = pixel[0]
        g = pixel[1]
        b = pixel[2]
        color = ''
        brightness = ''
        avg = (r + g + b) / 3
        if r != 0:
            if avg / r < 0.9:
                pixel_num['redAVG'] += 1
        if b < 40:
            if g < 40:
                if r < 40:
                    pixel_num['dark<40'] += 1
                elif 240 < r < 255:
                    pixel_num['240<red<255,green<40,blue<40'] += 1
                elif 220 < r < 240:
                    pixel_num['220<red<240,green<40,blue<40'] += 1
                elif 200 < r < 220:
                    pixel_num['200<red<220,green<40,blue<40'] += 1
            elif g < 100:
                if 240 < r < 255:
                    pixel_num['240<red<255,green<100,blue<40'] += 1
                elif 220 < r < 240:
                    pixel_num['220<red<240,green<100,blue<40'] += 1
                elif 200 < r < 220:
                    pixel_num['200<red<220,green<100,blue<40'] += 1
            elif g < 150:
                if 240 < r < 255:
                    pixel_num['240<red<255,green<150,blue<40'] += 1
                elif 220 < r < 240:
                    pixel_num['220<red<240,green<150,blue<40'] += 1
                elif 200 < r < 220:
                    pixel_num['200<red<220,green<150,blue<40'] += 1
        # else if avg < 80 then brightness = 'dark'
        # else if avg > 220 then brightness = 'white'
        # else if avg > 150 then brightness = 'light'
        # if avg / r > 0.9 then hue = 'red'
    pixel_avg = {}
    pixel_total = w*h
    for k, v in pixel_num.items():
        if v > 0:
            pixel_avg[k] = v/pixel_total
        # print('k: ', k, ' v: ', v)

    return dict(size=size, pixel_num=pixel_num, pixel_avg=pixel_avg)  # , pix_val=pix_val


# @login_required(redirect_field_name='account_login')
@permission_required('ocr.add_taharaimage', raise_exception=True)  # , login_url='/accounts/login/'
def TaharaImageCreateView(request):
    # print("method: ", request.method)
    if request.method == 'POST':
        form = TaharaImageForm(request.POST, request.FILES)
        if form.is_valid():
            tahara_image = form.save(commit=False)
            # image1 = image_to_color_percentage(tahara_image.image)
            # tahara_image.color_percentage = dict(image1=image1)
            tahara_image.save()
            return render(request, 'ocr/taharaImage_list.html')
            # return redirect('TaharaImageListView')
        else:
            print("errors: ", form.errors)
            return render(request, 'ocr/taharaImage_create.html', {'form': form})
    else:
        form = TaharaImageForm()
        for user in User.objects.all():
            print('user name: ', user.email)
            qs = TaharaImage.objects.filter(rabbi_name=user). \
            filter(release_date__lte=datetime.now() - timedelta(days=MIN_WAITING_TIME)).filter(second_pesak__exact=None)
            print('yesterdy: ', timezone.now()-timedelta(days=1))
            print('last login: ', user.last_login)
            print('qs.count() : ', qs.count())
            if qs.count() > 0:
                if user.last_login:
                    if user.last_login < timezone.now()-timedelta(days=1):
                        # send_email(user)
                        user.last_login = timezone.now()
                        user.save(update_fields=['last_login'])
                else:
                    user.last_login = timezone.now()
                    user.save(update_fields=['last_login'])
    return render(request, 'ocr/taharaImage_create.html', {'form': form})

# class TaharaImageCreateView(CreateView):
#     # model = TaharaImage
#     form_class = TaharaImageForm
#     template_name = 'ocr/taharaImage_create.html'
#     success_url = reverse_lazy('TaharaImageListView')

    # def get_form_kwargs(self):
    #     kwargs = {'rabbi_name': self.request.user, }
    #     print("kwargs: ", kwargs)
    #     return kwargs


class TaharaImageListView(PermissionRequiredMixin, ListView):
    permission_required = 'ocr.add_taharaimage'
    model = TaharaImage
    # paginate_by = 100  # if pagination is desired
    template_name = 'ocr/taharaImage_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        print('now:', context['now'])
        qs = TaharaImage.objects.filter(rabbi_name=self.request.user)
        number_of_edim_uploaded = context['number_of_edim_uploaded'] = qs.count()
        print('number_of_edim_uploaded:', number_of_edim_uploaded)
        if number_of_edim_uploaded > qs.count():
            context['additional_explanation'] = 'עדיין לא עבר הזמן המוגדר במערכת למרווח בין הפסיקה הראשונה והשניה לגבי עדים'
        print('qs.count(): ', qs.count())
        return context

    def get_queryset(self):
        qs = TaharaImage.objects.filter(rabbi_name=self.request.user).\
            filter(release_date__lte=datetime.now() - timedelta(days=MIN_WAITING_TIME)).filter(second_pesak__exact=None)
        return qs


class TaharaImageUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'ocr.add_taharaimage'
    model = TaharaImage
    fields = ['second_pesak', 'user_agent']  # fields / if you want to select all fields, use "__all__"
    template_name = 'ocr/taharaImage_update.html'
    success_url = '/ocr/list_image'


def send_email(request):
    # t = TaharaImage()
    image_url = TaharaImage.objects.first().image.url
    context = {
        'image_url': image_url,
        'image_id':  TaharaImage.objects.first().id
    }
    print(image_url)
    message = Mail(
        from_email='aviadm32@gmail.com',
        to_emails='aviadm24@gmail.com',
        subject="מחקר מראות מכון פועה",
        html_content=render_to_string('ocr/email.html', context))
    try:
        try:
            print(os.getcwd())
            with open('sendgrid_key.txt', 'r') as f:
                key = f.readline()
            print('key: ', key)
            sg = SendGridAPIClient(key)
        except:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
    print('sending mail')
    return render(request, template_name='ocr/email.html')


def home(request):
    return render(request, template_name='ocr/home.html')


def get_image_id(data):
    parsed_message = pr.unquote(data["originalmessage"])
    print("parsed_message: ", parsed_message)
    answer = pr.unquote(data["message"]).strip()
    print("answer: ", answer)
    if not answer.isdigit():
        answer = None
    split_message = parsed_message.split('\n')
    image_id = split_message[1].split('#')[1].strip()
    if not image_id.isdigit():
        image_id = None

    return image_id, answer

#  https://developers.clicksend.com/docs/rest/v3/#view-inbound-sms
@csrf_exempt
def incoming_sms(request):
    if request.method == "POST":
        # parse body and get SMS data (id, status)
        post_body_uft8 = request.body.decode("utf-8")
        data = dict(pr.parse_qsl(post_body_uft8))
        print("*** Testing new API ***")
        # print(post_body_uft8)
        print(data)
        print("*** End Test ***")
        image_id, answer = get_image_id(data)
        if image_id and answer in ["1", "2", "3", "4", "5"]:
            print("Incoming SMS with ID: {}, answer: {}".format(image_id, answer))
            answers_choice = Answers.objects.get(pk=int(answer))
            TaharaImage.objects.filter(id=int(image_id)).update(second_pesak=answers_choice, showed_to="sms")
            print("update success")
        else:
            print("Invalid SMS")
            return HttpResponse("")

        return HttpResponse("")


def incoming_answer_from_email(request):
    if request.method == "GET":
        print(request)
        print(request.GET)
        print(request.GET.items())
        image_id = request.GET["id"]
        answer = request.GET["answer"]
        print(image_id)
        print(answer)
        print(type(answer))
        if image_id and answer in ["1", "2", "3", "4", "5"]:
            print("Incoming email with ID: {}, answer: {}".format(image_id, answer))
            answers_choice = Answers.objects.get(pk=int(answer))
            TaharaImage.objects.filter(id=int(image_id)).update(second_pesak=answers_choice, showed_to="email")
            print("update success")
        else:
            print("Invalid email")
            return HttpResponse("חלה שגיאה התשובה לא התקבלה")

        return HttpResponse("תשובתך התקבלה בהצלחה תודה")


def test_sms(request):
    print("test sms")
    if request.GET:
        print("test get")
        try:
            configuration = clicksend_client.Configuration()
            configuration.username = os.environ.get('CLICKSEND_USERNAME', '')
            configuration.password = os.environ.get('CLICKSEND_PASSWORD', '')
            api_instance = clicksend_client.SMSApi(clicksend_client.ApiClient(configuration))

            def send_sms(image_url, image_id, rabbi_phone_num):
                sms_message = SmsMessage(source="toracomments",
                                         body="{}\nimage_id#{}\n 1 טמא ברור \n2 טמא מסובך\n3 טהור מסובך\n4 טהור ברור\n5 פצע".
                                         format(image_url, image_id),
                                         to="+972{}".format(rabbi_phone_num))

                sms_messages = clicksend_client.SmsMessageCollection(messages=[sms_message])
                try:
                    # Send sms message(s)
                    api_response = api_instance.sms_send_post(sms_messages)
                    print(api_response)
                except ApiException as e:
                    print("Exception when calling SMSApi->sms_send_post: %s\n" % e)
            user = request.user
            qs = TaharaImage.objects.filter(rabbi_name=user).filter(second_pesak__exact=None)

            send_sms(qs[0].image.url, qs[0].id, user.first_name)
            print(f"sent sms to {user} at number {user.first_name}")
            return HttpResponse(f" סמס בדיקה נשלח ל{user.first_name}  {user}  תודה")
        except:
            print("an error accoured")
            return HttpResponse(f"חלה תקלה הסמס {user.first_name}  {user} לא נשלח!")
    else:
        print('not get')
        try:
            configuration = clicksend_client.Configuration()
            configuration.username = os.environ.get('CLICKSEND_USERNAME', '')
            configuration.password = os.environ.get('CLICKSEND_PASSWORD', '')
            api_instance = clicksend_client.SMSApi(clicksend_client.ApiClient(configuration))

            def send_sms(image_url, image_id, rabbi_phone_num):
                sms_message = SmsMessage(source="toracomments",
                                         body="{}\nimage_id#{}\n 1 טמא ברור \n2 טמא מסובך\n3 טהור מסובך\n4 טהור ברור\n5 פצע".
                                         format(image_url, image_id),
                                         to="+972{}".format(rabbi_phone_num))

                sms_messages = clicksend_client.SmsMessageCollection(messages=[sms_message])
                try:
                    # Send sms message(s)
                    api_response = api_instance.sms_send_post(sms_messages)
                    print(api_response)
                except ApiException as e:
                    print("Exception when calling SMSApi->sms_send_post: %s\n" % e)
            user = request.user
            qs = TaharaImage.objects.filter(rabbi_name=user).filter(second_pesak__exact=None)

            send_sms(qs[0].image.url, qs[0].id, user.first_name)
            print(f"sent sms to {user} at number {user.first_name}")
            return HttpResponse(f" סמס בדיקה נשלח ל{user.first_name}  {user}  תודה")
        except:
            print("an error accoured")
            return HttpResponse(f"חלה תקלה הסמס {user.first_name}  {user} לא נשלח!")
    return HttpResponse(f"error")

@csrf_exempt
def image_upload(request):
    if request.is_ajax():
        image_file = os.listdir('ocr/static/images/')
        uploaded_file_url = os.path.join('ocr/static/images/', image_file[0])
        print('uploaded_file_url: ', uploaded_file_url)
        answers = data(uploaded_file_url)
        print(answers)
        json_response = {'answers': answers}

        return HttpResponse(json.dumps(json_response),
                            content_type='application/json')

    if request.method == 'POST' and request.FILES['image']:
        file = request.FILES['image']
        try:
            handler = Image.open(file)
            encoded_string = base64.b64encode(file.read()).decode('utf8')
            # print(encoded_string)
            try:
                text = plain_ocr(handler, 'heb')
            except:
                text = ''
        except:
            text = file.read().decode('utf8')
            print("text: ", text)
            encoded_string = ''
        response = {
            'text': text,
            'base64': encoded_string
        }
        return JsonResponse(response)
        # return render(request, 'ocr/image_upload.html', {
        #     'text': text,
        #     'base64': encoded_string
        #     })

    return render(request, 'ocr/upload_form.html')

@csrf_exempt
def ocr_output(request):
    if request.method == 'POST' and request.FILES['image']:
        myfile = request.FILES['image']
        # print(myfile)
        image = Image.open(myfile)
        text = plain_ocr(image, 'heb')
        data = {"ocr-text": text}
        # json_data = json.dumps(data, ensure_ascii=False).encode('utf8')
        return JsonResponse(json.dumps(data, ensure_ascii=False), safe=False)

    return render(request, 'ocr/ocr_output.html')


def filter_nones(d):
    return dict((k, v) for k, v in six.iteritems(d) if v is not None)


def cloudinary_list(request):
    defaults = dict(format="jpg", height=150, width=150)
    defaults["class"] = "thumbnail inline"

    # The different transformations to present
    samples = [
        dict(crop="fill", radius=10),
        dict(crop="scale"),
        dict(crop="fit", format="png"),
    ]
    samples = [filter_nones(dict(defaults, **sample)) for sample in samples]
    for img in TaharaImage.objects.all():
        print(img.image)
    return render(request, 'ocr/cloudinary_list.html', dict(photos=TaharaImage.objects.all(), samples=samples))


def upload(request):
    unsigned = request.GET.get("unsigned") == "true"

    if (unsigned):
        # For the sake of simplicity of the sample site, we generate the preset on the fly.
        # It only needs to be created once, in advance.
        try:
            api.upload_preset(PhotoUnsignedDirectForm.upload_preset_name)
        except api.NotFound:
            api.create_upload_preset(name=PhotoUnsignedDirectForm.upload_preset_name, unsigned=True,
                                     folder="preset_folder")

    direct_form = PhotoUnsignedDirectForm() if unsigned else PhotoDirectForm()
    context = dict(
        # Form demonstrating backend upload
        backend_form=PhotoForm(),
        # Form demonstrating direct upload
        direct_form=direct_form,
        # Should the upload form be unsigned
        unsigned=unsigned,
    )
    # When using direct upload - the following call is necessary to update the
    # form's callback url
    cl_init_js_callbacks(context['direct_form'], request)

    if request.method == 'POST':
        # Only backend upload should be posting here
        form = PhotoForm(request.POST, request.FILES)
        context['posted'] = form.instance
        if form.is_valid():
            # Uploads image and creates a model instance for it
            form.save()

    return render(request, 'upload.html', context)


def direct_upload_complete(request):
    form = PhotoDirectForm(request.POST)
    if form.is_valid():
        # Create a model instance for uploaded image using the provided data
        form.save()
        ret = dict(photo_id=form.instance.id)
    else:
        ret = dict(errors=form.errors)

    return HttpResponse(json.dumps(ret), content_type='application/json')