from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.contrib.auth.mixins import UserPassesTestMixin

from django.shortcuts import redirect
from django.db.models import Q

from django.core.cache import cache

from django.template.defaultfilters import date as filter_date

from .forms import SignupForm, PasswordChangeForm, UserForm, UserAvatarForm, \
    FacebookAccountForm, BulkUrlform, FacebookProfileForm, MessageForm, \
    CollectorForm

from .models import Avatar, FacebookAccount, FacebookProfileUrl, Stats, \
    TaskProgress, CollectProgress

from .tasks import send_message, collect_urls


class CreateFacebookAccount(generic.CreateView):
    form_class = FacebookAccountForm
    template_name = "create_facebook_account.html"


@login_required
def facebook_accounts(request):
    accounts = FacebookAccount.objects.filter(user=request.user,
                                              is_deleted=False)
    paginator = Paginator(accounts, 10)
    page = request.GET.get("page")

    try:
        accounts = paginator.page(page)
    except PageNotAnInteger:
        accounts = paginator.page(1)
    except EmptyPage:
        accounts = paginator.page(paginator.num_pages)


    return render(request, "facebook_accounts.html", {"accounts": accounts})


@login_required
def index(request):
    accounts = FacebookAccount.objects.filter(user=request.user,
                                              is_deleted=False).count()
    profile_urls = FacebookProfileUrl.objects.filter(user=request.user,
                                                     is_deleted=False).count()

    stats = Stats.objects.filter(user=request.user)[0]


    return render(request, "dashboard.html", {"accounts": accounts,
                                              "profile_urls": profile_urls,
                                              "stats": stats})


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
    avatar_form = UserAvatarForm()
    password_form = PasswordChangeForm(request.user)
    # print("Not post", password_form)
    user_form = UserForm(initial={
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        "username": request.user.username
    })
    facebook_form = FacebookAccountForm(initial={"fb_user": request.user.facebookaccount})

    if request.method == "POST" and "profile" in request.POST:
        user_form = UserForm(request.POST, instance=request.user)
        avatar_form = UserAvatarForm(request.POST, request.FILES)

        if user_form.is_valid():
            user_form.save()
        else:
            messages.error(request, 'Please correct the error below.')

        if avatar_form.is_valid():
            if avatar_form.cleaned_data["image"]:
                user_avatar = Avatar.objects.filter(user=request.user)[0]
                user_avatar.image = avatar_form.cleaned_data["image"]
                user_avatar.save()
                messages.success(request,
                                 "Your avatar was successfully updated!")
            user_form.save()
        else:
            messages.error(request, 'Profile Please correct the error below.')


    if request.method == "POST" and "password" in request.POST:
        password_form = PasswordChangeForm(request.user, request.POST)

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
        else:
            messages.error(request, 'Password Please correct the error below.')

    if request.method == "POST" and "facebook" in request.POST:
        instance = FacebookAccount.objects.filter(user=request.user)[0]
        facebook_form = FacebookAccountForm(request.POST)
        if facebook_form.is_valid():
            if instance:
                instance.fb_user = facebook_form.cleaned_data["fb_user"]
                instance.fb_pass = facebook_form.cleaned_data["fb_pass"]
                instance.save()
                messages.success(request, "Facebook credentials updated!")
            else:
                facebook_form = facebook_form.save(commit=False)
                facebook_form.user = request.user
                facebook_form.save()
                messages.success(request, "Facebook credentials saved!")
        else:
            messages.error(request, 'Facebook Please correct the error below.')



    return render(request, "profiletest.html", {"password_form": password_form,
                                                "user_form": user_form,
                                                "avatar_form": avatar_form,
                                                "facebook_form": facebook_form})

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
        username = request.POST.get("username")
        password = request.POST.get("password")
        facebook_account = FacebookAccount.objects.filter(pk=request.POST.get("id"),
                                                          user=request.user,
                                                          is_deleted=False)[0]
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
                tag = form.cleaned_data.get("tag")
                for url in urls:
                    url_form = FacebookProfileForm({"url": url,
                                                    "tag": tag})
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


@login_required
def remove_fburl(request):
    if request.POST:
        facebook_url = FacebookProfileUrl.objects.filter(pk=request.POST.get("id"),
                                                          user=request.user,
                                                          is_deleted=False)[0]
        if facebook_url:
            facebook_url.is_deleted = True
            facebook_url.save()
            data = {"success": True}
        else:
            data = {"success": False}

        return JsonResponse(data)
    else:
        return JsonResponse({"status": "You are not allowed to view this page."})


class UpdateFacebookProfileUrl(LoginRequiredMixin, generic.UpdateView):
    model = FacebookProfileUrl
    form_class = FacebookProfileForm
    template_name = "edit_profile_url.html"

    def get_success_url(self):
        return reverse("facebook_url_list")


class FacebookProfileUrlView(LoginRequiredMixin, generic.TemplateView):
    template_name = "facebook_profile_list.html"

class HistoryMessengerView(LoginRequiredMixin, generic.TemplateView):
    template_name = "history_messenger.html"

class HistoryCollectorView(LoginRequiredMixin, generic.TemplateView):
    template_name = "history_collector.html"

class BillingView(LoginRequiredMixin, generic.TemplateView):
    template_name = "billing.html"


class UsersView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    template_name = "users.html"

    def test_func(self):
        return self.request.user.is_staff


@login_required
def messaged_count(request):

    count = cache.get(request.user.pk)
    if not count:
        count = False

    count = {"count": count}

    return JsonResponse(count)


class MessengerView(LoginRequiredMixin, generic.FormView):

    form_class = MessageForm
    template_name = "messenger.html"


    def form_valid(self, form):
        super(MessengerView, self).form_valid(form)
        recipients = form.cleaned_data["recipients"]
        print(form.cleaned_data["message"])

        recipients = [recipient.pk for recipient in recipients]
        task = TaskProgress(
            user=self.request.user,
            name=form.cleaned_data.get("task_name"),
            total=len(recipients)
        )
        task.save()

        send_message.delay(self.request.user.pk,
                           recipients, form.cleaned_data["message"], task.id)

        json_response = {"status": True}
        return JsonResponse(json_response)


    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response


    def get_form_kwargs(self):
        """This method is what injects forms with their keyword arguments."""
        # grab the current set of form #kwargs
        kwargs = super(MessengerView, self).get_form_kwargs()
        # Update the kwargs with
        # the user_id
        kwargs['user'] = self.request.user.pk
        return kwargs

    def get_success_url(self):
        return reverse("messenger")


class CollectorView(LoginRequiredMixin, generic.FormView):

    form_class = CollectorForm
    template_name = "collector.html"


    def form_valid(self, form):
        super(CollectorView, self).form_valid(form)

        task = CollectProgress(
            user=self.request.user,
            name=form.cleaned_data.get("task_name"),
        )
        task.save()


        collect_urls.delay(self.request.user.pk,
                           form.cleaned_data["url"], task.id,
                           form.cleaned_data.get("task_name"))

        print(form.cleaned_data)
        json_response = {"status": True}
        return JsonResponse(json_response)


    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response


    def get_success_url(self):
        return reverse("collector")



@login_required
def ajax_profile(request):

    search = request.GET.get("search")
    sort = request.GET.get("sort", "id")
    order_type = request.GET.get("order", "desc")
    limit = request.GET.get("limit")
    offset = request.GET.get("offset")

    page = (int(offset) / int(limit)) + 1

    profiles = FacebookProfileUrl.objects.filter(user=request.user,
                                                 is_deleted=False)
    profile_count = profiles.count()

    if search:
        profiles = profiles.filter(Q(url__contains=search) | Q(tag__contains=search) | Q(full_name__contains=search))

    if order_type == 'asc':
        profiles = profiles.order_by(sort)
    else:
        profiles = profiles.order_by('-' + sort)

    paginator = Paginator(profiles, limit)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        profiles = paginator.page(1)
    except EmptyPage:
        profiles = paginator.page(paginator.num_pages)


    rows = [
        {
            "id": profile.id,
            "tag": profile.tag,
            "full_name": profile.full_name,
            "url": profile.url,
            "is_messaged": profile.is_messaged,
            "created_on": filter_date(profile.created_on, "d/m/Y")
        } for profile in profiles
    ]

    data = {
        "total": profile_count,
        "rows": rows
    }
    return JsonResponse(data)


@login_required
def ajax_messenger_history(request):

    search = request.GET.get("search")
    sort = request.GET.get("sort", "id")
    order_type = request.GET.get("order", "desc")
    limit = request.GET.get("limit")
    offset = request.GET.get("offset")

    page = (int(offset) / int(limit)) + 1

    profiles = TaskProgress.objects.filter(user=request.user)
    profile_count = profiles.count()

    if search:
        profiles = profiles.filter(name__contains=search)

    if order_type == 'asc':
        profiles = profiles.order_by(sort)
    else:
        profiles = profiles.order_by('-' + sort)

    paginator = Paginator(profiles, limit)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        profiles = paginator.page(1)
    except EmptyPage:
        profiles = paginator.page(paginator.num_pages)


    rows = [
        {
            "id": profile.id,
            "name": profile.name,
            "sent": profile.sent,
            "total": profile.total,
            "done": profile.done,
            "created_on": filter_date(profile.created_on, "d/m/Y")
        } for profile in profiles
    ]

    data = {
        "total": profile_count,
        "rows": rows
    }
    return JsonResponse(data)


@login_required
def ajax_collector_history(request):

    search = request.GET.get("search")
    sort = request.GET.get("sort", "id")
    order_type = request.GET.get("order", "desc")
    limit = request.GET.get("limit")
    offset = request.GET.get("offset")

    page = (int(offset) / int(limit)) + 1

    profiles = CollectProgress.objects.filter(user=request.user)
    profile_count = profiles.count()

    if search:
        profiles = profiles.filter(name__contains=search)

    if order_type == 'asc':
        profiles = profiles.order_by(sort)
    else:
        profiles = profiles.order_by('-' + sort)

    paginator = Paginator(profiles, limit)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        profiles = paginator.page(1)
    except EmptyPage:
        profiles = paginator.page(paginator.num_pages)


    rows = [
        {
            "id": profile.id,
            "name": profile.name,
            "collected": profile.collected,
            "done": profile.done,
            "created_on": filter_date(profile.created_on, "d/m/Y")
        } for profile in profiles
    ]

    data = {
        "total": profile_count,
        "rows": rows
    }
    return JsonResponse(data)


@login_required
def ajax_users(request):
    #TODO make less db queries.
    #TODO stats sortable too.

    search = request.GET.get("search")
    sort = request.GET.get("sort", "id")
    order_type = request.GET.get("order", "desc")
    limit = request.GET.get("limit")
    offset = request.GET.get("offset")

    page = (int(offset) / int(limit)) + 1

    users = User.objects.filter(is_active=True)
    users_count = users.count()

    if search:
        users = users.filter(username=search)

    if order_type == 'asc':
        users = users.order_by(sort)
    else:
        users = users.order_by('-' + sort)

    paginator = Paginator(users, limit)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)


    rows = [
        {
            "id": user.id,
            "username": user.username,
            "firstname": user.first_name,
            "lastname": user.last_name,
            "email": user.email,
            "profiles": FacebookProfileUrl.objects.filter(user=user,
                                                          is_deleted=False).count(),
            "sent": Stats.objects.filter(user=user)[0].total_messages,
            "created_on": filter_date(user.date_joined, "d/m/Y")
        } for user in users
    ]

    data = {
        "total": users_count,
        "rows": rows
    }
    return JsonResponse(data)


@login_required
def ajax_user_remove(request):
    if request.user.is_staff:
        if request.POST:
                user = User.objects.filter(pk=request.POST.get("id"))[0]
                if user:
                    user.is_active = False
                    user.save()
                    data = {"success": True}
                else:
                    data = {"success": False}

                return JsonResponse(data)
        else:
            return JsonResponse({"status": "You are not allowed to view this page."})
    else:
        return redirect("index")


@login_required
def ajax_user_edit(request):
    """User edit view.

    Staff member edits user with ajax call.
    """
    if request.user.is_staff:
        if request.POST:
            id = request.POST.get("id")
            username = request.POST.get("username")
            email = request.POST.get("email")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            password = request.POST.get("password")

            if id:
                user = User.objects.filter(pk=id)[0]
            if username:
                user.username = username
            if email:
                user.email = email
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if password:
                user.set_password(password)

            user.save()


            return JsonResponse({"success": True})

        else:
            return redirect("index")
    else:
        return redirect("index")


@login_required()
def ajax_progress(request):
    #TODO list to json check working station.
    #TODO need to change front side.
    #TODO maybe done. Front needs to changed.

    tasks = TaskProgress.objects.filter(user=request.user,
                                           done=False)
    collectors = CollectProgress.objects.filter(user=request.user,
                                               done=False)
    # print(collectors)
    # print(progress)
    progress = {"messenger": {task.id: task.jsonify() for task in tasks},
                "collector": {collector.id: collector.jsonify() for collector in collectors}}
    # print("===================================")
    # print(progress)
    # print("---------------------------------")

    return JsonResponse(progress)


@login_required()
def ajax_progress_last(request):

    task = TaskProgress.objects.filter(user=request.user).latest("id")

    return JsonResponse(task.jsonify())


@login_required()
def ajax_collect_last(request):

    collector = CollectProgress.objects.filter(user=request.user).latest("id")

    return JsonResponse(collector.jsonify())
