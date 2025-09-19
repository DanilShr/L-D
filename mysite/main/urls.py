from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf.urls.static import static
from .views import MainView, LoginView, RegisterView, MyLogoutView, ServicesView, ProductView, ProductDetailView, \
    OrdersView, ProfileView

urlpatterns = [
    path("", MainView.as_view(), name="main"),
    path("login", LoginView.as_view(), name="login" ),
    path("register", RegisterView.as_view(), name="register" ),

    path("logout", MyLogoutView.as_view(), name="logout" ),

    path("servises", ServicesView.as_view(), name="services"),

    path("products/", ProductView.as_view(), name="products"),

    path("products/<int:pk>", ProductDetailView.as_view(), name="product"),

    path("orders", OrdersView.as_view(), name="orders"),

    path("profile",ProfileView.as_view(), name="profile" ),
]


