from django.db import models


class Obras(models.Model):
    class Meta:
        ordering = ['id']

    pedido = models.IntegerField(null=False, blank=False, unique=True)
    data_lancamento = models.DateField(null=False, blank=False)
    data_inicio = models.DateField(null=False, blank=False)
    data_final = models.DateField(null=True, blank=True)
    observacao = models.TextField(null=True, blank=True)
