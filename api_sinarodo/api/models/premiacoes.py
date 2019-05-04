from django.db import models
from .categorias import Categorias
from .obras_usuarios import ObrasUsuarios


class Premiacoes(models.Model):
    class Meta:
        db_table = 'premiacoes'
        ordering = ['id']
        unique_together = ('mes_periodo', 'ano_periodo', 'categoria', 'obras_usuario')

    mes_periodo = models.IntegerField(null=False, blank=False)
    ano_periodo = models.IntegerField(null=False, blank=False)
    dias_em_campo = models.IntegerField(null=False, blank=False)
    nota = models.IntegerField(null=False, blank=False)
    categoria = models.ForeignKey(Categorias, on_delete=models.PROTECT)
    obras_usuario = models.ForeignKey(ObrasUsuarios, on_delete=models.CASCADE, related_name='premiacoes')
