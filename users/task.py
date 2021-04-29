
import time
from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()

@shared_task
def user_created(user_id):
    user = User.objects.get(id=user_id)
    subject = 'welcome!'
    message = f'Dear, {user.username} we happy to join us '
    email_host = settings.EMAIL_HOST_USER
    mail_send = send_mail(subject,message,email_host,[user.email])



