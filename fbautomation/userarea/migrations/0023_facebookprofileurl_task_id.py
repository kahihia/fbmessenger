# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-18 18:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userarea', '0022_client_taskstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='facebookprofileurl',
            name='task_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
