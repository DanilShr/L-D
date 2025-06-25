from django.shortcuts import render
from django.urls import reverse
from django.views import View


class MainView(View):
    def get(self, request):
        return render(request, 'main/index.html')


# Create your views here.
class LoginView(View):
    def post(self, request):
        if user.is_authenticated:
            return render(request, reverse("main:main"))
        username = request.POST['username']
        password = request.POST['password']
