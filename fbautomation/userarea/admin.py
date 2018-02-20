from django.contrib import admin

from .models import FacebookAccount, FacebookMessage, FacebookProfileUrl, Avatar, Stats


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
class AtatsAdmin(admin.ModelAdmin):
    list_display = ("user", "total_messages", "total_spent", "created_on")
