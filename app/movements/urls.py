from rest_framework.routers import DefaultRouter

from django.urls import path, include

from . import views


router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('movements', views.MovementViewSet, basename='movements')

app_name = 'movement'

urlpatterns = [
    path('', include(router.urls)),
]
