from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    datetime = models.DateTimeField(verbose_name=u"Date", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=u"Author", related_name="posts")
    text = models.CharField(max_length=200, verbose_name=u"Text", null=True, blank=True)
    image = models.ImageField(verbose_name=u"Image", null=True, blank=True)

    class Meta:
        ordering = ["-datetime"]

    def __str__(self):
        return "{}'s post".format(self.author.__str__())