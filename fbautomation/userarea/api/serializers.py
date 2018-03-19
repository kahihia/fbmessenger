from rest_framework import serializers
from userarea.models import FacebookProfileUrl, TaskStatus, FacebookAccount


class TaskStatusSerializer(serializers.ModelSerializer):
    """
    Serialize task status model.
    """

    task_id = serializers.IntegerField(read_only=True)
    task_type = serializers.ChoiceField(read_only=True,
                                        choices=TaskStatus.TASK_TYPE_CHOICES)
    message = serializers.CharField(read_only=True)
    in_progress = serializers.BooleanField()
    created_on = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TaskStatus
        fields = ("task_id", "task_type",
                  "message", "in_progress", "created_on")


class FbAccountSerializer(serializers.ModelSerializer):
    fb_user = serializers.CharField(read_only=True)
    fb_pass = serializers.CharField(read_only=True)

    class Meta:
        model = FacebookAccount
        fields = ("fb_user", "fb_pass")


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

    class Meta:
        model = FacebookProfileUrl
        fields = ("pk", "url", "is_messaged")

    def validate_url(self, value):
        qs = FacebookProfileUrl.objects.filter(url__iexact=value)

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError("This url exists")
        return value

