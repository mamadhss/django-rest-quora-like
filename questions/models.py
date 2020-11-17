from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import signals
from django.utils.text import slugify


class Question(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255,unique=True)
    

    def __str__(self):
        return self.content

class Answer(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='answers')  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    body = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='votes')

    def __str__(self):
        return self.body
    

        

@receiver(signals.pre_save, sender=Question)
def populate_slug(sender, instance, **kwargs):
    instance.slug = slugify(instance.content)