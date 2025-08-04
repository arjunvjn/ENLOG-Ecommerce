from django.db import models

from category.models import Category

# Create your models here.
class Product(models.Model):

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True)
    price = models.FloatField()
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name