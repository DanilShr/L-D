from django.urls import path

from catalog.views import ServicesView, ProductView, ProductDetailView

urlpatterns = [

    path("servises", ServicesView.as_view(), name="services"),

    path("products", ProductView.as_view(), name="products"),

    path("products/<int:pk>", ProductDetailView.as_view(), name="product"),

]
