from django.forms import ModelForm
from django import forms
from .models import Ycomment


class YcommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(YcommentForm, self).__init__(*args, **kwargs)
        # self.fields['url'].widget.attrs = {'value': '{{request.get_full_path}}', }

    class Meta:
        model = Ycomment
        fields = ['comment']  # , 'url'
        # widgets = {'url': forms.URLField(attrs={'value': '{{request.get_full_path}}'} )
        #            }

