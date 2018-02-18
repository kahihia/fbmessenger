from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .forms import SignupForm, PasswordChangeForm, UserForm, UserAvatarForm, FacebookAccountForm, BulkUrlform, FacebookProfileForm
from .models import Avatar, FacebookAccount, FacebookMessage, FacebookProfileUrl


class CreateFacebookAccount(generic.CreateView):
    form_class = FacebookAccountForm
    template_name = "create_facebook_account.html"


@login_required
def facebook_accounts(request):
    accounts = FacebookAccount.objects.filter(user=request.user, is_deleted=False)
    paginator = Paginator(accounts, 10)
    page = request.GET.get("page")

    try:
        accounts = paginator.page(page)
    except PageNotAnInteger:
        accounts = paginator.page(1)
    except EmptyPage:
        accounts = paginator.page(paginator.num_pages)


    print(accounts)
    return render(request, "facebook_accounts.html", {"accounts": accounts})


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
            messages.error(request, 'Please correct the error below.')
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

@login_required
def new_fbaccount(request):
    if request.POST:
        facebook_account_form = FacebookAccountForm(request.POST)
        if facebook_account_form.is_valid():
            facebook_account_form = facebook_account_form.save(commit=False)
            facebook_account_form.user = request.user
            facebook_account_form.save()
            data = {"success": True}

        else:
            data = {"success": False,
                    "error_message": facebook_account_form.errors}
        return JsonResponse(data)
    else:
        return JsonResponse({"status": "You are not allowed to view this page."})


@login_required
def remove_fbaccount(request):
    if request.POST:
        print(request.POST.get("id"))
        facebook_account = FacebookAccount.objects.filter(pk=request.POST.get("id"),
                                                          user=request.user,
                                                          is_deleted=False)[0]
        print(facebook_account)
        if facebook_account:
            facebook_account.is_deleted = True
            facebook_account.save()
            data = {"success": True}
        else:
            data = {"success": False}

        return JsonResponse(data)
    else:
        return JsonResponse({"status": "You are not allowed to view this page."})


@login_required
def edit_fbaccount(request):
    if request.POST:
        print("Aq var")
        username = request.POST.get("username")
        password = request.POST.get("password")
        facebook_account = FacebookAccount.objects.filter(pk=request.POST.get("id"),
                                                          user=request.user,
                                                          is_deleted=False)[0]
        print(facebook_account)
        if facebook_account:
            if username:
                facebook_account.username = username
            if password:
                facebook_account.password = password
            facebook_account.save()
            data = {"success": True}
        else:
            data = {"success": False}

        return JsonResponse(data)
    else:
        return JsonResponse({"status": "You are not allowed to view this page."})


@login_required
def get_fbaccount(request, pk):
    facebook_account = FacebookAccount.objects.filter(pk=pk,
                                                        user=request.user,
                                                        is_deleted=False)[0]
    print(facebook_account)
    data = {"success": True, "username": facebook_account.username}
    return JsonResponse(data)


@login_required
def new_fburl(request):
    if request.method == 'POST':
        form = BulkUrlform(request.POST)
        saved_url = False
        wrong_url = False
        if form.is_valid():
            try:
                urls = form.cleaned_data.get("url").split()
                for url in urls:
                    url_form = FacebookProfileForm({"url": url})
                    if url_form.is_valid():
                        url_form = url_form.save(commit=False)
                        url_form.user = request.user
                        url_form.save()
                        saved_url = True
                    else:
                        wrong_url = True
                if saved_url:
                    messages.success(request, "Saved!")
                if wrong_url:
                    messages.error(request, "Some of urls are wrong and are not saved!")
                return redirect('create_fburl')
            except:
                messages.error(request, "Each profile link must on a separate line.")
                return redirect('create_fburl')
        else:
            messages.error(request, "Please correct the error below!")
            return redirect('create_fburl')
    else:
        form = BulkUrlform()
    return render(request, 'new_profile_url.html', {'form': form})
