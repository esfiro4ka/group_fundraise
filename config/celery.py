from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

celery_app_collects = Celery('apps.collects')
celery_app_collects.config_from_object('django.conf:settings', namespace='CELERY')
celery_app_collects.autodiscover_tasks()

celery_app_payments = Celery('apps.payments')
celery_app_payments.config_from_object('django.conf:settings', namespace='CELERY')
celery_app_payments.autodiscover_tasks()
