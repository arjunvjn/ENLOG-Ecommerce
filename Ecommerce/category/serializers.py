from rest_framework import serializers

from .models import Category

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
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