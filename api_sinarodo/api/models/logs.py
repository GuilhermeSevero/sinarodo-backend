from django.db import models
from .usuarios import Usuarios


class Logs(models.Model):
    class Meta:
        db_table = 'logs'
        ordering = ['id']

    INFO = 'I'
    WARNING = 'W'
    ERROR = 'E'
    tipo_opcoes = (
        (INFO, 'Informação'),
        (WARNING, 'Atenção'),
        (ERROR, 'Erro')
    )

    data_hora = models.DateTimeField(null=False, blank=True, auto_now_add=True)
    usuario = models.ForeignKey(Usuarios, on_delete=models.DO_NOTHING)
    model = models.TextField(blank=False, null=False, max_length=25)
    tipo = models.CharField(choices=tipo_opcoes, max_length=1, null=False, blank=False)
    log = models.TextField(blank=False, null=False, max_length=2048)
