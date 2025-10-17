
from django.urls import path
from django.views.generic import TemplateView
from .views import MainView, \
    OrdersView, ProfileView

urlpatterns = [
    path("", MainView.as_view(), name="main"),

    path("orders", OrdersView.as_view(), name="orders"),

    path("profile",ProfileView.as_view(), name="profile" ),

    path("about", TemplateView.as_view(template_name='main/about.html'), name="about"),

    path("order", TemplateView.as_view(template_name='basket/order.html'), name="order"),
]




