from django.shortcuts import render, redirect
from django.views import View

from main.models import Basket, Product


# Create your views here.


class BasketView(View):
    def get(self, request):
        user = request.user
        basket = Basket.objects.select_related('user').prefetch_related('product').filter(user=user)
        context = {
            'baskets': basket,
        }
        return render(request, 'basket/basket.html', context)

    def post(self, request):
        id_product = request.POST.get('product_id')
        product = Product.objects.get(id=id_product)
        user = request.user
        if user.is_anonymous:
            pass
        else:
            basket, created = Basket.objects.get_or_create(user=user, product=product,
                                                  defaults={
                                                      'user': user,
                                                      'product': product,
                                                      'price': product.price,
                                                      'count': 1
                                                  })
            if not created:
                basket.count += 1
                basket.price = product.price * basket.count
                basket.save()
        return redirect('products')