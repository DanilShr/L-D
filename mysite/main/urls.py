from django.urls import path
from django.conf.urls.static import static
from mysite import settings
from .views import MainView

urlpatterns = [
    path("", MainView.as_view(), name="main")
]
