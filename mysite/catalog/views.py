from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView

from main.models import Services, Product
from main.models import Orders


# Create your views here.
class ServicesView(View):
    def get(self, request):
        services = Services.objects.all()
        context = {
            'services': services,
        }
        return render(request, 'catalog/servises.html', context=context)

    def post(self, request):
        data = request.POST.dict()
        user = request.user
        file = request.FILES['file']
        del data['csrfmiddlewaretoken']
        data['user'] = user
        order = Orders.objects.create(**data, file=file)
        order.save()
        return redirect('services')


class ProductView(View):
    def get(self, request):
        products = Product.objects.all()
        product_list = []
        for product in range(0, len(products), 3):
            product_list.append(products[product:product+3])
        context = {
            'product_list': product_list,
        }
        return render(request, 'catalog/catalog.html', context=context)


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    context_object_name = 'product'
    template_name = 'catalog/product.html'