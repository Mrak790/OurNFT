from tkinter import CASCADE
from wsgiref.simple_server import demo_app
from xmlrpc.client import Boolean
from django.db import models
from django.contrib.auth.models import User
import imagehash
from numpy import true_divide
# Create your models here.
DIFF_THRESHOLD = 0.2

def image_path(instance, filename):
    return f'images/{instance.image_hash}.jpg'

def diff(hash1, hash2):
    q1 = bin(int(hash1,16))[2:]
    q2 = bin(int(hash2,16))[2:]
    hamm_dist = len([1 for i,j in zip(q1,q2) if i!=j])
    print(hamm_dist/len(q1))
    return hamm_dist/len(q1)


class Image(models.Model):
    image = models.ImageField(upload_to=image_path)
    image_hash = models.CharField(max_length=64, null=True)
    ouwner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs) -> Boolean:
        
        self.image_hash = f'{imagehash.phash(imagehash.Image.open(self.image))}'
        query = Image.objects.values_list('image_hash')
        if not [i[0] for i in query if diff(i[0], self.image_hash) < DIFF_THRESHOLD]:
            super().save(*args, **kwargs)
            self.is_unique = True
        else:
            print("not unique image")
            self.is_unique = False

class Post(models.Model):
    datetime = models.DateTimeField(verbose_name=u"Date", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=u"Author", related_name="posts")
    text = models.CharField(max_length=200, verbose_name=u"Text", null=True, blank=True)
    image = models.ImageField(verbose_name=u"Image", null=True, blank=True)

    class Meta:
        ordering = ["-datetime"]

    def __str__(self):
        return "{}'s post".format(self.author.__str__())

