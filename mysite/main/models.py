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
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    specifications = models.OneToOneField(Specification, on_delete=models.CASCADE, blank=True, null=True)

def __str__(self):
        return self.name

class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=100, blank=True)
    customer = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    painting = models.CharField(max_length=100, blank=True)
    plastic = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=100, blank=True)
    delivery = models.CharField(max_length=100, blank=True)
    file = models.FileField(upload_to="Model/", blank=True, null=True)


def avatar_dir(instance, filename):
    return f'Profile/Avatars/{instance.user.username}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=avatar_dir, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, blank=True)






