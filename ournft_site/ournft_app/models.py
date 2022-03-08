from tkinter import CASCADE
from wsgiref.simple_server import demo_app
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

    def save(self, *args, **kwargs):
        
        self.image_hash = f'{imagehash.phash(imagehash.Image.open(self.image))}'
        query = Image.objects.values_list('image_hash')
        if not [i[0] for i in query if diff(i[0], self.image_hash) < DIFF_THRESHOLD]:
            super().save(*args, **kwargs)
            return True
        else:
            print("not unique image")
            return False