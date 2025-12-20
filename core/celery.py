import os

from celery import Celery

# Default module Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

# Loading conf from settings.py with prefix CELERY_
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto discovering tasks in files tasks.py in My apps
app.autodiscover_tasks()
