#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8


from rest_framework import generics, mixins
from userarea.models import FacebookProfileUrl, TaskStatus

from .serializers import FbProfileSerializer, TaskStatusSerializer


class TaskStatusView(generics.ListAPIView):
    serializer_class = TaskStatusSerializer


    def get_queryset(self):
        qs = TaskStatus.objects.filter(user=self.request.user,
                                       in_progress=False)
        return qs



class FbProfileApiView(mixins.CreateModelMixin, generics.ListAPIView):
    serializer_class = FbProfileSerializer


    def get_queryset(self):
        qs = FacebookProfileUrl.objects.all()
        query = self.request.GET.get("q")
        print(self.request.user)
        if query is not None:
            qs = qs.filter(url__icontains=query)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class FacebookProfileApiView(generics.RetrieveUpdateAPIView):
    lookup_field = "pk"
    serializer_class = FbProfileSerializer


    def get_queryset(self):
        return FacebookProfileUrl.objects.all()
