from django.db import models
from django.contrib.auth.models import  User
from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.dispatch import receiver
import datetime

#defines the upload loaction of any media uploaded
def upload_loaction(instance, filename, **kwargs):
    file_path = 'bucks/{author_id}/{title}-{filename}'.format(
        author_id=str(instance.author.id), title=str(instance.title), filename=filename
        )
    return file_path


class Post(models.Model):
    title       = models.CharField(max_length=50, null=False, blank=False)
    body        = models.TextField(max_length=5000, null=False, blank=False)
    image       = models.ImageField(upload_to=upload_loaction, null=False, blank=True)
    imagelink   = models.CharField(max_length=200, null=False, blank=True)
    date_pub    = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_up     = models.DateTimeField(auto_now=True, verbose_name="date updated")
    author      = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    slug        = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title

@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, *args, **kwargs):
    instance.image.delete(False)

def pre_save_post_receiever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug=slugify(instance.title + "-" + str(datetime.datetime.now()))

pre_save.connect(pre_save_post_receiever, sender=Post)
