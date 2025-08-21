from django.urls import path
from django.conf.urls.static import static
from .views import MainView, LoginView

urlpatterns = [
    path("", MainView.as_view(), name="main"),
    path("login", LoginView.as_view(), name="login" ),
]


