#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from .views import FacebookProfileApiView, FbProfileApiView, TaskStatusView, \
    FbAccountApiView

from django.conf.urls import url

urlpatterns = [
    url(r"^taskstatus/$", TaskStatusView.as_view(), name="api-task-status"),
    url(r"^fburls/$", FbProfileApiView.as_view(), name="api-fburl-create"),
    url(r"^fbaccount/$", FbAccountApiView.as_view(), name="api-fb-account"),
    url(r"^fburls/(?P<pk>\d+)/$", FacebookProfileApiView.as_view(), name="api-fburl")
]
