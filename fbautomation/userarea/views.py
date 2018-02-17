from django.shortcuts import render
# from django.views import generic
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def index(request):

    return render(request, "base_generic.html")
