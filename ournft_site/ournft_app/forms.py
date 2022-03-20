from django import forms

from .models import Image


class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Image
        fields = ['image', 'text', 'visibility']


class RestoreImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'secret']
    
