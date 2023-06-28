from typing import Any

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, FormView, DetailView, ListView

from .forms import ProfileUpdateForm, AboutForm
from .models import Profile


class AboutMeView(FormView):
    template_name = 'myauth/about-me.html'
    form_class = AboutForm


class ProfileUpdateView(UserPassesTestMixin, UpdateView):
    model = Profile
    fields = ['avatar', 'bio']
    success_url = reverse_lazy('myauth:about-me')
    template_name_suffix = '_update_form'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.profile == self.get_object()


class AboutProfileUpdateView(UserPassesTestMixin, UpdateView):
    model = Profile
    fields = ['avatar', 'bio']
    success_url = reverse_lazy('myauth:about_profile')
    template_name = 'myauth/about_profile_update_form.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.profile == self.get_object()


class ProfileListView(ListView):
    template_name = 'myauth/profile-list.html'
    queryset = Profile.objects.all()
    context_object_name = 'profiles'


class AboutProfile(DetailView):
    template_name = 'myauth/about-profile.html'
    queryset = Profile.objects.all()
    context_object_name = 'profile'


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:about-me')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')

        user = authenticate(self.request,
                            username=username,
                            password=password)
        login(request=self.request, user=user)
        return response


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/admin/')
        return render(request, 'myauth/login.html')
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return redirect('/admin/')
    return render(request, 'myauth/login.html', {'error'" 'invalid"})


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('myauth:login')


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie set')
    response.set_cookie('fizz', 'buzz', max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('fizz', 'default value')
    return HttpResponse(f'Cookie value: {value!r}')


@permission_required('myauth.view_profile', raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['foobar'] = 'spameggs'
    return HttpResponse('Session set')


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default')
    return HttpResponse(f'Session value: {value!r}')


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({'foo': 'bar', 'spam': 'eggs'})
