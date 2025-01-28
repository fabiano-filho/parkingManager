from django.urls import path
from .views import (
    registrar_entrada,
    registrar_saida,
    consultar_valor,
    registrar_pagamento_view,
    relatorio,
)

urlpatterns = [
    path("entrada/", registrar_entrada, name="registrar_entrada"),
    path("saida/", registrar_saida, name="registrar_saida"),
    path("valor/", consultar_valor, name="consultar_valor"),
    path("pagar/", registrar_pagamento_view, name="registrar_pagamento"),
    path("relatorio/", relatorio, name="relatorio"),
]
