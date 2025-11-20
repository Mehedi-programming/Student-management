from .models import Result
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_email():
    subject = "Result"
    message = "Your result created."
    users = Result.objects.all()
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email for user in users],
        fail_silently=False,
    )