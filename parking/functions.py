import re


def validar_placa(placa):
    """
    Valida o formato da placa. Aceita apenas o padrão Mercosul ou antigo.
    """
    padrao_antigo = r"^[A-Z]{3}[0-9]{4}$"  # Ex.: ABC1234
    padrao_mercosul = r"^[A-Z]{3}[0-9][A-Z][0-9]{2}$"  # Ex.: ABC1D23

    if not re.match(padrao_antigo, placa) and not re.match(padrao_mercosul, placa):
        return False
    return True
