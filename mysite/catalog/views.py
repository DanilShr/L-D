from django.contrib.admin.templatetags.admin_list import pagination
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView, ListView

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


class ProductView(ListView):
    model = Product
    template_name = 'catalog/catalog.html'
    context_object_name = 'product_list'
    paginate_by = 2

    def get_queryset(self):
        filters = self.request.GET.getlist('type')

        queryset = super().get_queryset().select_related('specifications')
        if filters:
            queryset = queryset.filter(
                specifications__material__in=filters
            ).distinct()
        product_list = []
        for product in range(0, len(queryset), 3):
            product_list.append(queryset[product:product+3])
        return product_list




class ProductDetailView(DetailView):
    queryset = Product.objects.select_related('specifications').all()
    context_object_name = 'product'
    template_name = 'catalog/product.html'





