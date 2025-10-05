from django.shortcuts import render, redirect
from django.views import View
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from basket.serializers import BasketSerializer
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


class BasketApiView(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.count <= 1:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            instance.count -= 1
            instance.price -= instance.product.price
            instance.save()
            return Response(BasketSerializer(instance).data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        baksetID, product = request.data['basket'], request.data['product']
        product = Product.objects.get(id=product)
        basket = Basket.objects.get(id=baksetID, user=request.user)
        if basket:
            basket.count += 1
            basket.price += product.price
            basket.save()
            return Response(BasketSerializer(basket).data, status=status.HTTP_200_OK)
        else:
            return super().create(request, *args, **kwargs)




