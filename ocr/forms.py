from django.forms import ModelForm
from django import forms
from .models import TaharaImage
from cloudinary.forms import CloudinaryJsFileField, CloudinaryUnsignedJsFileField


class TaharaImageForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(TaharaImageForm, self).__init__(*args, **kwargs)

    class Meta:
        model = TaharaImage
        exclude = ['rabbi_name', 'release_date', 'logo', 'showed_to', 'second_pesak', 'user_agent', 'place_holder',
                   'color_percentage']
        labels = {
            "rabbi_name": "שם הרב",
            "first_pesak": "פסק",
            "logo_image": "העלה תמונה",
            "second_pesak": "פסק",
            "image": "צד עיקרי",
            "image2": "צד שני",
        }


class TaharaImageDirectForm(TaharaImageForm):
    image = CloudinaryJsFileField()
