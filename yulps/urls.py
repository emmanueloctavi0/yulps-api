from django.contrib import admin
from django.urls import path, include

from core.views import LoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/auth/', include('core.urls')),
    path('v1/', include('movements.urls')),

    path('login/', LoginView.as_view(), name='login'),
]
