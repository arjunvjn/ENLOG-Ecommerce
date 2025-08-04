from django.db import models
import uuid

from user.models import CustomUser
from product.models import Product

# Create your models here.
class Order(models.Model):

    class StatusLevel(models.TextChoices):
        PENDING = 'pending'
        SHIPPED = 'shipped'
        DELIVERED = 'delivered'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='orders')
    products = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.FloatField(default=0)
    status = models.CharField(max_length=20, choices=StatusLevel.choices, default=StatusLevel.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
    
class OrderItem(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='order_items')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)