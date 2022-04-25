from django import forms

from .models import Image, Comment, Report

from captcha.fields import CaptchaField
from django.contrib.auth.models import User
from django.utils.html import format_html


class ImageChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return format_html('<img src="{}" alt="connect" style="max-height:80px">', obj.image.url)  

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
            self.fields['recipient'].queryset = User.objects.exclude(pk = user.pk).exclude(username='AnonymousUser')
            self.fields['image_hash'].queryset = Image.objects.filter(owner=user)
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]

class ReportForm(forms.ModelForm):
    class Meta:
        model= Report
        fields = ['link','text']

class BanUserForm(forms.Form):
    user = forms.ModelChoiceField(queryset = User.objects.none(), label="Ban user")
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(BanUserForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].queryset = User.objects.exclude(pk = user.pk).exclude(username='AnonymousUser').filter(is_staff=False)

class TokenRestoreForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image_hash', 'secret']

class ModerTokenRestoreForm(forms.ModelForm):

    user = forms.ModelChoiceField(queryset = User.objects.exclude(username='AnonymousUser'), label="User")
    
    class Meta:
        model = Image
        fields = ['image_hash', 'secret']
    