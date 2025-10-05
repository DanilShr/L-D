from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from basket.views import BasketView, BasketApiView

router = DefaultRouter()

router.register(r'basket', BasketApiView)

urlpatterns = [

    path('basket', TemplateView.as_view(template_name="basket/basket-api.html"), name="basket"),

    path('api/', include(router.urls))


]