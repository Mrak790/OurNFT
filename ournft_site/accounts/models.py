from django.db import models
from ournft_app.models import Image

# Create your models here.

from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=u"User")
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name=u"Info")
    avatar = models.OneToOneField(Image, on_delete=models.CASCADE, verbose_name=u"Avatar", null=True)

    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return "{}'s profile".format(self.user.__str__())


