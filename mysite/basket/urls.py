from django.urls import path, include

from basket.views import BasketView

urlpatterns = [
    path("basket", BasketView.as_view(), name="basket"),
]