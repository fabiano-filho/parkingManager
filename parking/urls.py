from django.urls import include, path
from .views import registrar_entrada

urlpatterns = [
    path("entrada/", registrar_entrada, name="registrar_entrada"),
]
