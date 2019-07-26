from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from . import serializers

from .models import MovementCategory


class CategoryViewSet(ModelViewSet):
    """Viewset de las categorias"""
    serializer_class = (serializers.CategorySerializer)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = MovementCategory.objects.all()

    def get_queryset(self):
        return MovementCategory.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
