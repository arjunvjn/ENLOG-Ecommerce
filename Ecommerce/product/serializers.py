from rest_framework import serializers

from .models import Product
from category.serializers import CategorySerializer
from category.models import Category

class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer(fields=['id','name'], read_only=True)

    class Meta:
        model = Product
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

    def validate_price(self, value):
        if not value > 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value