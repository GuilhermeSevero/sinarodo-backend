from django.db import models


class Configuracoes(models.Model):
    class Meta:
        db_table = 'Configuracoes'
        ordering = ['id']

    acrescimo_encarregado = models.FloatField(null=False, blank=True, default=10.0)
    dias_em_campo = models.IntegerField(null=False, blank=True, default=15)
    premio_seis = models.FloatField(null=False, blank=True, default=200.0)
    premio_sete = models.FloatField(null=False, blank=True, default=400.0)
    premio_oito = models.FloatField(null=False, blank=True, default=600.0)
    premio_nove = models.FloatField(null=False, blank=True, default=800.0)
    premio_dez = models.FloatField(null=False, blank=True, default=1000.0)
