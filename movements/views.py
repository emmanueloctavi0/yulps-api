from rest_framework.viewsets import ModelViewSet

from . import serializers

from .models import MovementCategory


class CategoryViewSet(ModelViewSet):
    """Viewset de las categorias"""
    serializer_class = serializers.CategorySerializer

    queryset = MovementCategory.objects.all()

    def get_queryset(self):
        return MovementCategory.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
