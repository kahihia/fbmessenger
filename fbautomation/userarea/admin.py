from django.contrib import admin

from .models import FacebookAccount, FacebookMessage, FacebookProfileUrl, \
    Avatar, Stats, TaskProgress, CollectProgress, DefaultPlan, UserPlan, \
    TaskStatus


@admin.register(FacebookAccount)
class FacebookAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "fb_user", "created_on")


@admin.register(FacebookMessage)
class FacebookMessageAdmin(admin.ModelAdmin):
    list_display = ("title", "created_on")


@admin.register(FacebookProfileUrl)
class FacebookProfileUrlAdmin(admin.ModelAdmin):
    list_display = ("url", "created_on")


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ("user", "created_on")


@admin.register(Stats)
class StatsAdmin(admin.ModelAdmin):
    list_display = ("user", "total_messages", "total_spent", "created_on")


@admin.register(TaskProgress)
class TaskProgressAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "user", "sent", "total", "done", "created_on")


@admin.register(CollectProgress)
class CollectProgressAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "user", "collected",
                    "commenters", "likers", "done", "created_on")


@admin.register(DefaultPlan)
class DefaultPlanAdmin(admin.ModelAdmin):
    list_display = ("stripe_plan", "message_limit")


@admin.register(UserPlan)
class UserPlanAdmin(admin.ModelAdmin):
    list_display = ("user", "stripe_plan", "messages_sent", "created_on")

@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = ("user", "task_id", "task_type", "in_progress", "created_on")
