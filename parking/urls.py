from django.urls import include, path
from .views import registrar_entrada, registrar_saida, consultar_valor

urlpatterns = [
    path("entrada/", registrar_entrada, name="registrar_entrada"),
    path("saida/", registrar_saida, name="registrar_saida"),
    path("valor/", consultar_valor, name="consultar_valor"),
]
