#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import time
from django.contrib.auth.models import User

# from django.core.cache import cache

from celery import shared_task

from .fbtool import Messenger, Collector
from .models import TaskProgress, CollectProgress, FacebookProfileUrl, UserPlan



@shared_task
def send_message(user, recipients, message, task):
    our_user = User.objects.filter(pk=user)[0]
    progress = TaskProgress.objects.filter(pk=task)[0]
    user_plan = UserPlan.objects.filter(user=our_user)[0]
    print(user)
    print("Got messenger task.")
    messenger = Messenger(our_user.facebookaccount.fb_user,
                          our_user.facebookaccount.fb_pass,
                          message)
    print(our_user, recipients, message)
    # for count, recipient in enumerate(recipients):
    for recipient in recipients:
        # cache.set(our_user.pk, count+1)
        recipient = FacebookProfileUrl.objects.filter(pk=recipient)[0]
        recipient.is_messaged = True
        recipient.save()
        message_url = messenger.get_message_url(recipient.url)
        messenger.send(message_url)
        print("Started sending messages!")

        progress.sent += 1
        progress.save()
        user_plan.messages_sent += 1
        user_plan.save()
        print(progress)

        # print(count, recipient)
        our_user.stats.total_messages += 1
        our_user.stats.save()
        time.sleep(10)
    progress.done = True
    progress.save()
    messenger.close()
    return "Message sent to recipients."


@shared_task
def collect_urls(user, url, task, tag=None):
    our_user = User.objects.filter(pk=user)[0]
    progress = CollectProgress.objects.filter(pk=task)[0]
    print(our_user)
    print("I am in collector task!")

    collector = Collector(our_user.facebookaccount.fb_user,
                          our_user.facebookaccount.fb_pass,
                          url)
    data = collector.collect()
    collector.close()

    if data:
        for profile in data:
            new_url = FacebookProfileUrl(
                user=our_user,
                url=profile[0],
                full_name=profile[1],
                tag=tag,
            )
            new_url.save()

            progress.collected -= 1
            progress.save()

    progress.collected = len(data)
    progress.done = True
    progress.save()

    return "Url profiles collected!"


