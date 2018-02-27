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
    full_name = models.CharField(max_length=250, null=True, blank=True)
    tag = models.CharField(max_length=250, null=True, blank=True)
    is_messaged = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=datetime.datetime.now,
                                      null=True, blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        string = ""
        if self.full_name:
            string += self.full_name
        if self.tag:
            string += " - {}".format(self.tag)

        if self.url:
            string += " - {}".format(self.url)

        # return "{} - {} - {}".format(self.full_name, self.tag, self.url)
        return string


class FacebookAccount(models.Model):

    # user = models.ForeignKey(User, blank=True, null=True,
    #                          on_delete=models.SET_NULL)

    user = models.OneToOneField(User, blank=True,
                                null=True, on_delete=models.SET_NULL)

    # username = models.CharField(max_length=250)
    # password = models.CharField(max_length=250)
    fb_user = models.CharField(max_length=250, blank=True, null=True)
    fb_pass = models.CharField(max_length=250, blank=True, null=True)

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
    created_on = models.DateTimeField(default=datetime.datetime.now,
                                      null=True, blank=True)


    class Meta:
        ordering = ["-id"]



class Pricing(models.Model):
    price = models.FloatField()


class TaskProgress(models.Model):

    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.SET_NULL)
    name = models.CharField(max_length=250, null=True, blank=True)
    sent = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    done = models.BooleanField(default=False)

    created_on = models.DateTimeField(default=datetime.datetime.now,
                                      null=True, blank=True)


    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return "Sent {} out of {}".format(self.sent, self.total)

    def jsonify(self):
        data = {
            "id": self.id,
            "user": self.user.id,
            "name": self.name,
            "sent": self.sent,
            "total": self.total,
            "done": self.done,
            "created_on": self.created_on
        }
        return data


class CollectProgress(models.Model):

    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.SET_NULL)
    name = models.CharField(max_length=250, null=True, blank=True)
    url = models.URLField(max_length=1000, null=True, blank=True)
    collected = models.IntegerField(default=0)
    commenters = models.IntegerField(default=0)
    likers = models.IntegerField(default=0)
    done = models.BooleanField(default=False)

    created_on = models.DateTimeField(default=datetime.datetime.now,
                                      null=True, blank=True)


    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return "Collected {}".format(self.collected)

    def jsonify(self):
        data = {
            "id": self.id,
            "user": self.user.id,
            "name": self.name,
            "collected": self.collected,
            "commenters": self.commenters,
            "likers": self.likers,
            "done": self.done,
            "created_on": self.created_on
        }
        return data



class GlobalSetting(models.Model):
    max_messages_day = models.IntegerField(default=50)





@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Avatar.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_user_stats(sender, instance, created, **kwargs):
    if created:
        Stats.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def create_message_progress(sender, instance, created, **kwargs):
#     if created:
#         TaskProgress.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_facebook_account(sender, instance, created, **kwargs):
    if created:
        FacebookAccount.objects.create(user=instance)
