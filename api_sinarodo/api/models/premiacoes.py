from django.db import models
from .categorias import Categorias


class Premiacoes(models.Model):
    class Meta:
        ordering = ['id']

    mes_periodo = models.IntegerField(null=False, blank=False)
    ano_periodo = models.IntegerField(null=False, blank=False)
    dias_em_campo = models.IntegerField(null=False, blank=False)
    nota = models.IntegerField(null=False, blank=False)
    categoria = models.ForeignKey(Categorias, on_delete=models.PROTECT)
