from django.contrib.auth.views import LoginView
from django.urls import path

from .views import (
    get_cookie_view,
    set_cookie_view,
    set_session_view,
    get_session_view,
    MyLogoutView,
    AboutMeView,
    RegisterView,
    FooBarView, ProfileUpdateView, ProfileListView, AboutProfile, AboutProfileUpdateView,
)

app_name = 'myauth'

urlpatterns = [
    path('login/',
         LoginView.as_view(
             template_name='myauth/login.html', redirect_authenticated_user=True),
         name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('cookie/get/', get_cookie_view, name='cookie_get'),
    path('cookie/set/', set_cookie_view, name='cookie_set'),
    path('about-me/', AboutMeView.as_view(), name='about-me'),
    path('about-profile/<pk>', AboutProfile.as_view(), name='about_profile'),
    path('about-profile/update/<pk>', AboutProfileUpdateView.as_view(), name='about_profile_update'),
    path('about-me/update/<pk>', ProfileUpdateView.as_view(), name='about_me_update'),
    path('profile-list/', ProfileListView.as_view(), name='profile_list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('session/set/', set_session_view, name='session_set'),
    path('session/get/', get_session_view, name='session_get'),
    path('foo-bar/', FooBarView.as_view(), name='foo-bar')
]
