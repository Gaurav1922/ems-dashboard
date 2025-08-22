from celery import shared_task
from django.core.mail import EmailMessage

@shared_task
def send_email_task(subject, message, recipient_list):
    email = EmailMessage(subject, message, to=recipient_list)
    email.send()