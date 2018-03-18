from rest_framework import serializers
from userarea.models import FacebookProfileUrl, TaskStatus


class TaskStatusSerializer(serializers.ModelSerializer):
    """
    Serialize task status model.
    """

    task_id = serializers.IntegerField(read_only=True)
    task_type = serializers.ChoiceField(read_only=True,
                                        choices=TaskStatus.TASK_TYPE_CHOICES)
    in_progress = serializers.BooleanField()
    created_on = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TaskStatus
        fields = ("task_id", "task_type", "in_progress", "created_on")



class FbProfileSerializer(serializers.ModelSerializer):
    url = serializers.CharField(read_only=True)

    class Meta:
        model = FacebookProfileUrl
        fields = ("url", )

    def validate_url(self, value):
        qs = FacebookProfileUrl.objects.filter(url__iexact=value)

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError("This url exists")
        return value

