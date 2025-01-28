from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils.timezone import now
from .functions import validar_placa
from .models import Veiculo
from .serializers import VeiculoSerializer


# Create your views here.
@api_view(["GET"])
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
