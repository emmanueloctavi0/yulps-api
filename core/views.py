from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView
from rest_framework.settings import api_settings

from core.serializers import CreateUserSerializer, ObteinAuthTokenSerializer


class CreateUserViewset(CreateAPIView):
    serializer_class = CreateUserSerializer

    def perform_create(self, serializer):
        serializer.save()


class ObtainAuthTokenView(ObtainAuthToken):
    serializer_class = ObteinAuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
