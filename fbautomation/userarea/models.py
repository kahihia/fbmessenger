from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import datetime


def custom_user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/pictures/user_<id>/<filename>
    return "pictures/user_{0}/{1}".format(instance.user.id, filename)


class FacebookProfileUrl(models.Model):

    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.SET_NULL)
    url = models.URLField(max_length=500, null=True, blank=True)
    is_messaged = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=datetime.datetime.now,
                                      null=True, blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return "{}".format(self.url)


class FacebookAccount(models.Model):

    # user = models.ForeignKey(User, blank=True, null=True,
    #                          on_delete=models.SET_NULL)

    user = models.OneToOneField(User, blank=True,
                                null=True, on_delete=models.SET_NULL)

    # username = models.CharField(max_length=250)
    # password = models.CharField(max_length=250)
    fb_user = models.CharField(max_length=250)
    fb_pass = models.CharField(max_length=250)

    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=datetime.datetime.now,
                                      null=True, blank=True)


    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return "{}".format(self.fb_user)


class FacebookMessage(models.Model):

    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.SET_NULL)

    title = models.CharField(max_length=250, null=True, blank=True)
    body = models.TextField(max_length=1000, null=True, blank=True)

    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=datetime.datetime.now,
                                      null=True, blank=True)


class Avatar(models.Model):
    user = models.OneToOneField(User, blank=True,
                                null=True, on_delete=models.SET_NULL)
    image = models.ImageField(null=True, blank=True,
                              default="/pictures/avatar.png",
                              upload_to=custom_user_directory_path)

    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=datetime.datetime.now,
                                      null=True, blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return "/media/{}".format(self.image)


class Stats(models.Model):

    user = models.OneToOneField(User, blank=True,
                                null=True, on_delete=models.SET_NULL)
    total_messages = models.IntegerField(default=0, null=True, blank=True)
    total_spent = models.FloatField(default=0, null=True, blank=True)
    total_urls = models.IntegerField(default=0, null=True, blank=True)


    class Meta:
        ordering = ["-id"]



class Pricing(models.Model):
    price = models.FloatField()



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Avatar.objects.create(user=instance)
