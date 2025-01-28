from django.db import models
from django.utils.timezone import now


# Create your models here.
class Veiculo(models.Model):
    placa = models.CharField(max_length=7, unique=True)
    data_entrada = models.DateTimeField(default=now)
    data_saida = models.DateTimeField(null=True, blank=True)
    valor_pago = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    pago = models.BooleanField(default=False)
    data_pagamento = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.placa} - Entrada: {self.data_entrada}"
