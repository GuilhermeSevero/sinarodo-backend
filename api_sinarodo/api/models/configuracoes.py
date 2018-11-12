from django.db import models


class Configuracoes(models.Model):
    class Meta:
        ordering = ['id']

    valor_por_ponto = models.FloatField(null=False, blank=False)
    acrescimo_encarregado = models.FloatField(null=False, blank=False)
