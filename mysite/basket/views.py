from urllib import request

from django.shortcuts import render, redirect
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from basket.serializers import BasketSerializer
from main.models import Basket, Product, Profile, Orders, OrderItem


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
        queryset = queryset.select_related('product').filter(user=self.request.user)
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        print(data)
        if instance.count <= 1 or data.get("type") == 'all':
            print('полное удаление')
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            print('мягкое удаление')
            instance.count -= 1
            instance.price -= instance.product.price
            instance.save()
            return Response(BasketSerializer(instance).data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data)
        if 'basket' in data:
            baksetID = data.get('basket')
            product = data.get('product')
            product = Product.objects.get(id=product)
            basket = Basket.objects.get(id=baksetID, user=request.user)
            basket.count += 1
            basket.price += product.price
            basket.save()
            return Response(BasketSerializer(basket).data, status=status.HTTP_200_OK)
        else:
            product = data.get('product')
            product = Product.objects.get(id=product)
            basket, create = Basket.objects.get_or_create(user=request.user, product=product, defaults={
                'user': request.user,
                'product': product,
                'price': product.price,
                'count': 1
            })
            if not create:
                print('update')
                basket.count += 1
                basket.price += product.price
                basket.save()
            return Response(BasketSerializer(basket).data, status=status.HTTP_200_OK)


class OrderView(View):
    def get(self, request):
        user = request.user
        baskets = Basket.objects.select_related('product').filter(user=user)
        profile = Profile.objects.select_related('user').get(user=user)
        context = {
            'baskets': baskets,
            'profile': profile,
        }
        return render(request, 'basket/order.html', context)

    def post(self, request):
        payment = request.POST.get('payment')
        delivery = request.POST.get('delivery')
        user = request.user
        profile = Profile.objects.get(user=user)
        try:
            order = Orders.objects.create(customer=profile, status='В ожидании оплаты', payment=payment, delivery=delivery)
            baskets = Basket.objects.select_related('product').filter(user=user).defer('id', 'user')
            for basket in baskets:
                OrderItem.objects.create(order=order, product_name=basket.product, count=basket.count, price=basket.price)
            baskets.delete()
        except Exception as e:
            print(f"Ошибка создания заказа {e}")

        return redirect('orders')





