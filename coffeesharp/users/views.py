from django.contrib.auth import authenticate, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from django.contrib.auth import authenticate, login
from django.views.generic import CreateView, UpdateView

from coffeesharp import settings
from users import forms
from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm


class LoginUser(LoginView):
 form_class = AuthenticationForm
 template_name = 'users/login.html'
 extra_context = {'title': "Авторизация"}


class RegisterUser(CreateView):
 form_class = RegisterUserForm
 success_url = reverse_lazy('users:login')
 template_name = 'users/register.html'
 extra_context = {'title': "Регистрация"}


class ProfileUser(LoginRequiredMixin, UpdateView):
 model = get_user_model()
 form_class = ProfileUserForm
 template_name = 'users/profile.html'
 extra_context = {'title': "Профиль пользователя"}

 def get_success_url(self):
  return reverse_lazy('users:profile')  # без аргументов

 def get_object(self, queryset=None):
  return self.request.user

 extra_context = {'title': "Профиль пользователя",
                  'default_image': settings.DEFAULT_USER_IMAGE}


class UserPasswordChange(PasswordChangeView):
 form_class = UserPasswordChangeForm
 success_url = reverse_lazy("users:password_change_done")
 template_name = "users/password_change_form.html"
 extra_context = {'title': "Изменение пароля"}





