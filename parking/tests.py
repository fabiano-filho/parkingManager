from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils.timezone import now, timedelta
from django.contrib.auth.models import User
from .models import Veiculo
from django.conf import settings


# Create your tests here.
class EstacionamentoTestCase(TestCase):
    def setUp(self):
        """
        Configura os dados iniciais para os testes.
        """
        self.client = APIClient()

        # Criar um usuário para autenticação
        self.user = User.objects.create_user(username="admin", password="admin123")

        # Autenticar o usuário e obter o token JWT
        response = self.client.post(
            "/api/login/", {"username": "admin", "password": "admin123"}, format="json"
        )
        self.access_token = response.data.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        # Criar veículo com registro de entrada
        self.veiculo_entrada = Veiculo.objects.create(
            placa="ABC1234", data_entrada=now()  # Padrão antigo
        )

        # Criar veículo com pagamento registrado
        self.veiculo_pago = Veiculo.objects.create(
            placa="XYZ1D23",  # Padrão Mercosul
            data_entrada=now() - timedelta(hours=2),
            data_pagamento=now(),
            valor_pago=10.0,
            pago=True,
        )

    def test_registrar_entrada_veiculo(self):
        """
        Testa o registro de entrada de um veículo.
        """
        response = self.client.post(
            "/api/entrada/", {"placa": "DEF5678"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["placa"], "DEF5678")

    def test_registrar_entrada_veiculo_placa_invalida(self):
        """
        Testa o registro de entrada com placa inválida.
        """
        response = self.client.post(
            "/api/entrada/", {"placa": "1234567"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Placa inválida", response.data["error"])

    def test_acesso_sem_autenticacao(self):
        """
        Testa o acesso negado a um endpoint protegido sem autenticação.
        """
        # Remove o token de autenticação
        self.client.credentials()
        response = self.client.post(
            "/api/entrada/", {"placa": "GHI8901"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_registrar_saida_veiculo_sem_pagamento(self):
        """
        Testa o registro de saída sem pagamento.
        """
        response = self.client.post("/api/saida/", {"placa": "ABC1234"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Pagamento não realizado!",
            response.data["error"],
        )

    def test_registrar_saida_veiculo_com_tolerancia(self):
        """
        Testa o registro de saída dentro do tempo de tolerância após pagamento.
        """
        response = self.client.post(
            "/api/saida/", {"placa": "XYZ1D23", "pago": True}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Saída registrada com sucesso", response.data["message"])

    def test_registrar_saida_veiculo_fora_tolerancia(self):
        """
        Testa o registro de saída fora do tempo de tolerância após pagamento.
        """
        self.veiculo_pago.data_pagamento = now() - timedelta(
            minutes=settings.TOLERANCIA_TEMPO_SAIDA + 1
        )
        self.veiculo_pago.save()

        response = self.client.post("/api/saida/", {"placa": "XYZ1D23"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("Tempo de tolerância excedido", response.data["error"])

    def test_consultar_valor_a_pagar(self):
        """
        Testa a consulta do valor a pagar para um veículo.
        """
        response = self.client.get("/api/valor/?placa=ABC1234", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("valor", response.data)

    def test_registrar_pagamento(self):
        """
        Testa o registro de pagamento de um veículo.
        """
        response = self.client.post("/api/pagar/", {"placa": "ABC1234"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("valor_pago", response.data)
        veiculo = Veiculo.objects.get(placa="ABC1234")
        self.assertTrue(veiculo.pago)
