from django.db import models


class Categorias(models.Model):
    class Meta:
        ordering = ['id']

    descricao = models.CharField(max_length=100, null=False, blank=False, unique=True)
    peso = models.IntegerField(null=False, blank=False)

