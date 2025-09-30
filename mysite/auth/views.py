from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View


# Create your views here.
class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('main'))
        return render(request, 'auth/login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'auth/form.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password2']
        email = request.POST['email']

        user = authenticate(request, username=username, password=password)
        if user:
            messages.error(request, "Пользователь существует")
            return HttpResponseRedirect(reverse('register'))
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

        return HttpResponseRedirect(reverse('login'))

class MyLogoutView(LogoutView):
    next_page = reverse_lazy('main')

