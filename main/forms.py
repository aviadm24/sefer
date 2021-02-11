from django.forms import ModelForm
from django import forms
from .models import Ycomment, Yfiles


class YcommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(YcommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs = {'dir': 'auto'}

    class Meta:
        model = Ycomment
        fields = ['comment', 'comment_reference', 'url']  # , 'url'
        # widgets = {'url': forms.URLField(attrs={'value': '{{request.get_full_path}}'} )
        #            }



class YfilesForm(ModelForm):

    class Meta:
        model = Yfiles
        fields = '__all__'

class FileUploadForm(forms.Form):

    file = forms.FileField()

    def clean_file(self):
        data = self.cleaned_data["file"]
        print("data: ", data)
        # read and parse the file, create a Python dictionary `data_dict` from it
        form = YfilesForm(data)
        if form.is_valid():
            # we don't want to put the object to the database on this step
            self.instance = form.save(commit=False)
        else:
            # You can use more specific error message here
            raise forms.ValidationError(u"The file contains invalid data.")
        return data

    def save(self):
        # We are not overriding the `save` method here because `form.Form` does not have it.
        # We just add it for convenience.
        instance = getattr(self, "instance", None)
        if instance:
            instance.save()
        return instance

