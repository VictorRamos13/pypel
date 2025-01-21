from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('autenticacao.urls')),
    path('core/', include('core.urls')),
]
