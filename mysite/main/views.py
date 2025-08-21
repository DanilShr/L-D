from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View


class MainView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user

        return render(request, 'main/index.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'main/form.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password1']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('main'))
        return render(request, 'main/form.html')
