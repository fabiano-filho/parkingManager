import re
from django.conf import settings
from django.utils.timezone import now, timedelta


def validar_placa(placa):
    """
    Valida o formato da placa. Aceita apenas o padrão Mercosul ou antigo.
    """
    padrao_antigo = r"^[A-Z]{3}[0-9]{4}$"  # Ex.: ABC1234
    padrao_mercosul = r"^[A-Z]{3}[0-9][A-Z][0-9]{2}$"  # Ex.: ABC1D23

    if not re.match(padrao_antigo, placa) and not re.match(padrao_mercosul, placa):
        return False
    return True


def verificar_tolerancia(data_pagamento):
    """
    Verifica se o tempo de tolerância após o pagamento foi excedido.
    """
    tolerancia = timedelta(minutes=settings.TOLERANCIA_TEMPO_SAIDA)
    return now() - data_pagamento > tolerancia


def calcular_valor_a_pagar(veiculo):
    """
    Calcula o valor a pagar para um veículo com base no tempo de permanência.
    """
    diferenca = now() - veiculo.data_entrada
    horas = (diferenca.total_seconds() // 3600) + (
        1 if diferenca.total_seconds() % 3600 else 0
    )
    return horas * settings.ESTACIONAMENTO_VALOR_HORA
