from django.db import models
from django.conf import settings
from django.db.models import signals
from django.dispatch import receiver
from django.utils.text import slugify
import uuid

class Question(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='questions')
    content = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    

class Answer(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='answers')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user_answer')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

class qlike(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='likes')
    liker = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.question.content}, {self.liker}"

class alike(models.Model):
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE,related_name='likers')
    liker = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)    

class Reply(models.Model):
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE,related_name='replies')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    body = models.TextField()

  

@receiver(signals.pre_save,sender=Question)
def slugify_content(sender,instance,*args,**kwargs):
    instance.slug = slugify(instance.content)+"-"+str(uuid.uuid4())[:4]
    
