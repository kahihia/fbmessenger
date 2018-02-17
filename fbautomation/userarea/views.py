from django.shortcuts import render
# from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib import messages
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .forms import SignupForm, PasswordChangeForm, UserForm, UserAvatarForm
from .models import Avatar



@login_required
def index(request):

    return render(request, "dashboard.html")


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def profile(request):
    if request.method == "POST":
        password_form = PasswordChangeForm(request.user, request.POST)
        user_form = UserForm(request.POST, instance=request.user)
        avatar_form = UserAvatarForm(request.POST, request.FILES)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
        else:
            messages.error(request, 'Please correct the error below.')

        if user_form.is_valid():
            user_form.save()

        if avatar_form.is_valid():
            if avatar_form.cleaned_data["image"]:
                user_avatar = Avatar.objects.filter(user=request.user)[0]
                user_avatar.image = avatar_form.cleaned_data["image"]
                user_avatar.save()
                messages.success(request, "Your avatar was successfully updated!")
            user_form.save()
        else:
            messages.error(request, 'Please aacorrect the error below.')
    else:
        avatar_form = UserAvatarForm()
        password_form = PasswordChangeForm(request.user)
        # print("Not post", password_form)
        user_form = UserForm(initial={
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "username": request.user.username
        })

    return render(request, "profile.html", {"password_form": password_form,
                                            "user_form": user_form,
                                            "avatar_form": avatar_form})
