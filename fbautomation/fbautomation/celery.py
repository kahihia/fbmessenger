#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8


import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fbautomation.settings')

app = Celery('fbautomation')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
