from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from .serializers import VeiculoSerializer

# Documentação para registrar_entrada
registrar_entrada_docs = extend_schema(
    summary="Registrar entrada de veículo",
    description="Registra a entrada de um veículo no estacionamento com base na placa fornecida.",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "placa": {
                    "type": "string",
                    "description": "Placa do veículo no formato Mercosul ou antigo.",
                    "example": "ABC1234",
                }
            },
            "required": ["placa"],
        }
    },
    responses={
        201: VeiculoSerializer,
        400: {"type": "object", "properties": {"error": {"type": "string"}}},
    },
)

# Documentação para registrar_saida
registrar_saida_docs = extend_schema(
    summary="Registrar saída de veículo",
    description="Registra a saída de um veículo do estacionamento após validar o pagamento e verificar as condições de tolerância.",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "placa": {
                    "type": "string",
                    "description": "Placa do veículo no formato Mercosul ou antigo.",
                    "example": "ABC1234",
                },
                "pago": {
                    "type": "boolean",
                    "description": "Indica se o pagamento foi realizado.",
                    "example": True,
                },
            },
            "required": ["placa", "pago"],
        }
    },
    responses={
        200: {"type": "object", "properties": {"message": {"type": "string"}}},
        400: {"type": "object", "properties": {"error": {"type": "string"}}},
        404: {"type": "object", "properties": {"error": {"type": "string"}}},
        403: {"type": "object", "properties": {"error": {"type": "string"}}},
    },
)

# Documentação para consultar_valor
consultar_valor_docs = extend_schema(
    summary="Consultar valor a pagar",
    description="Consulta o valor devido por um veículo no estacionamento com base na placa fornecida.",
    parameters=[
        OpenApiParameter(
            name="placa",
            description="Placa do veículo no formato Mercosul ou antigo.",
            required=True,
            type=str,
            location=OpenApiParameter.QUERY,
        )
    ],
    responses={
        200: {"type": "object", "properties": {"valor": {"type": "number"}}},
        400: {"type": "object", "properties": {"error": {"type": "string"}}},
        404: {"type": "object", "properties": {"error": {"type": "string"}}},
    },
)

# Documentação para registrar_pagamento_view
registrar_pagamento_docs = extend_schema(
    summary="Registrar pagamento",
    description="Registra o pagamento de um veículo no estacionamento com base na placa fornecida.",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "placa": {
                    "type": "string",
                    "description": "Placa do veículo no formato Mercosul ou antigo.",
                    "example": "ABC1234",
                }
            },
            "required": ["placa"],
        }
    },
    responses={
        200: {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "valor_pago": {"type": "number"},
            },
        },
        404: {"type": "object", "properties": {"error": {"type": "string"}}},
    },
)

# Documentação para relatorio
relatorio_docs = extend_schema(
    summary="Relatório de veículos",
    description="Retorna um relatório com todos os registros de entrada e saida no sistema.",
    responses={
        200: VeiculoSerializer(many=True),
        404: {"type": "object", "properties": {"message": {"type": "string"}}},
    },
)
