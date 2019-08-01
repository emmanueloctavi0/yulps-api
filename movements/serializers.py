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


class MovementSerializer(serializers.ModelSerializer):
    """Movement Serializer"""
    class Meta:
        model = models.Movement
        fields = (
            'id',
            'detail',
            'mount',
            'iso_code',
            'category',
        )

    def validate_category(self, value):
        """Validar que la categoria pertenece al usuario"""
        exists = models.MovementCategory.objects.filter(
            id=value.id,
            user=self.context['request'].user.id
        ).exists()

        if not exists:
            raise serializers.ValidationError('Object does not exist.')
        return value
