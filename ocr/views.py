from django.shortcuts import render, redirect
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
from .forms import TaharaImageForm
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from io import StringIO
from PIL import Image
import json
from .ocr_functions import data, word_list_dict, heb_digit


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
            return render(request, 'ocr/taharaImage_list.html')
        else:
            print("errors: ", form.errors)
            return render(request, 'ocr/taharaImage_create.html', {'form': form})
    else:
        form = TaharaImageForm()
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        qs = TaharaImage.objects.filter(rabbi_name=self.request.user)
        number_of_edim_uploaded = context['number_of_edim_uploaded'] = qs.count()
        qs = TaharaImage.objects.filter(rabbi_name=self.request.user). \
            filter(release_date__lte=datetime.now() - timedelta(days=30))
        if number_of_edim_uploaded > qs.count():
            context['additional_explanation'] = 'עדיין לא עבר הזמן המוגדר במערכת למרווח בין הפסיקה הראשונה והשניה לגבי עדים'
        # form = TaharaImageForm()
        # context['form'] = form
        return context

    def get_queryset(self):
        qs = TaharaImage.objects.filter(rabbi_name=self.request.user).\
            filter(release_date__lte=datetime.now() - timedelta(days=0))
        for t_image in qs:
            logo = t_image.logo
            t_image.logo = logo[2:-1]
            t_image.first_pesak = TaharaImage.pesak_in_hebrew(t_image.first_pesak)
            # print("logo: ", t_image.logo)
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

