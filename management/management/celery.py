import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'management.settings')

app = Celery('management')
app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'email-send-in-every-minutes': {
#         'task': 'apps.student_management_system.tasks.send_email',
#         'schedule': crontab(minute='*/1'),
#     },
# }

# Windows compatibility settings
app.conf.update(
    worker_pool='solo',  # Use solo pool instead of prefork (Windows fix)
)

