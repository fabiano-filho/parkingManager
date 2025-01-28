from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from django.utils.timezone import now
from .functions import validar_placa, verificar_tolerancia
from .models import Veiculo
from .serializers import VeiculoSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
@api_view(["POST"])
@authentication_classes([JWTAuthentication])  # Define a autenticação JWT
@permission_classes([IsAuthenticated])
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


@api_view(["POST"])
@authentication_classes([JWTAuthentication])  # Define a autenticação JWT
@permission_classes([IsAuthenticated])
def registrar_saida(request):
    placa = request.data.get("placa")
    veiculo = Veiculo.objects.filter(placa=placa).first()
    if not veiculo:
        return Response(
            {"error": "Veículo não encontrado"}, status=status.HTTP_404_NOT_FOUND
        )

    if not veiculo.pago:
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
