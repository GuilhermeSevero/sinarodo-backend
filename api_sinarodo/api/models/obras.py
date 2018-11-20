from django.db import models


class Obras(models.Model):
    class Meta:
        db_table = 'Obras'
        ordering = ['id']

    pedido = models.CharField(max_length=20, null=False, blank=False, unique=True)
    data_lancamento = models.DateField(null=False, blank=False)
    data_inicio = models.DateField(null=False, blank=False)
    data_final = models.DateField(null=True, blank=True)
    observacao = models.TextField(null=True, blank=True)
