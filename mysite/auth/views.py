from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View

from main.models import Profile


# Create your views here.
class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('main'))
        else:
            messages.error(request, 'Логин или пароль неверно введены')
        return render(request, 'auth/login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'auth/form.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'auth/form.html')
        user = User.objects.filter(username=username)
        if user:
            messages.info(request,'Пользователь уже существует')
        else:
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                profile = Profile.objects.create(user=user)
                profile.save()
                messages.success(request, 'Аккаунт успешно создан')
            except Exception as e:
                messages.error(request, 'Ошибка создания пользователя')
        return HttpResponseRedirect(reverse('register'))

class MyLogoutView(LogoutView):
    next_page = reverse_lazy('main')

