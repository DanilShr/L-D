from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.defaultfilters import first
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView

from main.models import Services, Product


class MainView(View):
    def get(self, request):
        user = request.user
        context = {
            'user': user,
        }
        return render(request, 'main/index.html', context=context)


class LoginView(View):
    def get(self, request):
        return render(request, 'main/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('main'))
        return render(request, 'main/login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'main/form.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password2']
        email = request.POST['email']

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return HttpResponseRedirect(reverse('login'))

class MyLogoutView(LogoutView):
    next_page = reverse_lazy('main')

class ServicesView(View):
    def get(self, request):
        services = Services.objects.all()
        context = {
            'services': services,
        }
        return render(request, 'main/servises.html', context=context)


class ProductView(View):
    def get(self, request):
        products = Product.objects.all()
        product_list = []
        for product in range(0, len(products), 3):
            product_list.append(products[product:product+3])
        context = {
            'product_list': product_list,
        }
        return render(request, 'main/catalog.html', context=context)


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    context_object_name = 'product'
    template_name = 'main/product.html'
