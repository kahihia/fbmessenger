from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from pinax.stripe.models import Plan, Customer
from pinax.stripe.signals import WEBHOOK_SIGNALS
from rest_framework.authtoken.models import Token
import datetime


def custom_user_directory_path(instance, filename):
    """
    This function gives to uploaded file
    saving location. Mostly used for saving
    Avatar.
    """
    # file will be uploaded to MEDIA_ROOT/pictures/user_<id>/<filename>
    return "pictures/user_{0}/{1}".format(instance.user.id, filename)


class FacebookProfileUrl(models.Model):
    """
    Facebook profile url model.
    All the information about
    our target is stored here.
    """

    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.SET_NULL)
    url = models.URLField(max_length=500, null=True, blank=True)
    full_name = models.CharField(max_length=250, null=True, blank=True)
    tag = models.CharField(max_length=250, null=True, blank=True)
    task_id = models.IntegerField(null=True, blank=True)
    is_messaged = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=datetime.datetime.now,
                                      null=True, blank=True)
    updated_on = models.DateTimeField(default=datetime.datetime.now,
                                      null=True, blank=True)

    image_path = models.URLField(max_length=500, null=True, blank=True)
    date_to_be_added = models.CharField(max_length=50, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)

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
    """
    User adds facebook account
    to this model. We are storing
    it here.
    """

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

    account_status = models.IntegerField(default=1, null=True, blank=True)
    disabled_on = models.DateTimeField(default=datetime.datetime.now,
                                      null=True, blank=True)
    max_message_count = models.IntegerField(default=45, null=True, blank=True)
    max_profile_count = models.IntegerField(default=2000, null=True, blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return "{}".format(self.fb_user)


class FacebookMessage(models.Model):
    """
    Facebook message model.
    We are storing here sent message.
    """

    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.SET_NULL)

    title = models.CharField(max_length=250, null=True, blank=True)
    body = models.TextField(max_length=1000, null=True, blank=True)

    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=datetime.datetime.now,
                                      null=True, blank=True)


class Avatar(models.Model):
    """
    User avatar model.
    """
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
    """
    User stats model.
    """

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
    """
    Messenger task prgoress.
    """

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
    """
    Collet task progress.
    """

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


class TaskStatus(models.Model):
    """
    Model for tracking tasks from
    Api serializers.
    """
    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.SET_NULL)
    task_id = models.IntegerField()
    message = models.TextField(max_length=2000, null=True, blank=True)
    url = models.URLField(max_length=1000, null=True, blank=True)
    tag = models.CharField(max_length=250, null=True, blank=True)
    TASK_TYPE_CHOICES = (
        ("c", "collector"),
        ("m", "messenger"),
    )
    task_type = models.CharField(max_length=1, choices=TASK_TYPE_CHOICES,
                                 blank=True, null=True)

    in_progress = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=datetime.datetime.now,
                                      null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.task_id, self.task_type)



class GlobalSetting(models.Model):
    max_messages_day = models.IntegerField(default=50)


class DefaultPlan(models.Model):
    """
    Default plan model.
    """
    stripe_plan = models.OneToOneField(Plan, blank=True, null=True,
                                       on_delete=models.SET_NULL)
    message_limit = models.IntegerField()

    COLOR_CHOICES = (
        ('g', "green"),
        ('y', "yellow"),
        ('p', "purple"),
    )
    box_color = models.CharField(max_length=1, choices=COLOR_CHOICES,
                                 blank=True, null=True, default="y")

    def __str__(self):
        return "{} {}".format(self.stripe_plan, self.message_limit)


class UserPlan(models.Model):
    """
    User plan model. When user buys
    subscription information about it is
    saved here.
    Also we are giving some limitations.
    """
    user = models.OneToOneField(User, blank=True,
                                null=True, on_delete=models.SET_NULL)
    stripe_plan = models.ForeignKey(Plan, blank=True, null=True,
                                    on_delete=models.SET_NULL)
    messages_sent = models.IntegerField(default=100)
    created_on = models.DateTimeField(default=datetime.datetime.now,
                                      null=True, blank=True)


    def exceeded_limit(self):
        # default_limit = DefaultPlan.objects.filter(stripe_plan=self.stripe_plan)[0]
        # print(default_limit)
        if self.messages_sent <= 0:
            return True
        else:
            return False

    def __str__(self):
        return "{} {} {}".format(self.user, self.stripe_plan, self.messages_sent)


class Client(models.Model):
    """
    In this model we are tracking
    desktop client status. Is it online
    or is it in offline. So we can
    give user notifications.
    """
    user = models.OneToOneField(User, blank=True,
                                null=True, on_delete=models.SET_NULL)

    online = models.BooleanField(default=False)
    last_update = models.DateTimeField(auto_now=True,
                                       null=True, blank=True)
    created_on = models.DateTimeField(default=datetime.datetime.now,
                                      null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.user, self.online)

    def update(self):
        self.last_update = datetime.datetime.now()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    We are creating user default
    avatar at the user registration ends.
    """
    if created:
        Avatar.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_user_stats(sender, instance, created, **kwargs):
    """
    Creating user stats row.
    """
    if created:
        Stats.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_user_client(sender, instance, created, **kwargs):
    """
    We are creating user client.
    """
    if created:
        Client.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def create_message_progress(sender, instance, created, **kwargs):
#     if created:
#         TaskProgress.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_facebook_account(sender, instance, created, **kwargs):
    """
    By default we are creating empty
    row for newly created users
    as we have one to one field.
    It cant be empty.
    """
    if created:
        FacebookAccount.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_user_token(sender, instance, created, **kwargs):
    """
    When user is created we also
    register for it api token.
    """
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_user_plan(sender, instance, created, **kwargs):
    """
    When user is created we also
    create for them subscrption plan.
    """
    if created:
        UserPlan.objects.create(user=instance)


@receiver(WEBHOOK_SIGNALS["plan.created"])
def handle_plan_created(sender, event, **kwargs):
    print(event)


@receiver(WEBHOOK_SIGNALS["invoice.payment_succeeded"])
def handle_payment_succeeded(sender, event, **kwargs):
    # TODO Clean this code.
    # print(sender, event.validated_message["data"]["object"])
    customer_id = event.validated_message["data"]["object"]["customer"]
    # print(customer_id)
    plan_id = event.validated_message["data"]["object"]["lines"]["data"][0]["plan"]["id"]#[0]#["plan"]#["id"]
    plan = Plan.objects.filter(stripe_id=plan_id)[0]
    # print(plan_id)
    user = User.objects.filter(username=Customer.objects.filter(stripe_id=customer_id)[0])[0]
    userplan = UserPlan.objects.filter(user=user)[0]
    default_user_plan = DefaultPlan.objects.filter(stripe_plan=plan)[0]
    userplan.stripe_plan = plan
    userplan.messages_sent = default_user_plan.message_limit
    userplan.save()
