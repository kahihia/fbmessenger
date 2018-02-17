from django.shortcuts import render
# from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, update_session_auth_hash
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .forms import SignupForm



@login_required
def index(request):

    return render(request, "base_generic.html")


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

def profile(request):
    if request.method == "POST":
        password_form = PasswordChangeForm(request.user, request.POST)
        user_form = UserForm(request.POST, instance=request.user)
        image_form = UserImageForm(request.POST, instance=request.user)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
        if user_form.is_valid():
            user_form.save()

        if image_form.is_valid():
            user_image = UserImage.objects.filter(user=request.user)[0]
            user_image.image = image_form.cleaned_data["image"]
            user_image.save()
        return redirect("profile")
    else:
        image_form = UserImageForm()
        password_form = PasswordChangeForm(request.user)
        user_form = UserForm(initial={
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "username": request.user.username
        })

    return render(request, "profile.html", {"password_form": password_form,
                                            "user_form": user_form,
                                            "image_form": image_form})
