from django.urls import path
from django.conf.urls.static import static
from .views import MainView, LoginView

urlpatterns = [
    path("", LoginView.as_view(), name="main"),
]


