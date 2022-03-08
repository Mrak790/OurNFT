from django import forms

from .models import Image


class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Image
        fields = ('image',)


from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ['author']

