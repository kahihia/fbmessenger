from django.contrib import admin

from .models import FacebookAccount, FacebookMessage, FacebookProfileUrl, Avatar, Stats, MessageProgress


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


@admin.register(MessageProgress)
class MessageProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "sent", "total", "done", "created_on")
