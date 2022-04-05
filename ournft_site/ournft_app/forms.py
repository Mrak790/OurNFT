from tabnanny import verbose
from django import forms

from .models import Image

from captcha.fields import CaptchaField
from django.contrib.auth.models import User

class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Image
        fields = ['image', 'text', 'visibility']


class RestoreImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'secret']
    
class CaptchaForm(forms.Form):
    captcha = CaptchaField()

class TransferForm(forms.Form):
    recipient = forms.ModelChoiceField(queryset = User.objects.none(), label="Give to")
    image_hash = forms.ModelChoiceField(queryset = Image.objects.none(),label="Image")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TransferForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['recipient'].queryset = User.objects.exclude(pk = user.pk)
            self.fields['image_hash'].queryset = Image.objects.filter(owner=user)
        
        
        
