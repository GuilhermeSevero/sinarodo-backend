from django.db import models
from .obras import Obras
from .usuarios import Usuarios


class ObrasUsuarios(models.Model):
    class Meta:
        db_table = 'ObrasUsuarios'
        ordering = ['id']
        unique_together = ('obra', 'usuario',)

    obra = models.ForeignKey(Obras, on_delete=models.CASCADE, related_name='usuarios_obra')
    usuario = models.ForeignKey(Usuarios, on_delete=models.PROTECT)
    nota_final = models.FloatField(null=False, blank=False)
    observacao = models.TextField(null=True, blank=True)
    encarregado = models.BooleanField(blank=True, default=False)
