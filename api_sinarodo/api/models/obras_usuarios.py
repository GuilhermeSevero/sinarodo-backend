from django.db import models
from .obras import Obras
from .usuarios import Usuarios


class ObrasUsuarios(models.Model):
    class Meta:
        ordering = ['id']

    obra = models.ForeignKey(Obras, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuarios, on_delete=models.PROTECT)
    nota_final = models.IntegerField(null=False, blank=False)
    observacao = models.TextField(null=True, blank=True)

