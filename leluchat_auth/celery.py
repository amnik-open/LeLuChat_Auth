"""Define celery app"""
import os
from celery import Celery
from django.conf import settings
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "leluchat_auth.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")

import configurations
configurations.setup()

app = Celery("leluchat_auth")
app.config_from_object("django.conf:settings",  namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
