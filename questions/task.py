
import time
from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
User = get_user_model()
from .models import Question,Answer,qlike

@shared_task
def question_created(question_id):
    question = Question.objects.get(id=question_id)
    subject = f'question id {question.id}'
    message = f'dear {question.author} your have successfully created question. your question id is {question.id}'
    email_host = settings.EMAIL_HOST_USER

    mail_send = send_mail(subject,message,email_host,[question.author.email])

@shared_task
def question_answered(answer_id):
    answer = Answer.objects.get(id=answer_id)
    subject = f' user {answer.author.username} answered your question'
    message = f'Dear { answer.question.author.username } answer body is {answer.body}'
    email_host = settings.EMAIL_HOST_USER
    mail_send = send_mail(subject,message,email_host,[answer.question.author.email])

@shared_task
def question_liked(q_id):
    qs = qlike.objects.get(id=q_id)
    subject = f' user {qs.liker.username} Liked your question'
    message = f'Dear { qs.question.author.username } , {qs.liker.username} liked your question'
    email_host = settings.EMAIL_HOST_USER
    mail_send = send_mail(subject,message,email_host,[qs.question.author.email])



