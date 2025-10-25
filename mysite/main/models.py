from django.contrib.auth.models import User
from django.db import models
class Services(models.Model):
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)

# def name_src(instance, filename):
#         return f'products/{instance.name}/{filename}'

class Specification(models.Model):
    name = models.CharField(max_length=100, blank=True)
    size = models.CharField(max_length=100, blank=True)
    material = models.CharField(max_length=100, blank=True)
    painting = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=100, blank=True)




class Product(models.Model):
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    specifications = models.OneToOneField(Specification, on_delete=models.CASCADE, blank=True, null=True)

def __str__(self):
        return self.name



def avatar_dir(instance, filename):
    return f'Profile/Avatars/{instance.user.username}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=avatar_dir, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, blank=True)


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    count = models.IntegerField(default=0)


class Orders(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    payment = models.CharField(max_length=100, blank=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.IntegerField()

class Delivery(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=255)







