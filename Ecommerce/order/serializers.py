from rest_framework import serializers

from .models import Order, OrderItem
from category.serializers import CategorySerializer
from category.models import Category
from user.serializers import CustomUserSerializer
from product.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):

    user = CustomUserSerializer(fields=['id','email'], read_only=True)
    product = ProductSerializer(fields=['id', 'name', 'category', 'price'], read_only=True)

    class Meta:
        model = OrderItem
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        required_fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if required_fields:
            # Drop any fields that are not specified
            allowed = set(required_fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class OrderSerializer(serializers.ModelSerializer):

    user = CustomUserSerializer(fields=['id','email'], read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_items', 'total_price', 'status', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        required_fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if required_fields:
            # Drop any fields that are not specified
            allowed = set(required_fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)