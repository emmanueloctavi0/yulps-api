from django.urls import path
from . import views


urlpatterns = [
    path('', views.FrontEndView.as_view() ),
]
