from rest_framework.viewsets import ModelViewSet

from . import serializers

from .models import MovementCategory, Movement


class BaseViewSet(ModelViewSet):
    """Base viewset"""
    model = Movement
    queryset = model.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.model.objects.filter(
            user=self.request.user
        )


class CategoryViewSet(BaseViewSet):
    """Viewset de las categorias"""
    serializer_class = serializers.CategorySerializer
    model = MovementCategory


class MovementViewSet(BaseViewSet):
    """Movements ViewSet"""
    serializer_class = serializers.MovementSerializer
    model = Movement
