from django.urls import include, path
from .views import registrar_entrada, registrar_saida

urlpatterns = [
    path("entrada/", registrar_entrada, name="registrar_entrada"),
    path("saida/", registrar_saida, name="registrar_saida"),
]
