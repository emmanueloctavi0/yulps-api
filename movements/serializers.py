from rest_framework import serializers

from . import models


class CategorySerializer(serializers.ModelSerializer):
    """Category Serializer"""
    class Meta:
        model = models.MovementCategory
        fields = (
            'id',
            'name',
            'description',
            'is_entry',
            'created_at',
            'updated_at',
        )
