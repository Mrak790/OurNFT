from django import forms

from .models import Image


class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Image
        fields = ['image', 'text', 'visibility']
        # exclude = ['owner']


from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ['author']

