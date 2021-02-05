from django.shortcuts import render, redirect
import pytesseract
from PIL import Image
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
import difflib
import os
# from dateutil.parser import parse
from django.conf import settings
from django.http import JsonResponse, HttpResponse

import json
from .ocr_functions import data, word_list_dict, heb_digit


# def is_date(string, fuzzy=False):
#     """
#     Return whether the string can be interpreted as a date.
#
#     :param string: str, string to check for date
#     :param fuzzy: bool, ignore unknown tokens in string if True
#     """
#     try:
#         parse(string, fuzzy=fuzzy)
#         return True
#
#     except ValueError:
#         return False


#  https://guides.gdpicture.com/content/Affecting%20Tesseract%20OCR%20engine%20with%20special%20parameters.html
INVOICE_WORD_LIST = ["קבלה", "חשבונית"]


def home(request):
    return render(request, template_name='ocr/home.html')


def plain_ocr(handler, lang):
    text = pytesseract.image_to_string(handler, lang=lang)  # 'eng+heb'
    return text


def digits(handler):
    text = pytesseract.image_to_string(handler, config='digits')
    return text


def close_match(text):
    answers = []
    word_list = text.split()
    # print(word_list)
    for invoice_kind in INVOICE_WORD_LIST:
        found = difflib.get_close_matches(invoice_kind, word_list)
        # print('difflib: ', found)
        for f in found:
            found_indexs = [i for i, val in enumerate(word_list) if val == f]
            for indx in found_indexs:
                for word in word_list[indx: indx + 5]:
                    # print('invoice: ', word)
                    if any(char.isdigit() for char in word):
                        # if is_date(word):
                        #     answers.append(('קשור לתאריך '+invoice_kind, word))
                        # elif len(word) > 4:
                        #     answers.append((invoice_kind, word))
                        if len(word) > 4:
                            answers.append((invoice_kind, word))
    # print(answers)
    return answers

    # return difflib.get_close_matches(INVOICE_WORD_LIST, word_list)
import base64
import re
from io import StringIO
from PIL import Image

# https://stackoverflow.com/questions/53363547/how-to-deploy-pytesseract-to-heroku
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
        if file.name.endswith("png"):
            handler = Image.open(file)
            encoded_string = base64.b64encode(file.read()).decode('utf8')
            # print(encoded_string)
            try:
                text = plain_ocr(handler, 'heb')
            except:
                text = ''
        else:
            text = file.read().decode('utf8')
            print("text: ", text)
            encoded_string = ''
        return render(request, 'ocr/image_upload.html', {
            'text': text,
            'base64': encoded_string
            })

    return render(request, 'ocr/image_upload.html')

@csrf_exempt
def merge(request):
    if request.is_ajax():
        image_file = os.listdir('ocr/static/images/')
        uploaded_file_url = os.path.join('ocr/static/images/', image_file[0])
        merge = heb_digit(uploaded_file_url)
        print('merge \n:', merge)
        json_response = {'merge': merge}

        return HttpResponse(json.dumps(json_response),
                            content_type='application/json')


def get_params(request):
    image_file = os.listdir('ocr/static/images/')
    uploaded_file_url = os.path.join('ocr/static/images/', image_file[0])
    print('uploaded_file_url: ', uploaded_file_url)
    answers = data(uploaded_file_url)
    #  https://stackoverflow.com/questions/8018973/how-to-iterate-through-dictionary-in-a-dictionary-in-django-template
    return render(request, 'ocr/image_upload.html', {
        'answers': answers
            })


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

