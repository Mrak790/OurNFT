from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
import imagehash
import uuid
from ckeditor.fields import RichTextField
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
    likes = models.ManyToManyField(User, related_name="likes", blank=True)


    objects = models.Manager()
    public = PublicImageManager()
    

    def save(self, *args, **kwargs):
        if self.pk:
            print("create image object")
        else:
            print("change image object")
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-upload_datetime"]

    def __str__(self):
        return str(self.image_hash)

    def GetImageHash(image):
        return f'{imagehash.phash(imagehash.Image.open(image))}'

    def IsUnique(image_hash):
        query = Image.objects.values_list('image_hash')
        return not [i[0] for i in query if diff(i[0], image_hash) < DIFF_THRESHOLD]
    
    def total_likes(self):
        return self.likes.count()

    def most_liked():
        return Image.public.annotate(num_likes=Count('likes')).order_by('-num_likes')


class History(models.Model):
    datetime = models.DateTimeField(verbose_name="Date", auto_now_add=True)
    referred_owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Owner", related_name="record")
    referred_image = models.ForeignKey(Image, on_delete=models.CASCADE, verbose_name="Image", related_name="record")


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="New Owner", related_name="notifications")
    new_image = models.ForeignKey(Image, on_delete=models.CASCADE, verbose_name="New Image", related_name="notifications")

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name="User", related_name="comments")
    image = models.ForeignKey(Image,on_delete=models.CASCADE, verbose_name="Image", related_name="comments")
    content = RichTextField(blank=True, null=True)
    # content = models.CharField(max_length = 100,blank=True, verbose_name="Text",null=True)