from tabnanny import verbose
# from tkinter import CASCADE
from wsgiref.simple_server import demo_app
from xmlrpc.client import Boolean
from django.db import models
#<<<<<<< likes
from taggit.managers import TaggableManager

# Create your models here.
class IpModel(models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip

class Blog(models.Model):
    title = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=550)
    tags = TaggableManager()
    views = models.ManyToManyField(IpModel, related_name="post_views", blank=True)
    likes = models.ManyToManyField(IpModel, related_name="post_likes", blank=True)


    def __str__(self):
        return self.title

    def total_views(self):
        return self.views.count()

    def total_likes(self):
        return self.likes.count()
#=======
from django.contrib.auth.models import User
import imagehash
from numpy import true_divide
from datetime import datetime
from django.utils.timezone import make_aware
# Create your models here.
DIFF_THRESHOLD = 0.2

def image_path(instance, filename):
    return f'images/{instance.image_hash}.png'

def diff(hash1, hash2):
    q1 = bin(int(hash1,16))[2:]
    q2 = bin(int(hash2,16))[2:]
    hamm_dist = len([1 for i,j in zip(q1,q2) if i!=j])
    print(hamm_dist/len(q1))
    return hamm_dist/len(q1)


class PublicImageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(visibility=True)

class Image(models.Model):
    upload_datetime = models.DateTimeField(verbose_name="Date", auto_now_add=True)
    image = models.ImageField(upload_to=image_path,verbose_name="Image")
    image_hash = models.CharField(max_length=64,verbose_name="Token", null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Owner", related_name="images")
    text = models.CharField(max_length=200, verbose_name="Text", null=True, blank=True)
    visibility = models.BooleanField(verbose_name="Visible", null=False)
    secret = models.CharField(max_length=50,verbose_name="Secret", null=False)

    objects = models.Manager()
    public = PublicImageManager()
    

    def save(self, *args, **kwargs):
        if self.pk:
            print("create image object")
        else:
            print("change image object")
        self.secret = User.objects.make_random_password(length=20)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-upload_datetime"]

    def __str__(self):
        return "{}'s post".format(self.owner.__str__())

    def GetImageHash(image):
        return f'{imagehash.phash(imagehash.Image.open(image))}'

    def IsUnique(image_hash):
        query = Image.objects.values_list('image_hash')
        return not [i[0] for i in query if diff(i[0], image_hash) < DIFF_THRESHOLD]


class History(models.Model):
    datetime = models.DateTimeField(verbose_name="Date", auto_now_add=True)
    referred_owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Owner", related_name="record")
    referred_image = models.ForeignKey(Image, on_delete=models.CASCADE, verbose_name="Image", related_name="record")
#>>>>>>> main
