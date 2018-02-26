# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-24 18:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userarea', '0011_messageprogress'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_messages_day', models.IntegerField(default=50)),
            ],
        ),
        migrations.AlterField(
            model_name='facebookaccount',
            name='fb_pass',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='facebookaccount',
            name='fb_user',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='messageprogress',
            name='done',
            field=models.BooleanField(default=True),
        ),
    ]