from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email_task(subject,message,recipline_list):
    send_mail(subject,message,'rikudo.sanin98@mail.ru',recipline_list)