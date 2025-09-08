from django.db import models

# Create your models here.
class Services(models.Model):
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)

# def name_src(instance, filename):
#         return f'products/{instance.name}/{filename}'


class Product(models.Model):
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

def __str__(self):
        return self.name


