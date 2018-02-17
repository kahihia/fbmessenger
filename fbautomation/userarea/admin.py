from django.contrib import admin

from .models import FacebookAccount, FacebookMessage, FacebookProfileUrl


@admin.register(FacebookAccount)
class FacebookAccountAdmin(admin.ModelAdmin):
    list_display = ("username", "created_on")


@admin.register(FacebookMessage)
class FacebookMessageAdmin(admin.ModelAdmin):
    list_display = ("title", "created_on")


@admin.register(FacebookProfileUrl)
class FacebookProfileUrlAdmin(admin.ModelAdmin):
    list_display = ("url", "created_on")
