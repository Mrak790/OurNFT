from dataclasses import fields
from tabnanny import verbose
from django import forms

from .models import Image, Comment

from captcha.fields import CaptchaField
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.html import format_html


class ImageChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return format_html('<img src="{}" alt="connect" style="max-height:100px">', obj.image.url)  

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
    image_hash = ImageChoiceField(queryset = Image.objects.none(),label="Image",widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TransferForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['recipient'].queryset = User.objects.exclude(pk = user.pk)
            self.fields['image_hash'].queryset = Image.objects.filter(owner=user)
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]
