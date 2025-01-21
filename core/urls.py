from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    path("main", views.main, name="main"),
]