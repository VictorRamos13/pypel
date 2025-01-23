from django.contrib import admin
from django.urls import path, include

#aqui permite que o django possa acessar a urls de outros apps
urlpatterns = [
    path('', include('autenticacao.urls')),
    path('core/', include('core.urls')),
    path('cadastros/', include('cadastros.urls')),
]
