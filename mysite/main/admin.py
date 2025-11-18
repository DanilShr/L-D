from django.contrib import admin
from .models import Profile, Services, Product, Orders, OrderItem
from django.contrib.auth.models import User


# Register your models here.
@admin.register(Services)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name','description','image')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','description','image')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'avatar','phone','email')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fk_name = 'order'
    extra = 0

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'customer', 'created_at', 'payment', 'total', 'status')
    list_editable = ('status',)
    list_display_links = ('id', 'customer')
    list_filter = ('created_at', 'status')

