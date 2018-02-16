from django.db import models


from django.contrib.auth.models import User
import datetime


class ProfileUrl(models.Model):

    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.SET_NULL)
    url = models.CharField(max_length=500, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=datetime.datetime.now,
                                      null=True, blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return "{}".format(self.url)


class FacebookAccount(models.Model):

    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.SET_NULL)

    username = models.CharField(max_length=250)
    password = models.CharField(max_length=250)

    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=datetime.datetime.now,
                                      null=True, blank=True)


    class Meta:
        ordering = ["id"]

    def __str__(self):
        return "{}".format(self.username)


class Message(models.Model):

    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.SET_NULL)

    body = models.TextField(max_length=1000, null=True, blank=True)

    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=datetime.datetime.now,
                                      null=True, blank=True)
