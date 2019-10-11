from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.settings import api_settings
from rest_framework.permissions import AllowAny

from django.contrib.auth.views import LoginView

from core.serializers import ObteinAuthTokenSerializer, \
                             UserSerializer


class CreateUserViewset(CreateAPIView):
    """Viewset para registrar a un usuario"""
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class ObtainAuthTokenView(ObtainAuthToken):
    """Viewset para obtener el token"""
    serializer_class = ObteinAuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserView(RetrieveUpdateAPIView):
    """Viewset para Administrar la info del usuario"""
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class LoginView(LoginView):
    """View para crear una sesión de usuario"""
    template_name = 'core/login.html'
