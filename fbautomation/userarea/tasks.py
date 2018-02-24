#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import time
import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from django.core.cache import cache

from celery import shared_task

from .fbmessenger import Messenger
from .models import TaskProgress


@shared_task
def create_random_user_accounts(total):
    for i in range(total):
        username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
        email = '{}@example.com'.format(username)
        password = get_random_string(50)
        User.objects.create_user(username=username, email=email, password=password)
    return '{} random users created with success!'.format(total)


@shared_task
def send_message(user, recipients, message, task):
    our_user = User.objects.filter(pk=user)[0]
    progress = TaskProgress.objects.filter(pk=task)[0]
    print(user)
    print("I am started.")
    # messenger = Messenger(user.facebookaccount.fb_user,
    #                       user.facebookaccount.fb_pass,
    #                       message)
    print(our_user, recipients, message)
    for count, recipient in enumerate(recipients):
        cache.set(our_user.pk, count+1)
        # recipient.is_messaged = True
        # recipient.save()
        # message_url = messenger.get_message_url(recipient.url)
        # messenger.send(message_url)
        print("I am here bro!")

        progress.sent += 1
        progress.save()
        print(progress)

        print(count, recipient)
        our_user.stats.total_messages += 1
        our_user.stats.save()
        time.sleep(10)
    progress.done = True
    progress.save()
    # messenger.close()
    return "Message sent to recipients."

