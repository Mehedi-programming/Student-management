from .models import Student
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_email(email):
    subject = "Result"
    message = "Your result have created successfully."
    # users = Student.objects.all()
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )