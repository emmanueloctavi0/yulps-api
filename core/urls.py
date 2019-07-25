from django.urls import path

from . import views


app_name = 'auth'

urlpatterns = [
    path('signup/', views.CreateUserViewset.as_view(), name='create'),
    path('token/', views.ObtainAuthTokenView.as_view(), name='token'),
]
