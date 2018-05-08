from rest_framework import serializers
from userarea.models import FacebookProfileUrl, TaskStatus, FacebookAccount
from django.contrib.auth.models import User
from pinax.stripe.models import Subscription, Plan
import datetime

class TaskStatusSerializer(serializers.ModelSerializer):
    """
    Serialize task status model.
    """

    task_id = serializers.IntegerField(read_only=True)
    task_type = serializers.ChoiceField(read_only=True,
                                        choices=TaskStatus.TASK_TYPE_CHOICES)
    message = serializers.CharField(read_only=True)
    url = serializers.URLField(read_only=True)
    tag = serializers.CharField(read_only=True)
    in_progress = serializers.BooleanField(read_only=True)
    in_pause = serializers.BooleanField()
    created_on = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TaskStatus
        fields = ("task_id", "task_type", "message", "url",
                  "tag", "in_progress", "in_pause", "created_on")

    def update(self, instance, validated_data):
        print("+++++++++++++Update Pause+++++++++++++++")
        print (instance)
        print (validated_data)

        instance.in_pause = validated_data.get('in_pause', instance.in_pause)
        instance.save()
        return instance

class SubscriptionSerializer(serializers.ModelSerializer):
    current_period_start = serializers.DateTimeField(read_only=True)
    current_period_end = serializers.DateTimeField(read_only=True)
    plan = serializers.CharField(read_only=True, source='plan.name')

    class Meta:
        model = Subscription
        fields = ("current_period_start", "current_period_end", "plan")

class FbAccountSerializer(serializers.ModelSerializer):
    fb_user = serializers.CharField(read_only=True)
    fb_pass = serializers.CharField(read_only=True)
    max_message_count = serializers.IntegerField(read_only=True)
    max_profile_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = FacebookAccount
        fields = ("fb_user", "fb_pass", "account_status", "disabled_on", "user_id", "max_message_count", "max_profile_count")

    def update(self, instance, validated_data):
        instance.account_status = validated_data.get('account_status', instance.account_status)
        instance.disabled_on = validated_data.get('disabled_on', instance.disabled_on)
        instance.save()
        return instance

class FbMessageProfileSerializer(serializers.ModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(read_only=True)
    url = serializers.CharField(read_only=True)
    is_messaged = serializers.BooleanField(read_only=False)
    updated_on = serializers.DateTimeField(read_only=True)
    task_id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = FacebookProfileUrl
        fields = ("pk", "url", "is_messaged", "updated_on", "task_id", "user_id")

class FbulrCraeteSerializer(serializers.ModelSerializer):
    url = serializers.URLField()
    full_name = serializers.CharField()
    tag = serializers.CharField()
    image_path = serializers.URLField(allow_blank=True)
    date_to_be_added = serializers.CharField(allow_blank=True)
    desc = serializers.CharField(allow_blank=True)

    class Meta:
        model = FacebookProfileUrl
        fields = ("url", "full_name", "tag", "image_path", "date_to_be_added", "desc")


class FbProfileSerializer(serializers.ModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(read_only=True)
    url = serializers.CharField(read_only=True)

    class Meta:
        model = FacebookProfileUrl
        fields = ("pk", "url", )

    def validate_url(self, value):
        qs = FacebookProfileUrl.objects.filter(url__iexact=value)

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError("This url exists")
        return value

class FbUpdateSerializer(serializers.ModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(read_only=True)
    url = serializers.CharField(read_only=True)
    is_messaged = serializers.BooleanField(read_only=False)
    updated_on = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FacebookProfileUrl
        fields = ("pk", "url", "is_messaged", "updated_on")

    def validate_url(self, value):
        qs = FacebookProfileUrl.objects.filter(url__iexact=value)

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError("This url exists")
        return value

    def update(self, instance, validated_data):
        print("+++++++++++++Update+++++++++++++++")
        print (instance)
        print (validated_data)

        instance.is_messaged = validated_data.get('is_messaged', instance.is_messaged)
        instance.updated_on = datetime.datetime.now()
        instance.save()
        return instance

class EmptySerializer(serializers.Serializer):
    task_id = serializers.IntegerField()
    done = serializers.BooleanField()

