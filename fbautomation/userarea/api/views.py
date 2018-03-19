#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8


from rest_framework import generics, mixins
from userarea.models import FacebookProfileUrl, TaskStatus, FacebookAccount, \
    Client, TaskProgress, UserPlan

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
        print(request.POST.get("task_id"))
        task_id = request.POST.get("task_id")
        done = request.POST.get("task_id")

        user_plan = UserPlan.objects.filter(user=self.request.user)[0]
        user_plan.messages_sent -= 1
        user_plan.save()

        progress = TaskProgress.objects.filter(pk=task_id)
        if progress:
            progress.sent += 1
            progress.save()


        if done:
            progress.done = True
            progress.save()
        return self.update(request, *args, **kwargs)
