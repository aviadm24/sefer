from django.forms import ModelForm
from django import forms
from .models import TaharaImage


class TaharaImageForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(TaharaImageForm, self).__init__(*args, **kwargs)

    class Meta:
        model = TaharaImage
        exclude = ['rabbi_name', 'release_date', 'logo', 'showed_to', 'second_pesak']
        labels = {
            "rabbi_name": "שם הרב",
            "first_pesak": "פסק",
            "logo_image": "העלה תמונה",
            "second_pesak": "פסק",
        }
