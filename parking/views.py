from .docs import *
from .functions import *
from .models import Veiculo
from rest_framework import status
from django.utils.timezone import now
from .serializers import VeiculoSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


# Create your views here.
@registrar_entrada_docs
@api_view(["POST"])
def registrar_entrada(request):
    placa = request.data.get("placa")
    if not placa:
        return Response(
            {"error": "Placa é obrigatória"}, status=status.HTTP_400_BAD_REQUEST
        )

    if not validar_placa(placa):
        return Response(
            {"error": "Placa inválida. Use o padrão Mercosul ou o antigo."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    veiculo, created = Veiculo.objects.get_or_create(placa=placa)
    if not created:
        return Response(
            {"error": "Veículo já registrado"}, status=status.HTTP_400_BAD_REQUEST
        )

    serializer = VeiculoSerializer(veiculo)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@registrar_saida_docs
@api_view(["POST"])
def registrar_saida(request):
    placa = request.data.get("placa")
    pago = request.data.get("pago")
    veiculo = Veiculo.objects.filter(placa=placa).first()
    if not veiculo:
        return Response(
            {"error": "Veículo não encontrado"}, status=status.HTTP_404_NOT_FOUND
        )
    if veiculo.data_saida:
        return Response(
            {"error": "Este veículo não se encontra mais no estacionamento."},
            status=status.HTTP_404_NOT_FOUND,
        )
    if not veiculo.pago and (veiculo.pago != bool(pago) or not bool(pago)):
        return Response(
            {
                "error": "Pagamento não realizado! Efetue o pagamento para liberar o veículo."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if verificar_tolerancia(veiculo.data_pagamento):
        return Response(
            {"error": "Tempo de tolerância excedido. Efetue o pagamento novamente."},
            status=status.HTTP_403_FORBIDDEN,
        )

    veiculo.data_saida = now()
    veiculo.save()
    return Response(
        {"message": "Saída registrada com sucesso"}, status=status.HTTP_200_OK
    )


@consultar_valor_docs
@api_view(["GET"])
def consultar_valor(request):
    placa = request.query_params.get("placa")
    if not placa:
        return Response(
            {"error": "Placa não informada"}, status=status.HTTP_400_BAD_REQUEST
        )
    veiculo = Veiculo.objects.filter(placa=placa).first()
    if not veiculo:
        return Response(
            {"error": "Veículo não encontrado"}, status=status.HTTP_404_NOT_FOUND
        )

    valor = calcular_valor_a_pagar(veiculo)
    return Response({"valor": valor}, status=status.HTTP_200_OK)


@registrar_pagamento_docs
@api_view(["POST"])
def registrar_pagamento_view(request):
    placa = request.data.get("placa")
    error, valor = registrar_pagamento(placa)
    if error:
        return Response(error, status=status.HTTP_404_NOT_FOUND)

    return Response(
        {"message": "Pagamento realizado com sucesso", "valor_pago": valor},
        status=status.HTTP_200_OK,
    )


@relatorio_docs
@api_view(["GET"])
def relatorio(request):
    veiculos = Veiculo.objects.all()
    if not veiculos.exists():
        return Response(
            {"message": "Nenhum registro encontrado no sistema"},
            status=status.HTTP_200_OK,
        )
    serializer = VeiculoSerializer(veiculos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
