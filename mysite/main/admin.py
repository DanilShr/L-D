from django.contrib import admin
from .models import Services
from django.contrib.auth.models import User


# Register your models here.
@admin.register(Services)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name','description','image')

