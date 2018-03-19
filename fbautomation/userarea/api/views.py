#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8


from rest_framework import generics, mixins
from userarea.models import FacebookProfileUrl, TaskStatus, FacebookAccount, \
    Client

from .serializers import FbProfileSerializer, TaskStatusSerializer, \
    FbAccountSerializer, FbUpdateSerializer


class TaskStatusView(generics.ListAPIView):
    serializer_class = TaskStatusSerializer


    def get_queryset(self):
        qs = TaskStatus.objects.filter(user=self.request.user,
                                       in_progress=False)

        client = Client.objects.filter(user=self.request.user) #, online=False)
        if client:
            client[0].online = True
            client[0].save()

        return qs


class FbAccountApiView(generics.ListAPIView):
    serializer_class = FbAccountSerializer


    def get_queryset(self):
        qs = FacebookAccount.objects.filter(user=self.request.user)
        return qs


class FbProfileApiView(mixins.CreateModelMixin, generics.ListAPIView):
    serializer_class = FbProfileSerializer


    def get_queryset(self):
        query = self.request.GET.get("task_id")
        print(self.request.user)
        if query is not None:
            qs = FacebookProfileUrl.objects.filter(user=self.request.user,
                                                   task_id=query,
                                                   is_messaged=False)
            return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class FacebookProfileApiView(generics.RetrieveUpdateAPIView):
    lookup_field = "pk"
    serializer_class = FbUpdateSerializer


    def get_queryset(self):
        return FacebookProfileUrl.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        print(kwargs["pk"], kwargs["task_id"])
        return self.update(request, *args, **kwargs)
