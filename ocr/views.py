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
from .models import TaharaImage
from django.contrib.auth.models import User
from .forms import TaharaImageForm
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from io import StringIO
from PIL import Image
import json
from .ocr_functions import data, word_list_dict, heb_digit
from cloudinary.forms import cl_init_js_callbacks
import six
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

MIN_WAITING_TIME = 0


def send_email(user):
    subject = "מחקר מראות מכון פועה"
    from_email, to = None, user.email
    text_content = 'Text'
    html_content = render_to_string(
        'ocr/email.html')
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print('sending mail')
    # send_mail(
    #     'מחקר מראות מכון פועה',
    #     'Here is the message.',
    #     'from@example.com',
    #     [user.email],
    #     fail_silently=False,
    # )


@login_required(redirect_field_name='account_login')
def TaharaImageCreateView(request):
    # print("method: ", request.method)
    if request.method == 'POST':
        # print("request.POST: ", request.POST)
        # print("request.FILES: ", request.FILES)
        form = TaharaImageForm(request.POST, request.FILES)
        if form.is_valid():
            tahara_image = form.save(commit=False)
            tahara_image.rabbi_name = request.user
            tahara_image.save()
            # return render(request, 'ocr/taharaImage_list.html')
            return redirect('TaharaImageListView')
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


class TaharaImageListView(ListView):
    model = TaharaImage
    paginate_by = 100  # if pagination is desired
    template_name = 'ocr/taharaImage_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        qs = TaharaImage.objects.filter(rabbi_name=self.request.user)
        number_of_edim_uploaded = context['number_of_edim_uploaded'] = qs.count()
        qs = TaharaImage.objects.filter(rabbi_name=self.request.user). \
            filter(release_date__lte=datetime.now() - timedelta(days=MIN_WAITING_TIME)).filter(second_pesak__exact=None)
        if number_of_edim_uploaded > qs.count():
            context['additional_explanation'] = 'עדיין לא עבר הזמן המוגדר במערכת למרווח בין הפסיקה הראשונה והשניה לגבי עדים'
        # form = TaharaImageForm()
        # context['form'] = form
        return context

    def get_queryset(self):
        qs = TaharaImage.objects.filter(rabbi_name=self.request.user).\
            filter(release_date__lte=datetime.now() - timedelta(days=MIN_WAITING_TIME)).filter(second_pesak__exact=None)
        for t_image in qs:
            # logo = t_image.logo
            # t_image.logo = logo[2:-1]
            t_image.first_pesak = TaharaImage.pesak_in_hebrew(t_image.first_pesak)
            print("second_pesak: ", t_image.second_pesak)
            if t_image.second_pesak:
                t_image.second_pesak = TaharaImage.pesak_in_hebrew(t_image.second_pesak)
        return qs


class TaharaImageUpdateView(UpdateView):
    model = TaharaImage
    fields = ['second_pesak']  # fields / if you want to select all fields, use "__all__"
    template_name = 'ocr/taharaImage_update.html'
    success_url = '/ocr/list_image'


def home(request):
    return render(request, template_name='ocr/home.html')


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