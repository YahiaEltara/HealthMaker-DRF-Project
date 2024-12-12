from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_scheduled_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        'yahiaeltaralm@gmail.com',  # Replace with your email
        recipient_list,
        fail_silently=False,
    )
