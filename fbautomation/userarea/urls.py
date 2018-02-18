from django.conf.urls import url
from . import views



urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/signup/$', views.signup, name='signup'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^fbaccounts/$', views.facebook_accounts, name='fbaccounts'),
    url(r'^create/fbaccount/$', views.CreateFacebookAccount.as_view(), name='create_fbaccount'),
    url(r'^ajax/new/fbaccount/$', views.new_fbaccount, name='new_fbaccount'),
]
